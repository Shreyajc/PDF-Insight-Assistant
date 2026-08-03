
import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader


def load_pdfs(uploaded_files):
    """
    Save uploaded PDFs temporarily and load them using PyPDFLoader.
    """

    documents = []

    for uploaded_file in uploaded_files:

        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(uploaded_file.read())

            temp_path = temp_file.name

        # Load PDF
        loader = PyPDFLoader(temp_path)

        docs = loader.load()

        documents.extend(docs)

    return documents