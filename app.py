import streamlit as st

from ui.sidebar import render_sidebar
from ui.chat import render_chat
from ui.summary_tab import render_summary
from ui.settings import render_settings
from backend.summary import generate_summary
from backend.download_chat import export_chat
from backend.audio import generate_audio

from backend.pdf_handler import load_pdfs
from backend.rag_pipeline import (
    split_documents,
    create_vector_store,
    load_vector_store,
    get_retriever,
    ask_question,
)

st.set_page_config(
    page_title="PDF Insight Assistant",
    page_icon="📚",
    layout="wide",
)

# ---------------- Session State ----------------

if "language" not in st.session_state:
    st.session_state.language = "English"

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "summary" not in st.session_state:
    st.session_state.summary = ""

st.title("🧠 PDF Insight Assistant")
uploaded_files, process_button, clear_chat = render_sidebar()

if process_button:
    if uploaded_files:
        with st.spinner("Processing PDFs..."):
            documents = load_pdfs(uploaded_files)
            st.session_state.documents = documents

            chunks = split_documents(documents)
            st.session_state.chunks = chunks

            create_vector_store(chunks)
            vector_store = load_vector_store()
            st.session_state.retriever = get_retriever(vector_store)
            
            # Reset summary on new document load
            st.session_state.summary = ""
            st.session_state.messages = []

        st.success("PDFs processed successfully!")
    else:
        st.warning("Please upload at least one PDF.")

if clear_chat:
    st.session_state.messages = []
    st.success("Chat cleared!")

# Default settings
if "language" not in st.session_state:
    st.session_state.language = "English"

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📄 Summary", "⚙ Settings"])

with tab1:

    question, ask_button = render_chat()

    if ask_button and question:
        if st.session_state.retriever is None:
            st.warning("Please process PDFs first.")
        else:
            with st.spinner("Searching relevant pages...Generating answer..."):
                answer, docs = ask_question(question, st.session_state.retriever)

            st.session_state.messages.append(
                {
                    "question": question,
                    "answer": answer,
                    "docs": docs,
                }
            )

    for i, chat in enumerate(st.session_state.messages):

    # ---------------- User ----------------

        st.chat_message("user").write(
            chat["question"]
        )

    # ---------------- Assistant ----------------

        with st.chat_message("assistant"):

            st.write(chat["answer"])

        # ---------------- Source Citation ----------------

            pages = []

            if "docs" in chat:

                for doc in chat["docs"]:

                    if "page" in doc.metadata:

                        page = doc.metadata["page"] + 1

                        if page not in pages:
                            pages.append(page)

            pages.sort()

            if pages:

                st.caption(
                    "📄 Source Pages: "
                    + ", ".join(map(str, pages))
                )

        # ---------------- Audio ----------------

            if st.button(
                "🔊 Listen",
                key=f"listen_{i}"
            ):

                with st.spinner("Generating Audio..."):

                    audio_file = generate_audio(
                        chat["answer"],
                        st.session_state.language
                    )

                st.audio(audio_file)

with tab2:
    summary_button = render_summary()

    if summary_button:
        if not st.session_state.chunks:
            st.warning("Please process PDFs first.")
        else:
            with st.spinner("Generating document summary..."):
                st.session_state.summary = generate_summary(st.session_state.chunks)
            st.success("Summary Generated!")

    if st.session_state.summary:
        st.markdown(st.session_state.summary)

with tab3:

    language, download_chat = render_settings()
    st.session_state.language = language

    st.divider()

    st.subheader("💾 Export Chat")

    if st.session_state.messages:

        chat_text = export_chat(
            st.session_state.messages
        )

        st.download_button(
            label="⬇ Download Chat History",
            data=chat_text,
            file_name="Chat_History.txt",
            mime="text/plain",
            use_container_width=True,
        )

    else:

        st.info("Start a conversation to enable chat download.")