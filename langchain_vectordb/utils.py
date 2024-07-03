from rest_framework import status
from rest_framework.response import Response
import threading
from .html import *
from .html import extract_interactive_elements
import time
import re
from .html import clean_html
import json
from django.core.files import File
from io import BytesIO
import boto3
import os
import shutil
import urllib
import uuid
from django.conf import settings
from .core.doc_service import DocService
from .core.pdf_service import PDFService
import pickle


def create_chat_model_for_resume(resume):
    HOME = settings.TEMP_DIR
    uuid_memory = str(uuid.uuid4())

    # Create temp_save_directory if it does not exist
    temp_save_directory = os.path.join(HOME, 'dataset')
    if not os.path.exists(temp_save_directory):
        os.makedirs(temp_save_directory)

    # Download resume file from AWS bucket and save in temp_file
    resume_file = resume.file
    unique_filename = str(uuid.uuid4()) + '.' + resume.file.name.split('.')[-1]
    temp_file_path = os.path.join(
        temp_save_directory, unique_filename)  # Local temp path

    with open(temp_file_path, 'wb') as f:
        resume_file.open('rb')
        shutil.copyfileobj(resume_file, f)
        resume_file.close()

    # Initialize PDFService with the local file path
    persist_directory = os.path.join(HOME, "chroma_storage", uuid_memory)
    # Create persist_directory if it does not exist
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)

    cht_mdl = PDFService(temp_file_path, persist_directory=persist_directory)

    # Fetch document and create vector index
    cht_mdl.fetch_document()
    cht_mdl.create_vector_index()

    cht_mdl_bytes = pickle.dumps(cht_mdl)
    cht_mdl_pkl_in_memory = BytesIO(cht_mdl_bytes)
    cht_mdl_file = File(cht_mdl_pkl_in_memory, name="cht_mdl.pkl")
    resume.chat_model = cht_mdl_file
    resume.save()
    cht_mdl_pkl_in_memory.close()

    # Clean up the temporary file and chroma_storage directory
    os.remove(temp_file_path)


def get_chat_model_from_resume(resume):

    if resume.chat_model:
        with resume.chat_model.open('rb') as file:
            chat_model_bytes = file.read()
            chat_model = pickle.loads(chat_model_bytes)
            return chat_model
    else:
        return None


def extract_json_substring(text):
    # This regex looks for a pattern where ```json is followed by any characters (non-greedy)
    # until ``` is found
    matches = re.findall(r'```json(.*?)```', text, re.DOTALL)
    return matches  # Returns a list of all captured groups


def resume_query(resume, query):
    prompt = """
    The current date is 24th Jan 2024.
    Assume the role of a user who is applying for a job, and respond to questions on a job application form.
    You are provided with the user's personal and professional information in the context.
    You will be given a part of the html form to be filled. Fill the form like the user would.

    Your actions include:
    1. Filling text fields with accurate information
    2. Selection of correct options like dropdowns, buttons, etc.
    3. Upload resume if already not present.
    4. Clicking correct buttons like apply, submit, next , so on.

    Important:
    1. Don't include any other selectors in the reponse which is not there in the form.

    Give your response strictly in this format:
    {"responses":[{"selector":<selector for html element with attributes>,"response" : <value to enter or action to do in the html element>},...]}
    """

    # Process the query to extract and clean interactive HTML elements
    html, class_dict, id_dict = reduce_tokens(query)
    cleaned_query = clean_html_2(extract_interactive_elements(html))
    print(cleaned_query)
    # Ensure a chat model exists for the resume, creating one if necessary
    if not resume.chat_model:
        create_chat_model_for_resume(resume)

    # Retrieve the chat model from the resume
    cht_mdl = get_chat_model_from_resume(resume)

    # Record the start time of the query
    start_time = time.time()

    # Query the document using the chat model
    output = cht_mdl.query_document(prompt=prompt + cleaned_query)

    # Attempt to parse the output as JSON
    try:
        response = json.loads(output)
    except Exception as e:
        # If parsing fails, attempt to extract and parse the JSON substring
        response = json.loads(extract_json_substring(output)[0])

    # Log the response
    # print(response)

    # Replace placeholders in the response with actual ids and classes from the original HTML
    for item in response.get("responses", []):
        selector = item.get("selector", "")
        # Replace class and id placeholders
        # Sort class_dict and id_dict by the length of placeholders in descending order to replace longer placeholders first
        for class_name, placeholder in sorted(class_dict.items(), key=lambda x: len(x[1]), reverse=True):
            selector = selector.replace(placeholder, class_name)
        for id_name, placeholder in sorted(id_dict.items(), key=lambda x: len(x[1]), reverse=True):
            selector = selector.replace(placeholder, id_name)
        item["selector"] = selector
    # Record the end time and calculate the duration
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    # print(response)
    return response


def resume_query2(cht_mdl, query, timeout_seconds=10):
    class QueryThread(threading.Thread):
        def __init__(self, cht_mdl, query):
            threading.Thread.__init__(self)
            self.cht_mdl = cht_mdl
            self.query = query
            self.result = None
            self.exception = None

        def run(self):
            try:
                prompt = """
                The current date is 24th Jan 2024.
                Assume the role of a user who is applying for a job, and respond to questions on a job application form.
                You are provided with the user's personal and professional information in the context.
                Answer every question/query as if you are filling an online form with concise and accurately formatted responses as if you were completing an online form.
                Give only the required data in json format.
                {"question":<question>,"answer":<answer to the question in required type given in question>}
                Here is the question
                """
                self.result = self.cht_mdl.query_document(
                    prompt=prompt + json.dumps(self.query))
            except Exception as e:
                self.exception = e

    query_thread = QueryThread(cht_mdl, query)
    query_thread.start()
    query_thread.join(timeout=timeout_seconds)

    if query_thread.is_alive():
        return None, Response({'error': 'Timeout error'}, status=status.HTTP_408_REQUEST_TIMEOUT)

    if query_thread.exception:
        error = query_thread.exception
        error_response = Response(
            {'error': error.response.text}, status=error.response.status_code)
        return None, error_response

    try:
        output = json.loads(query_thread.result)
    except Exception as e:
        output = json.loads(extract_json_substring(query_thread.result)[0])

    return output, None
