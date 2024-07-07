# app.py
import streamlit as st
import os
import getpass
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

st.title('OpenAI Language Model Chatbot')

# Setup OpenAI API key securely
api_key = st.text_input("Enter your OpenAI API key:", type="password")

if st.button("Set API Key"):
    os.environ["OPENAI_API_KEY"] = api_key
    st.success("API Key set successfully.")

# Function to query the language model
def query_llm(question):
    try:
        response = llm_chain.invoke({'question': question})
        st.write("Answer:")
        st.write(response)
    except Exception as e:
        st.error(f"Error: {e}")

# Main Streamlit app
if "OPENAI_API_KEY" in os.environ:
    # Read the prompt from a file and truncate if necessary
    prompt_file_content = open('pdf_text', 'r', encoding='utf-8').read()
    max_prompt_length = 3500  # Set a max length for the initial prompt content

    if len(prompt_file_content) > max_prompt_length:
        prompt = prompt_file_content[:max_prompt_length] + "..."
    else:
        prompt = prompt_file_content

    # Define the assistant template
    hotel_assistant_template = prompt + """
    You are the hotel manager of Landon Hotel, named "Mr. Landon".
    Your expertise is exclusively in providing information and advice about anything related to Landon Hotel.
    This includes any general Landon Hotel related queries.
    You do not provide information outside of this scope.
    If a question is not about Landon Hotel, respond with, "I can't assist you with that, sorry!"
    Question: {question}
    Answer:
    """

    # Create the prompt template
    hotel_assistant_prompt_template = PromptTemplate(
        input_variables=["question"],
        template=hotel_assistant_template
    )

    # Initialize the language model
    llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0)

    # Combine the prompt template and the language model
    llm_chain = hotel_assistant_prompt_template | llm

    # Streamlit interaction loop
    user_input = st.text_area("Enter your question:")
    if st.button("Ask"):
        query_llm(user_input.strip())

else:
    st.warning("Please enter your OpenAI API key to proceed.")
