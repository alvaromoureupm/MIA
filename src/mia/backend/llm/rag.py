from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain import hub
from langchain_chroma import Chroma
from mia.backend.chroma.chroma import initialize_chroma_vector_store
from mia.backend.llm.prompts import default_chat_template

from mia.backend.llm.classes import MiaState
from langgraph.graph import START, StateGraph


def run_rag(query: str, vector_store: Chroma, top_k: int = 5, chat_history=[]):
    chat_llm = ChatOpenAI(verbose=True, temperature=0)

    stuff_documents_chain = create_stuff_documents_chain(
        chat_llm, default_chat_template
    )

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    history_aware_retriever = create_history_aware_retriever(
        llm=chat_llm,
        retriever=vector_store.as_retriever(
            search_type="similarity", search_kwargs={"k": top_k}
        ),
        prompt=rephrase_prompt
    )

    rag_chain = create_retrieval_chain(
        retriever=history_aware_retriever,
        combine_docs_chain=stuff_documents_chain,
    )
    result = rag_chain.invoke(input={"input": query, "chat_history": chat_history})

    new_result = {
        "query": result["input"],
        "result": result["answer"],
        "source_documents": result["context"],
    }
    return new_result


def add_sources_to_answer(answer, sources, metadata_only=False):
    # Concate the sources to the answer in a readable format
    if metadata_only:
        sources = [source.metadata for source in sources]
    sources = [f"Source: {source}" for source in sources]
    return f"{answer}\n\n{' '.join(sources)}"







if __name__ == "__main__":
    load_dotenv()
    vector_store = initialize_chroma_vector_store()

