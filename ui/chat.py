
# import streamlit as st


# def render_chat():

#     st.subheader("💬 Chat with your PDFs")

#     question = st.text_input(
#         "Ask a question"
#     )

#     ask_button = st.button(
#         "Ask Question",
#         use_container_width=True,
#     )

#     return question, ask_button

import streamlit as st


def render_chat():
    st.subheader("💬 Chat with your PDFs")
    st.caption("Ask questions about the contents of your uploaded documents.")

    with st.container():
        question = st.text_input(
            "Ask a question",
            placeholder="e.g., What are the key findings in section 2?",
            label_visibility="collapsed",
        )

        col1, col2 = st.columns([3, 1])
        with col2:
            ask_button = st.button(
                "💬 Ask Question",
                type="primary",
                use_container_width=True,
            )

    return question, ask_button