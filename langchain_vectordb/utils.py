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
    They current date is 24th Jan 2024.
    Assume the role of a user who is applying for a job, and respond to questions on a job application form.
    You are provided with the user's personal and professional information in the context.
    Answer every question/query as if you are filling an online form with concise and accurately formatted responses as if you were completing an online form.
    
    Give your response strictly in this format:
    {"responses":[{"selector":<selector for html element with attributes>."response" : <value to enter or action to do in the html element>},...]}
    

    """
    html, class_dict, id_dict = reduce_tokens(query)
    cleaned_query = clean_html_2(
        extract_interactive_elements(html))
    print(cleaned_query)
    if (resume.chat_model == ""):
        create_chat_model_for_resume(resume)

    cht_mdl = get_chat_model_from_resume(resume)

    start_time = time.time()
    output = cht_mdl.query_document(prompt=prompt+cleaned_query)
    print(output)
    try:
        response = json.loads(output)
    except Exception as e:
        response = json.loads(extract_json_substring(output)[0])

    # Replace ids and classes in the response
    for item in response.get('responses', []):
        selector = item.get('selector', '')
        for original_id, replacement_id in id_dict.items():
            selector = selector.replace(
                f'#{original_id}', f'#{replacement_id}')
        for original_class, replacement_class in class_dict.items():
            selector = selector.replace(
                f'.{original_class}', f'.{replacement_class}')
        item['selector'] = selector
    print(response)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return response


def resume_query2(resume, query):
    prompt = """Assume the role of a user who is applying for a job, and respond to questions on a job application form.
    Give only the required data.
    
    """
    if (resume.chat_model == ""):
        create_chat_model_for_resume(resume)

    cht_mdl = get_chat_model_from_resume(resume)

    start_time = time.time()
    output = cht_mdl.query_document(prompt=prompt+query+":")
    print(output)
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    return {"response": output}
