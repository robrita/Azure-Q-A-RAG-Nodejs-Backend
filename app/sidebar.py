import streamlit as st


# display the sidebar
def show_sidebar():
    st.subheader("💡Info", anchor=False)
    st.write(
        "This is a Streamlit app for **Q&A Evaluator with RAG** in Nodejs backend api powered by Azure OpenAI."
    )

    st.subheader("⚙️Settings", anchor=False)

    with st.container(border=True):
        appKey = st.text_input(
            "Access Key:",
            placeholder="8cb78***************",
            type="password",
        )

    st.subheader("🛠Technology Stack", anchor=False)
    st.write("Python, Nodejs, Streamlit, Azure OpenAI, Azure AI Search")
    st.write(
        "Check out the repo here: [Q&A RAG Nodejs Backend](https://github.com/robrita/Azure-Q-A-RAG-Nodejs-Backend)"
    )

    return appKey
