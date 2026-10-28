import streamlit as st
from summarizer import summarize_text, extract_action_items, extract_attendees

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

if st.button("Summarize Meeting", type="primary"):
    if not meeting_text.strip():
        st.warning("Please enter some meeting notes first!")
    else:
        with st.spinner("Analyzing meeting notes..."):
            summary = summarize_text(meeting_text)
            action_items = extract_action_items(meeting_text)
            attendees = extract_attendees(meeting_text)

        st.divider()

        st.subheader("📝 Executive Summary")
        st.write(summary)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Action Items")
            if action_items:
                for item in action_items:
                    st.markdown(f"- {item}")
            else:
                st.caption("No action items detected")

        with col2:
            st.subheader("👥 Attendees")
            if attendees:
                for person in attendees:
                    st.markdown(f"- {person}")
            else:
                st.caption("No attendees detected")

        st.divider()
        st.download_button(
            label="Download Summary",
            data=f"SUMMARY\n\n{summary}\n\nACTION ITEMS\n" + "\n".join(f"- {i}" for i in action_items),
            file_name="meeting_summary.txt",
            mime="text/plain"
        )
