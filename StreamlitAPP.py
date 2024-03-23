import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.mcqgenerator import generate_evaluate_chain

# loading json file
with open('/home/pjlinux/projects/mcqgen/response.json', "r") as file:
    RESPONSE_JSON = json.load(file)

# Creating a title for the app
st.title("MCQ Generator with LangChain :parrot::chains:")

# Creat a form
with st.form("user_input"):
    # File uploader
    uploaded_file = st.file_uploader("Choose a pdf or txt file")

    # Input fields
    mcq_count = st.number_input("Number of MCQs", min_value=3, max_value=10)
    subject = st.text_input("Subject", max_chars=20)
    tone = st.text_input("Complexity Level of Questions",
                         max_chars=20,
                         placeholder="simple, moderate, complex"
                         )

    
    # Create a submit button
    button = st.form_submit_button(label='Create a Quiz')

    # Check if the button is clicked and all the fields are filled

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating the quiz..."):
            # Read the file
            try:
                text = read_file(uploaded_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
                    # st.write(response)
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"Error in generating the quiz: {e}")
            
            else:
                # Print token usage
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost (USD): ${cb.total_cost}")
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data=get_table_data(quiz)
                        if table_data is not None:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1
                            st.table(df)
            
                            # Display the review in a text box as well
                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                else:
                    st.write(response)
if "df" in locals():
    # Add a download button
    st.download_button("Download", df.to_csv(), file_name="quiz.csv", mime="text/csv")