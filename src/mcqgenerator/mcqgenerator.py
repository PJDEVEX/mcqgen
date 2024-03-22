import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# import packages from LangChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import  SequentialChain
from langchain.callbacks import get_openai_callback

# Load the .env file
load_dotenv()

# Access the API key from the environment variable
os.getenv("APIKEY_OPENAI")

# Initialize ChatopenAI
llm = ChatOpenAI(openai_api_key=APIKEY_OPENAI, model_name="gpt-3.5-turbo",temperature=0.5)

# Template 1 for the prompt
TEMPLATE ="""
text:{text}
You are an expert MCQ maker. Give the above text, it is your job to\
create a quize of {number} multiple choice questions for {subject} in a {tone} tone\
Make sure questions are not repeated and check all question to be confirming to the text as well. \
Make sure to format your resepomse like RESPONSE_JSON below and use it as a guide.  \
Ensure to make {number} MCQs
###RESPONSE_JSON
{response_json}
"""

# Prompt Template for quiz generation
quiz_generation_prompt = PromptTemplate(
    input_variables=["text","number","subject","tone"],
    template=TEMPLATE)

# LLMChain for quiz generation
quiz_generation_chain = LLMChain(
    llm=llm,
    prompt_template=quiz_generation_prompt,
    output_key="quiz",
    verbose=True)

