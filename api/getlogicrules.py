from openai import OpenAI
import json
import os

# Initialize OpenAI API
client = OpenAI(
    api_key=os.environ["OPENAITELEKOM_API_KEY"]
)
def save_to_json(data, filename="rules_output.json"):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def generate_logic_rules(input_json):
    # Parse JSON input
    label = input_json['label']
    regex = input_json['regex']
    document_metadata = input_json['document_metadata']

    # Create prompt for GPT-4
    prompt = f"""
    Given the document metadata: {document_metadata}, 
    and the regex pattern for the label '{label}': {regex},
    generate 1-3 logic rules in natural language for possible values of the label '{label}'.
    Do not give any text aside of this 1-3 rules delimited using "|".
    """
    try:
        # Call OpenAI's chat completion endpoint
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a document management specialist."},
                {"role": "user", "content": prompt},
            ],
            model="gpt-4o-mini",  # Specify the GPT model
            max_tokens=150,
        )
        response = chat_completion.choices[0].message.content
    except Exception as e:
        response = f"Error: {str(e)}"
    # Extract logic rules from response
    print(f"Logic rules:\n{response}")

    logic_rules = response.strip().split('|')

    return logic_rules


def get_logic_rules(input_json):
    # Call the function to generate logic rules
    rules = generate_logic_rules(input_json)
    output_json = {
        "label": input_json['label'],
        "criteria_1": rules[0].strip() if len(rules) > 0 else "",
        "criteria_2": rules[1].strip() if len(rules) > 1 else "",
        "criteria_3": rules[2].strip() if len(rules) > 2 else ""
    }
  #  save_to_json(output_json)
    # Output the generated logic rules
  #  print(f"Logic rules for {input_json['label']}: {rules}")
    return rules
