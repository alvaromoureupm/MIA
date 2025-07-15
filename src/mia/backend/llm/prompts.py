from langchain_core.prompts import ChatPromptTemplate

default_chat_template = ChatPromptTemplate([
    ("system", """Answer any use questions based solely on the context below:
    <context>
    {context}
    </context>
    """),
    ("placeholder", "{conversation}"),
    ("human", "{input}")
])