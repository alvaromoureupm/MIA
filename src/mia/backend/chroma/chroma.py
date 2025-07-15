import os
import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

def get_chroma_client(host, port) -> ClientAPI:
    load_dotenv()
    return chromadb.HttpClient(
        host=host,
        port=port,
        settings=Settings(
            chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",
            chroma_client_auth_credentials=os.getenv("CHROMA_CLIENT_AUTH_CREDENTIALS"),
            allow_reset = True
        ),
    )

def get_collection_name(model_name: str, chunk_size:str, chunk_overlap:str) -> str:
    return f"{model_name}_{chunk_size}_{chunk_overlap}"

def reset_db():
    client = get_chroma_client()
    client.reset()


def initialize_chroma_vector_store(host="localhost", port=8000, embedding_name="text-embedding-3-small", collection_name="mia-test"):
    client = get_chroma_client(host, port)
    embedding = OpenAIEmbeddings(model=embedding_name)
    client.get_or_create_collection(collection_name)
    vector_store = Chroma(
        client=client, collection_name="mia-test", embedding_function=embedding
    )
    
    return vector_store

if __name__ == "__main__":
    reset_db()




