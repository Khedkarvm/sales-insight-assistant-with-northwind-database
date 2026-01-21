"""import streamlit as st
from nl_to_sql import run_question

st.set_page_config(page_title="NL-to-SQL Chat", layout="centered")

st.title("NL-to-SQL Chat Interface")


# History Section 
st.markdown("---")  
st.header("Query History")


if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Enter your question:")

if st.button("Submit"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Generating SQL and querying database"):
            df = run_question(question)

        st.session_state.history.append({"question": question, "df": df})

        if "error" in df.columns:
            st.error(df.iloc[0]["error"])
        else:
            st.success("Query executed successfully")
            st.dataframe(df)


if st.session_state.history:

    for i, entry in enumerate(reversed(st.session_state.history), 1):
        st.subheader(f"Question {len(st.session_state.history)-i+1}")
        st.markdown(f"**Query:** {entry['question']}")
        df = entry["df"]
        if "error" in df.columns:
            st.error(df.iloc[0]["error"])
        else:
            st.dataframe(df)
else:
    st.info("No previous queries yet. Your past questions will appear here.")
   
"""
import streamlit as st
from nl_to_sql import run_question

st.set_page_config(page_title="NL-to-SQL Chat", layout="wide")
st.title("Natural Language to SQL")

if "history" not in st.session_state:
    st.session_state.history = []

if "selected_index" not in st.session_state:
    st.session_state.selected_index = None


# Sidebar
st.sidebar.header("Query History")

if st.session_state.history:
    for idx, item in enumerate(st.session_state.history):
        if st.sidebar.button(item["question"], key=f"hist_{idx}"):
            st.session_state.selected_index = idx
else:
    st.sidebar.info("No queries yet")


question = st.text_input("Ask a Northwind question (NL → SQL):")

if st.button("Submit"):
    if question.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Generating SQL and querying database..."):
            df, sql = run_question(question)   

        # Current query
        st.markdown("### Current Query")
        st.markdown(f"**Question:** {question}")

        st.markdown("#### Generated SQL")
        st.code(sql, language="sql")

        if "error" in df.columns:
            st.warning(df.iloc[0]["error"])
        else:
            st.success("Query executed successfully")
            st.dataframe(df)

        # Save history
        st.session_state.history.append({
            "question": question,
            "df": df,
            "sql": sql
        })

        st.session_state.selected_index = len(st.session_state.history) - 1


# Selected history item
if st.session_state.selected_index is not None:
    item = st.session_state.history[st.session_state.selected_index]

    st.markdown("---")
    st.header("Selected Query")

    st.markdown(f"**Question:** {item['question']}")
    st.markdown("#### Generated SQL")
    st.code(item["sql"], language="sql")

    if "error" in item["df"].columns:
        st.warning(item["df"].iloc[0]["error"])
    else:
        st.dataframe(item["df"])
