import os
import shutil
import urllib
import uuid
from django.conf import settings
from .core.doc_service import DocService
from .core.pdf_service import PDFService


def start_testing():
    """ for testing prompts """
    HOME = settings.TEMP_DIR

    uuid_memory = str(uuid.uuid4())
    temp_save_directory = os.path.join(HOME, 'dataset')

    filename = "test.docx"  # add the file name here
    data_path = os.path.join(temp_save_directory, filename)

    cht_mdl = DocService(data_path, persist_directory=os.path.join(
        HOME, "chroma_storage", uuid_memory))
    cht_mdl.fetch_document()
    cht_mdl.create_vector_index()

    while True:
        query = input("input the text here: ")
        output = cht_mdl.query_document(prompt=query)
        print(output)


def resume_queries(resume, queries):
    """ given a resume, takes queries and returns responses"""
    HOME = settings.TEMP_DIR

    uuid_memory = str(uuid.uuid4())
    temp_save_directory = os.path.join(HOME, 'dataset')

    # Download resume file from AWS bucket and save in temp_file
    resume_file = resume.file
    unique_filename = str(uuid.uuid4())+resume.file.name.split('.')[-1]
    temp_file_path = os.path.join(temp_save_directory, unique_filename)

    with open(temp_file_path, 'wb') as f:
        resume_file.open('rb')
        shutil.copyfileobj(resume_file, f)
        resume_file.close()

    if (resume_file.name.endswith('pdf')):
        cht_mdl = PDFService(temp_file_path, persist_directory=os.path.join(
            HOME, "chroma_storage", uuid_memory))
    else:

        cht_mdl = DocService(temp_file_path, persist_directory=os.path.join(
            HOME, "chroma_storage", uuid_memory))

    cht_mdl.fetch_document()
    cht_mdl.create_vector_index()

    responses = []
    for query in queries:
        output = cht_mdl.query_document(prompt=query)
        responses.append({"query": query, "response": output})

    # Clean up the temporary file
    os.remove(temp_file_path)
    return responses
