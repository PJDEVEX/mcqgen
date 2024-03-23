import os
import PyPDF2
import json
import traceback as tb

def read_file(file):
    """
    Read the pdf file and return the text
    """
    if file.name.endswith('.pdf'):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e:
            raise Exception(f"Error in reading the file: {e}")

    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise Exception(
            "File type not supported only pdf and txt files are supported"
            )
    
def get_table_data(quiz_str):
    """
    Get the table data from the text
    """
    try:
        # convert the quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data=[]

        # Iterate over the quiz_dict and get the table data
        for key, value in quiz_dict.items():
            mcq = value.get("mcq")
            options = " | ".join(
                [
                    f"{option} : {option_value}" for option, option_value in value["options"].items()
                    ]
                )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "choices": options, "correct": correct})
        
        return quiz_table_data
    
    except Exception as e:
        tb.print_exception(type(e), e, e.__traceback__)
        return False
    
