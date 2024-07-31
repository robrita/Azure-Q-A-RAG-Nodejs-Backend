import streamlit as st


# display the sidebar
def show_sidebar():
    st.subheader("💡Info", anchor=False)
    st.write(
        "This is a Streamlit app for **Q&A Evaluator with RAG** with Nodejs backend api powered by Azure OpenAI."
    )

    st.subheader("🛠Technology Stack", anchor=False)
    st.write("Python, Streamlit, Azure OpenAI, Azure AI")
    st.write(
        "Check out the repo here: [Q&A RAG Nodejs Backend](https://github.com/robrita/Azure-Q-A-RAG-Nodejs-Backend)"
    )
