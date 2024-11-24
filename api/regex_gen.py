from openai import OpenAI
import json
import os

# Initialize OpenAI API
client = OpenAI(
    api_key="----"
)

import json


def read_json_file():
    file_path = "document.json"

    # Считываем содержимое файла в переменную
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Пример использования


def save_to_json(data, filename="rules_output.json"):
    with open(filename, 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

def generate_logic_rules(json_elem):
    # Create prompt for GPT-4

    prompt = rf"""
        I will provide element{json_elem} in the following format:\

        {{
            "label": "Mesto a dátum podania",
            "Description": "The place and date of submitting the application."
        }}

        Each element includes a "label" and a "Description". The "label" identifies the field, and the "Description" explains what the field represents. Your task is to analyze both the "label" and "Description" to determine the likely format of the data and generate a regular expression to extract the value. Since no actual values are provided, base your regular expression entirely on the information in the "label" and "Description".

        Use the "label" to infer the type of data and the "Description" to confirm or clarify its structure. If necessary, research common data formats online. For example, if the field relates to a date, determine the likely format, such as YYYY-MM-DD. If it mentions a place, consider standard address patterns. For combined fields, like "place and date," design a regular expression to capture both components.

        Under no circumstances should you use Slovak diacritics in your regular expressions or output. Avoid including special Slovak characters such as á, ä, é, í, ó, ú, ľ, š, č, etc., in any part of the result.

        Return the result as text in the format of a JSON element, containing the original "label" and the generated "regex". The output format must look like this:

        {{
            "label": "Mesto a datum podania",
            "regex": "[\\w\\s.,]+ \\d{{4}}-\\d{{2}}-\\d{{2}}"
        }}

        Ensure the response is formatted as a JSON element with no additional text or explanations. Focus on providing accurate and flexible regular expressions based on the given information while strictly avoiding Slovak diacritics.
    """

    try:
        # Call OpenAI's chat completion endpoint
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini",  # Specify the GPT model
            max_tokens=150,
        )
        response = chat_completion.choices[0].message.content
    except Exception as e:
        response = f"Error: {str(e)}"
    # Extract logic rules from response
    # print(f"Logic rules:\n{response}")

    return response


def get_logic_rules(json_elem):
    rules = generate_logic_rules(json_elem)
    # print(f"Logic rules:\n{rules}")
    rules = rules.decode('utf-8') if isinstance(rules, bytes) else rules

    json_element = json.loads(rules)
    save_to_json(json_element)



