
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

import os
import getpass

# Prompt user to enter their OpenAI API key securely
api_key = getpass.getpass(prompt="Enter your OpenAI API key: ")

# Set the environment variable
os.environ["OPENAI_API_KEY"] = api_key




from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

# Read the prompt from a file and truncate if necessary
prompt_file_content = open('pdf_text', 'r').read()
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

# Define a function to query the language model
def query_llm(question): 
    try:
        response = llm_chain.invoke({'question': question})
        print(response)
    except Exception as e:
        print("Error:", e)

# Run an interactive loop
while True:
    user_input = input()
    if user_input.strip().lower() == "good bye":
        print("Ending the discussion. Good bye!")
        break
    query_llm(user_input)

