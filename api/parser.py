import os
import json
from openai import OpenAI
from PyPDF2 import PdfReader

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.environ["OPENAITELEKOM_API_KEY"])
prompt = f"""
    You are a specialized AI designed to parse data from documents and provide structured output with an additional 
    short description for each field. Your task is to extract all labeled information (e.g., Name, Surname, Address, etc.), 
    match it with its value (if there is one, if none just put empty string as output), and add a concise description of each field based on the context provided in the input data (e.g., 
    Name: John, Description: Name of the individual, Name:..., Description: Name of the individual, etc.). 
    Don’t add anything from yourself, take everything you convert from the user’s request. Remember that field for value of data can be in a form of ........... , __________________ , "",  just empty space etc.
"""
fix_prompt = f"""
    You are a specialized AI designed to fix bad formatted output. You will be given bad formatted input json text that contains pairs label/value.
    You need to format it properly, fix errors in characters and remove or simplify nonmeaningful data or wrong formated data. The output data should
    be json that contains pairs label : data where label is name of field and data value ( can be empty if bad formated or no data ). Example 
    label : name , value : John | label : street_name value : Jedlikova. Also add descriptions for each label/data pairs that is given in input. Result json must contain array of jsons with 
    label : name , value : John , description : This field contains name of landlord. Keep stricted formatted output, do not add anything from yourself. Output data must be in proper format.  
    Save name of labels in source language, replace all diacritic. Output must strictly be json file in format - [
    {{
        "label" : "nazov_sidlo_spravneho_uradu" , 
        "value": "", 
        "description":"Name and address of the relevant administrative body acting as the construction authority."
    }}
] -  add only brackets and no other characters, delim using newline
"""
# Initialize chat history
chat_history = [
    {"role": "system", "content": prompt}
]
def extract_text_from_pdf(file_path):
    """
}Extracts text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        return f"Error: {str(e)}"


def process_pdf_files(file_path):
    """Process PDF files from a directory."""
    response = None
    file_content = extract_text_from_pdf(file_path)
    print("content" + file_content)
    prompt = f"\n\nExtracted PDF Text : {file_content}"

    if prompt.strip():
        try:
           #  Append the new user message to chat history
            chat_history.append({"role": "user", "content": prompt})

         #    Call OpenAI's chat completion endpoint
            chat_completion = client.chat.completions.create(
                messages=chat_history,
                model="chatgpt-4o-latest",  # Specify the GPT model
                max_tokens=1024
            )

            # Extract and save the assistant's response
            assistant_response = chat_completion.choices[0].message.content
            chat_history.append({"role": "assistant", "content": assistant_response})

            # Attempt to convert the assistant's response into JSON
            try:
                json_response = json.loads(assistant_response)
                response = json.dumps(json_response, indent=4)
            except json.JSONDecodeError:
                response = json.dumps({"response": assistant_response}, indent=4)

        except Exception as e:
            response = f"Error: {str(e)}"

    #print(f"Response:\n{response}\n")
    return response
def format_output(unformatted_output):
    try:
        #  Append the new user message to chat history
        chat_history.append({"role": "user", "content": fix_prompt})
        chat_history.append({"role": "user", "content": unformatted_output})

        #    Call OpenAI's chat completion endpoint
        chat_completion = client.chat.completions.create(
            messages=chat_history,
            model="chatgpt-4o-latest",  # Specify the GPT model
            max_tokens=1024
        )

        # Extract and save the assistant's response
        assistant_response = chat_completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": assistant_response})

        # Attempt to convert the assistant's response into JSON
        try:
            json_response = json.loads(assistant_response)
            response = json.dumps(json_response, indent=4)
        except json.JSONDecodeError:
            response = json.dumps({"response": assistant_response}, indent=4)

    except Exception as e:
        response = f"Error: {str(e)}"
    return response
def save_list_to_file(content):
    """Saves a list directly to a file named parser_output.json."""
    try:
        with open("parser_output.json", 'w') as file:
            for item in content:
                file.write(str(item) + '\n')  # Convert each item to a string and write it
        print("File saved as parser_output.json")
    except Exception as e:
        print(f"Error: {str(e)}")

def parse_input(input_pdf_path):
    unformatted_output = process_pdf_files(input_pdf_path)
    formatted_output = format_output(unformatted_output)
    formatted_output_v2 = format_output(formatted_output)
    save_list_to_file(formatted_output_v2.strip().split('\n'))

#if __name__ == "__main__":
#    parse_input("./pdfs/ŽIADOSŤ_O_STAVEBNÉ_POVOLENIE_Ziadost_o_stavebne_povolenie.pdf")
