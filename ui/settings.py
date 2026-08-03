# import streamlit as st


# def render_settings():

#     st.subheader("⚙ Settings")

#     language = st.selectbox(
#         "Audio Language",
#         [
#             "English",
#             "Hindi",
#         ],
#     )

#     download_chat = st.button(
#         "💾 Download Chat",
#         use_container_width=True,
#     )

#     return language, download_chat

import streamlit as st


def render_settings():
    st.subheader("⚙️ App Settings")
    st.caption("Configure audio playback and manage application session data.")

    st.markdown("##### 🔊 Preferences")
    language = st.selectbox(
        "Audio Language",
        options=["English", "Hindi"],
        help="Select the preferred spoken language for audio outputs.",
    )

    st.markdown("---")
    st.markdown("##### 💾 Data Management")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "Export your current conversation history as a text log."
        )
    with col2:
        download_chat = st.button(
            "💾 Download Chat",
            use_container_width=True,
        )

    return language, download_chat