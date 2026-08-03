
# import streamlit as st


# def render_summary():

#     st.subheader("📄 PDF Summary")

#     summary_button = st.button(
#         "Generate Summary",
#         use_container_width=True,
#     )

#     return summary_button

import streamlit as st


def render_summary():
    st.subheader("📄 Document Summary")
    st.caption(
        "Generate a comprehensive executive summary from your uploaded documents."
    )

    st.info(
        "💡 Click below to extract key insights, main takeaways, and structured overviews.",
        icon="ℹ️",
    )

    summary_button = st.button(
        "✨ Generate Summary",
        type="primary",
        use_container_width=True,
    )

    return summary_button