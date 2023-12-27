import os
import shutil
import urllib
import uuid
from django.conf import settings
from .core.doc_service import DocService


def start():
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
