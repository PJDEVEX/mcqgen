import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv

from src.mcqgenerator.logger import logging

# import packages from LangChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import  SequentialChain


# Load the .env file
load_dotenv()

# Access the API key from the environment variable
APIKEY_OPENAI=os.getenv("APIKEY_OPENAI")

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
quize_chain = LLMChain(
    llm=llm,
    prompt_template=quiz_generation_prompt,
    output_key="quiz",
    verbose=True)

# Template 2 for the prompt
TEMPLATE2="""
Your are an expert English grammerian. Give a multiple choice quiz for {subject} students. \
    you need to evaluate the complexity of the question and give a complete analysis of the quiz. 
    Only use at max 50 words for the complexity analysis. \
    If the questions are not in par with the student's cognitive and analytical abilities of the student, \
    Update the questions which needs to be changed and change the tone such that it perfectly fits the student's cognitive and analytical abilities. \
    Quiz_MCQs: 
    {quiz}

    check from an expert English writer of the above quiz:
    """

# Question evaluation prompt
quiz_evaluation_prompt = PromptTemplate(
    input_variables=["subject", "quiz"],
    template=TEMPLATE2
)

# Quiz evaluation chain
review_chain = LLMChain(llm=llm,
                        prompt=quiz_evaluation_prompt,
                        output_key="review",
                        verbose=True)

# Sequential chain for quiz generation and evaluation
generate_evaluate_chain = SequentialChain(  
    chains=[quize_chain, review_chain],
    input_variables=["text", "number", "subject", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)
