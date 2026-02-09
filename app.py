import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template


#PDF Text Extraction
def extract_text_from_pdfs(pdf_files):
    combined_text = ""
    for file in pdf_files:
        reader = PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                combined_text += page_text
    return combined_text


#Text Segmentation 
def split_into_chunks(text_data):
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return splitter.split_text(text_data)


#Vector Database Creation
def build_vector_database(chunks):
    embedder = OpenAIEmbeddings()
    vector_db = FAISS.from_texts(texts=chunks, embedding=embedder)
    return vector_db


# Conversation Setup 
def create_chat_chain(vector_db):
    model = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    chat_chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=vector_db.as_retriever(),
        memory=memory
    )
    return chat_chain


#Handling User Interaction
def display_chat_response(user_input):
    response = st.session_state.chat_engine({'question': user_input})
    st.session_state.chat_log = response['chat_history']

    for index, msg in enumerate(st.session_state.chat_log):
        template = user_template if index % 2 == 0 else bot_template
        st.write(template.replace("{{MSG}}", msg.content), unsafe_allow_html=True)


#Streamlit 
def main():
    load_dotenv()
    st.set_page_config(page_title="PDF AI Assistant", page_icon="📚")
    st.write(css, unsafe_allow_html=True)

    if "chat_engine" not in st.session_state:
        st.session_state.chat_engine = None
    if "chat_log" not in st.session_state:
        st.session_state.chat_log = None

    st.header("Chat with Multiple PDFs")
    user_input = st.text_input("Ask something about your documents:")

    if user_input:
        display_chat_response(user_input)

    with st.sidebar:
        st.subheader("Upload Your PDFs")
        pdf_files = st.file_uploader(
            "Select your PDF files and click 'Start Processing'",
            accept_multiple_files=True
        )

        if st.button("Start Processing"):
            with st.spinner("Extracting and indexing your documents..."):
                # Step 1: Extract text
                text_data = extract_text_from_pdfs(pdf_files)

                # Step 2: Create chunks
                chunks = split_into_chunks(text_data)

                # Step 3: Build vector database
                vector_db = build_vector_database(chunks)

                # Step 4: Initialize chat engine
                st.session_state.chat_engine = create_chat_chain(vector_db)


if __name__ == "__main__":
    main()
