# Import necessary libraries
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
import os
import pytesseract
from pdf2image import convert_from_path

# Initialize the LLM model
llm = Ollama(model="llama3.1")

# Set up directories if they don't exist
os.makedirs('files', exist_ok=True)

# Set up Streamlit application
st.title("Resume Screening with Llama3")

# Upload a PDF file for resume
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Text area for job description
job_description = st.text_area("Enter the job description:")

# Text area for user prompt
user_prompt = st.text_area("Enter your prompt for resume screening:")

if st.button("Generate Analysis"):
    if uploaded_file is not None and job_description and user_prompt:
        # Save the uploaded PDF file
        file_path = os.path.join('files', uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Load the PDF file
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Initialize text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=200,
            length_function=len
        )

        all_splits = []
        for doc in documents:
            # Check if the document has text
            if hasattr(doc, 'get_text'):
                text = doc.get_text()
                if text:
                    chunks = text_splitter.split_text(text)
                    all_splits.extend(chunks)
                else:
                    st.warning("The document does not contain text.")
            else:
                # If no text, attempt OCR
                st.warning("No text found, attempting OCR...")
                images = convert_from_path(file_path)
                for image in images:
                    text = pytesseract.image_to_string(image)
                    if text:
                        chunks = text_splitter.split_text(text)
                        all_splits.extend(chunks)
                    else:
                        st.warning("OCR failed to extract text from the document.")

        responses = []
        for chunk in all_splits:
            # Create prompt for each chunk
            resume_content = chunk
            full_prompt = f"""
            You are a professional HR assistant. Your task is to evaluate resumes based on the provided job description.

            Job Description: {job_description}
            Resume Content: {resume_content}

            User: {user_prompt}
            HR Assistant:
            """

            # Generate response using LLM for each chunk
            with st.spinner("Generating response for chunk..."):
                response = llm.stream(full_prompt, stop=['<|eot_id|>'])
                responses.append(response)

        # Aggregate responses
        st.write("### Analysis Result:")
        for response in responses:
            st.write(response)

    else:
        st.warning("Please upload a PDF file, enter the job description, and provide a prompt.")