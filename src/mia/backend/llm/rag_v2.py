from dotenv import load_dotenv
from mia.backend.llm.classes import MiaState
from langgraph.graph import START, StateGraph

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from mia.backend.chroma.chroma import initialize_chroma_vector_store
from mia.backend.llm.prompts import default_chat_template


def retrieve(state: MiaState):
    vector_store: Chroma = initialize_chroma_vector_store()
    retrieved_docs = vector_store.similarity_search_with_relevance_scores(
        state["question"], k=5
    )
    return {
        "context": retrieved_docs,
    }


def generate(state: MiaState, config: dict):
    chat_llm = ChatOpenAI(model="gpt-4o-mini",temperature=0)
    if state.get("context") is not None:
        stuffed_documents = "\n\n".join([doc.page_content for doc in state["context"]])
    else:
        stuffed_documents = "No context available"
    messages = default_chat_template.invoke(
        {"input": state["question"], "context": stuffed_documents}
    )
    response = chat_llm.invoke(messages)
    return {
        "answer": response.content,
    }


graph_builder = StateGraph(MiaState)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "generate")

graph = graph_builder.compile()

