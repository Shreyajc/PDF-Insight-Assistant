
# import streamlit as st


# def render_sidebar():
#     """
#     Render the sidebar.
#     """

#     st.sidebar.title("📂 PDF Upload")

#     uploaded_files = st.sidebar.file_uploader(
#         "Upload one or more PDF files",
#         type=["pdf"],
#         accept_multiple_files=True,
#     )

#     process_button = st.sidebar.button(
#         "⚙ Process PDFs",
#         use_container_width=True,
#     )

#     st.sidebar.divider()

#     clear_chat = st.sidebar.button(
#         "🗑 Clear Chat",
#         use_container_width=True,
#     )

#     st.sidebar.divider()

#     st.sidebar.info(
#         """
#         **Supported Features**

#         ✅ Multiple PDFs

#         ✅ Semantic Search

#         ✅ AI Chat

#         ✅ PDF Summary

#         ✅ English Audio

#         ✅ Hindi Audio

#         ✅ Download Chat
#         """
#     )

#     return uploaded_files, process_button, clear_chat

import streamlit as st


def render_sidebar():
    """Render the enhanced sidebar UI."""

    st.sidebar.title("📂 Document Hub")

    with st.sidebar.container():
        uploaded_files = st.sidebar.file_uploader(
            "Upload PDF files",
            type=["pdf"],
            accept_multiple_files=True,
            help="Select one or more PDF files to index.",
        )

        process_button = st.sidebar.button(
            "⚡ Process PDFs",
            type="primary",
            use_container_width=True,
        )

    st.sidebar.divider()

    clear_chat = st.sidebar.button(
        "🗑️ Clear Chat",
        type="secondary",
        use_container_width=True,
    )

    st.sidebar.divider()

    with st.sidebar.expander("✨ Features & Capabilities", expanded=True):
        st.markdown(
            """
            * 📄 **Multiple PDFs** support
            * 🔍 **Semantic Vector Search**
            * 💬 **Contextual AI Chat**
            * 📝 **Automated PDF Summaries**
            * 🎧 **English & Hindi Audio**
            * 💾 **Exportable Chat Logs**
            """
        )

    return uploaded_files, process_button, clear_chat