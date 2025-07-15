# Reloads all documents by reading the docuemnts poaths, ccreating the corresponding embeddingss and storing them in the database.
import glob
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from mia.backend.chroma.chroma import get_chroma_client, reset_db, get_collection_name
import logging

def reload_docs(method:str, embedding_name, chunk_size, chunk_overlap):
    client = get_chroma_client()
    reset_db()
    # collection_name = get_collection_name(model_name=embedding_name, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    collection_name = "mia-test"
    embedding_model = OpenAIEmbeddings(model=embedding_name)

    vector_store = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=embedding_model,
    )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    pdf_list = get_test_raw_pdf_docs("data/raw")
    # TODO: Refactor this for re-usability
    for pdf in pdf_list:
        loader = PyPDFLoader(pdf)
        document = loader.load()
        chunks = text_splitter.split_documents(document)
        # embeddings = embedding_model.embed(chunks) # This is not needed a the embeddings are calculated in the Chroma class
        chunks = calculate_pdf_chunk_ids(chunks)
        chunk_ids = [chunk.metadata["id"] for chunk in chunks]
        vector_store.add_documents(chunks, ids=chunk_ids)
    

def calculate_pdf_chunk_ids(chunks):

    # This will create IDs like "data/monopoly.pdf:6:2"
    # Page Source : Page Number : Chunk Index

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        normalize_pdf_name(source)
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        # If the page ID is the same as the last one, increment the index.
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks

def get_test_raw_pdf_docs(path:str):
    # searches all pdf files in the given path and returns a list of their paths
    return glob.glob(f"{path}/*.pdf")

def normalize_pdf_name(pdf:str):
    # normalizes the pdf name by removing the path, extension and replacing spaces or any other special characterss with underscores

    pdf = pdf.split("/")[-1]
    pdf = pdf.split(".")[0]
    # pdf = re.sub(r'\W+', '_', pdf)
    return pdf

if __name__ == '__main__':
    reload_docs("pdf", "text-embedding-3-small", 1000, 50)


