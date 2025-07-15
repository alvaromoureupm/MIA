import streamlit as st
from typing import Set

from mia.backend.llm.rag import run_rag
from mia.backend.chroma.chroma import initialize_chroma_vector_store
from streamlit_chat import message


st.set_page_config(page_title="Asistente Legal Bot", page_icon="⚖️")

# Add custom CSS for a blue gradient background
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(to right, #1e3c72, #2a5298);
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #f0f0f5;
        color: black;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a title and a logo
st.image("src/mia/frontend/assets/mia_logo_2.jpg", width=100)
st.title("⚖️ Asistente Legal Bot")
st.subheader("Tu asesor legal basado en IA")

prompt = st.text_input(
    "📝 Introduzca su consulta legal:", placeholder="Escribe tu pregunta aquí..."
)

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_answers_history" not in st.session_state:
    st.session_state["chat_answers_history"] = []

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Default args
vector_store = initialize_chroma_vector_store()

if prompt:
    with st.spinner("🔍 Analizando tu consulta..."):
        generated_response = run_rag(
            query=prompt,
            vector_store=vector_store,
            top_k=10,
            chat_history=st.session_state["chat_history"],
        )

        formatted_response = generated_response["result"]

        sources = set([doc.metadata["id"] for doc in generated_response["source_documents"]])

        formatted_response += "\n\nFuentes:\n" + "\n".join(
            sources
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answers_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("bot", generated_response["result"]))

if st.session_state["chat_answers_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answers_history"],
        st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True, avatar_style="initials", seed="Usuario")
        message(generated_response, avatar_style="initials", seed="Bot")

# Add a footer
st.markdown("---")
st.markdown("© 2024 MIA Asistente Legal. Todos los derechos reservados.")
