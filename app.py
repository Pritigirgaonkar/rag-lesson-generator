import streamlit as st
import json
from workflow.graph import run_workflow
from memory.memory_manager import get_memory_summary
from config import MOCK_MODE

st.set_page_config(page_title="Lesson Quality Agent", page_icon="📚", layout="wide")
st.title("📚 Self-Evaluating Lesson Content Generator")
st.caption("Generate → Evaluate → Improve → Approve")

with st.sidebar:
    st.subheader("Run settings")
    topic = st.text_input("Lesson topic", "Introduction to RAG")
    max_retries = st.slider("Maximum retries", 0, 2, 2)
    inject_error = st.checkbox("Inject a deliberate error into the first draft", value=False)
    st.info("Offline mock mode is active." if MOCK_MODE else "Live model mode is active.")

if st.button("Run lesson agent", type="primary"):
    with st.spinner("The agent is generating and evaluating the lesson..."):
        result = run_workflow(topic, inject_error, max_retries)
    st.session_state["last_result"] = result

result = st.session_state.get("last_result")
if result:
    status = result.get("status")
    if status == "approved":
        st.success(f"Approved after {result.get('retry_count', 0) + 1} attempt(s).")
        st.markdown(result["lesson"])
        st.download_button("Download approved lesson", result["lesson"], file_name="final_lesson.md")
    else:
        st.error("The lesson did not pass within the retry limit.")
    st.subheader("Evaluation")
    ev = result.get("evaluation", {})
    st.write(ev.get("summary", "No evaluation summary"))
    for check in ev.get("checks", []):
        with st.expander(f"{'✅' if check['passed'] else '❌'} {check['check_id']} — {check['dimension']}"):
            st.write(check["evidence"])
            if check.get("fix"):
                st.write("Suggested fix:", check["fix"])
    st.subheader("Rejection log")
    st.json(result.get("rejection_log", []))

st.divider()
st.subheader("Persistent run memory")
st.caption("Recent run history is stored in a local SQLite database.")
st.json(get_memory_summary())
