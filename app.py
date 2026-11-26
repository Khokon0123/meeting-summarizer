import streamlit as st

from summarizer import summarize_text, extract_action_items, extract_attendees
from exporter import make_pdf, make_docx, make_txt

st.set_page_config(
    page_title="Meeting Summarizer",
    page_icon="📋",
    layout="centered"
)

st.title("📋 Meeting Notes Summarizer")
st.caption("Paste your meeting notes and get an instant AI summary.")
st.divider()


@st.cache_resource
def load_model():
    from summarizer import summarizer
    return summarizer


load_model()

input_method = st.radio(
    "Choose input method:",
    ["Paste text", "Upload .txt file"]
)

meeting_text = ""

if input_method == "Paste text":
    meeting_text = st.text_area(
        "Paste your meeting notes here:",
        height=300,
        placeholder="Paste your meeting notes here..."
    )
else:
    uploaded_file = st.file_uploader(
        "Upload your meeting notes",
        type=["txt"]
    )
    if uploaded_file:
        meeting_text = uploaded_file.read().decode("utf-8")
        st.success(f"File uploaded: {uploaded_file.name}")
        with st.expander("View original text"):
            st.text(meeting_text)

meeting_title = st.text_input("Meeting title (used in the downloaded file):", value="Meeting Summary")

if st.button("Summarize Meeting", type="primary"):
    if not meeting_text.strip():
        st.warning("Please enter some meeting notes first!")
    else:
        with st.spinner("Analyzing meeting notes..."):
            st.session_state["result"] = {
                "title": meeting_title.strip() or "Meeting Summary",
                "summary": summarize_text(meeting_text),
                "action_items": extract_action_items(meeting_text),
                "attendees": extract_attendees(meeting_text),
            }

result = st.session_state.get("result")

if result:
    st.divider()

    st.subheader("📝 Executive Summary")
    st.write(result["summary"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Action Items")
        if result["action_items"]:
            for item in result["action_items"]:
                st.markdown(f"- {item}")
        else:
            st.caption("No action items detected")

    with col2:
        st.subheader("👥 Attendees")
        if result["attendees"]:
            for person in result["attendees"]:
                st.markdown(f"- {person}")
        else:
            st.caption("No attendees detected")

    st.divider()
    st.subheader("⬇️ Download")

    args = (
        result["title"],
        result["summary"],
        result["action_items"],
        result["attendees"],
    )

    dl1, dl2, dl3 = st.columns(3)
    with dl1:
        st.download_button(
            "PDF",
            data=make_pdf(*args),
            file_name="meeting_summary.pdf",
            mime="application/pdf",
        )
    with dl2:
        st.download_button(
            "Word / Google Docs",
            data=make_docx(*args),
            file_name="meeting_summary.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
    with dl3:
        st.download_button(
            "Text",
            data=make_txt(*args),
            file_name="meeting_summary.txt",
            mime="text/plain",
        )

    st.caption(
        "To open in Google Docs: upload the .docx file to Google Drive, "
        "right-click it, and choose Open with > Google Docs."
    )
