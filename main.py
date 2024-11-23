# import os
# import json
# from flask import Flask, request, render_template_string
# from openai import OpenAI
# from PyPDF2 import PdfReader
# from PIL import Image
# import pytesseract
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#
# # Initialize OpenAI client with your API key
# client = OpenAI(
#     api_key="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")
#
# # HTML template for user interaction
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>GPT Query Interface</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             margin: 0;
#             padding: 20px;
#             background-color: #f9f9f9;
#         }
#         .container {
#             max-width: 600px;
#             margin: 0 auto;
#             background: #fff;
#             padding: 20px;
#             border-radius: 8px;
#             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
#         }
#         textarea, input[type="file"] {
#             width: 100%;
#             margin-bottom: 10px;
#             padding: 10px;
#             font-size: 16px;
#             border-radius: 4px;
#             border: 1px solid #ccc;
#         }
#         button {
#             padding: 10px 20px;
#             font-size: 16px;
#             color: #fff;
#             background-color: #007BFF;
#             border: none;
#             border-radius: 4px;
#             cursor: pointer;
#         }
#         button:hover {
#             background-color: #0056b3;
#         }
#         .response {
#             margin-top: 20px;
#             padding: 10px;
#             background: #f1f1f1;
#             border-radius: 4px;
#             font-size: 16px;
#         }
#         .response pre {
#             white-space: pre-wrap;
#             font-family: inherit;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>GPT Query Interface</h1>
#         <form method="POST" action="/" enctype="multipart/form-data">
#             <label for="prompt">Enter your query:</label>
#             <textarea id="prompt" name="prompt" placeholder="Type your question here..."></textarea>
#             <label for="file">Upload a file (optional):</label>
#             <input type="file" id="file" name="file">
#             <button type="submit">Submit</button>
#         </form>
#         {% if response %}
#         <div class="response">
#             <h3>Response:</h3>
#             <pre>{{ response }}</pre>
#         </div>
#         {% endif %}
#     </div>
# </body>
# </html>
# """
#
# def extract_text_from_pdf(file_path):
#     """Extracts text from a PDF file."""
#     try:
#         reader = PdfReader(file_path)
#         return "\n".join(page.extract_text() for page in reader.pages)
#     except Exception as e:
#         return f"Error reading PDF file: {str(e)}"
#
# def extract_text_from_image(file_path):
#     """Extracts text from an image using OCR."""
#     try:
#         image = Image.open(file_path)
#         return pytesseract.image_to_string(image)
#     except Exception as e:
#         return f"Error reading image file: {str(e)}"
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     response = None
#     if request.method == "POST":
#         prompt = request.form.get("prompt", "")
#         file = request.files.get("file")
#
#         # Handle uploaded file if it exists
#         file_content = None
#         if file:
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
#             try:
#                 if file.filename.endswith(".json"):
#                     with open(file_path, "r") as f:
#                         file_content = json.load(f)
#                     prompt += f"\n\nFile Content: {json.dumps(file_content)}"
#                 elif file.filename.endswith(".pdf"):
#                     file_content = extract_text_from_pdf(file_path)
#                     prompt += f"\n\nExtracted PDF Text: {file_content}"
#                 elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
#                     file_content = extract_text_from_image(file_path)
#                     prompt += f"\n\nExtracted Image Text: {file_content}"
#             except Exception as e:
#                 response = f"Error processing file: {str(e)}"
#
#         if prompt:
#             try:
#                 # Call OpenAI's chat completion endpoint
#                 chat_completion = client.chat.completions.create(
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant."},
#                         {"role": "user", "content": prompt},
#                     ],
#                     model="chatgpt-4o-latest",  # Specify the GPT model
#                     max_tokens=10240,  # Збільшення кількості токенів
#                 )
#                 response = chat_completion.choices[0].message.content
#             except Exception as e:
#                 response = f"Error: {str(e)}"
#
#     return render_template_string(HTML_TEMPLATE, response=response)
#
# if __name__ == "__main__":
#     app.run(debug=True)


# import os
# import json
# from flask import Flask, request, render_template_string
# from openai import OpenAI
# from PyPDF2 import PdfReader
# import easyocr
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'uploads'
# os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
#
# # Initialize OpenAI client with your API key
# client = OpenAI(
#     api_key="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"
# )
#
# # HTML template for user interaction
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>GPT Query Interface</title>
#     <style>
#         body {
#             font-family: Arial, sans-serif;
#             margin: 0;
#             padding: 20px;
#             background-color: #f9f9f9;
#         }
#         .container {
#             max-width: 600px;
#             margin: 0 auto;
#             background: #fff;
#             padding: 20px;
#             border-radius: 8px;
#             box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
#         }
#         textarea, input[type="file"] {
#             width: 100%;
#             margin-bottom: 10px;
#             padding: 10px;
#             font-size: 16px;
#             border-radius: 4px;
#             border: 1px solid #ccc;
#         }
#         button {
#             padding: 10px 20px;
#             font-size: 16px;
#             color: #fff;
#             background-color: #007BFF;
#             border: none;
#             border-radius: 4px;
#             cursor: pointer;
#         }
#         button:hover {
#             background-color: #0056b3;
#         }
#         .response {
#             margin-top: 20px;
#             padding: 10px;
#             background: #f1f1f1;
#             border-radius: 4px;
#             font-size: 16px;
#         }
#         .response pre {
#             white-space: pre-wrap;
#             font-family: inherit;
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <h1>GPT Query Interface</h1>
#         <form method="POST" action="/" enctype="multipart/form-data">
#             <label for="prompt">Enter your query:</label>
#             <textarea id="prompt" name="prompt" placeholder="Type your question here..."></textarea>
#             <label for="file">Upload a file (optional):</label>
#             <input type="file" id="file" name="file">
#             <button type="submit">Submit</button>
#         </form>
#         {% if response %}
#         <div class="response">
#             <h3>Response:</h3>
#             <pre>{{ response }}</pre>
#         </div>
#         {% endif %}
#     </div>
# </body>
# </html>
# """
#
# def extract_text_from_pdf(file_path):
#     """Extracts text from a PDF file."""
#     try:
#         reader = PdfReader(file_path)
#         return "\n".join(page.extract_text() for page in reader.pages)
#     except Exception as e:
#         return f"Error reading PDF file: {str(e)}"
#
# def extract_text_from_image(file_path):
#     """Extracts text from an image using EasyOCR."""
#     try:
#         reader = easyocr.Reader(['en', 'uk'])  # Adjust languages as needed
#         results = reader.readtext(file_path)
#         return "\n".join([result[1] for result in results])
#     except Exception as e:
#         return f"Error reading image file: {str(e)}"
#
# @app.route("/", methods=["GET", "POST"])
# def index():
#     response = None
#     if request.method == "POST":
#         prompt = request.form.get("prompt", "")
#         file = request.files.get("file")
#
#         # Handle uploaded file if it exists
#         file_content = None
#         if file:
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#             file.save(file_path)
#             try:
#                 if file.filename.endswith(".json"):
#                     with open(file_path, "r") as f:
#                         file_content = json.load(f)
#                     prompt += f"\n\nFile Content: {json.dumps(file_content)}"
#                 elif file.filename.endswith(".pdf"):
#                     file_content = extract_text_from_pdf(file_path)
#                     prompt += f"\n\nExtracted PDF Text: {file_content}"
#                 elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
#                     file_content = extract_text_from_image(file_path)
#                     prompt += f"\n\nExtracted Image Text: {file_content}"
#             except Exception as e:
#                 response = f"Error processing file: {str(e)}"
#
#         if prompt:
#             try:
#                 # Call OpenAI's chat completion endpoint
#                 chat_completion = client.chat.completions.create(
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant."},
#                         {"role": "user", "content": prompt},
#                     ],
#                     model="chatgpt-4o-latest",  # Specify the GPT model
#                     max_tokens=1024,
#                 )
#                 response = chat_completion.choices[0].message.content
#             except Exception as e:
#                 response = f"Error: {str(e)}"
#
#     return render_template_string(HTML_TEMPLATE, response=response)
#
# if __name__ == "__main__":
#     app.run(debug=True)


import os
import json
from flask import Flask, request, render_template_string
from openai import OpenAI
from PyPDF2 import PdfReader
import easyocr

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize OpenAI client with your API key
client = OpenAI(
    api_key="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"
)

# HTML template with enhanced drag-and-drop for multiple files
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GPT Query Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        textarea {
            width: 100%;
            margin-bottom: 10px;
            padding: 10px;
            font-size: 16px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        .drop-zone {
            width: 100%;
            padding: 20px;
            border: 2px dashed #007BFF;
            border-radius: 4px;
            text-align: center;
            color: #007BFF;
            cursor: pointer;
            margin-bottom: 10px;
        }
        .drop-zone.dragover {
            background-color: #e6f7ff;
        }
        input[type="file"] {
            display: none;
        }
        .file-list {
            margin: 10px 0;
            list-style: none;
            padding: 0;
        }
        .file-list li {
            background: #f1f1f1;
            margin: 5px 0;
            padding: 8px;
            border-radius: 4px;
            font-size: 14px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007BFF;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .response {
            margin-top: 20px;
            padding: 10px;
            background: #f1f1f1;
            border-radius: 4px;
            font-size: 16px;
        }
        .response pre {
            white-space: pre-wrap;
            font-family: inherit;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GPT Query Interface</h1>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="prompt">Enter your query:</label>
            <textarea id="prompt" name="prompt" placeholder="Type your question here..."></textarea>
            <div class="drop-zone" id="drop-zone">Drag and drop files here, or click to upload</div>
            <input type="file" id="files" name="files" multiple>
            <ul class="file-list" id="file-list"></ul>
            <button type="submit">Submit</button>
        </form>
        {% if response %}
        <div class="response">
            <h3>Response:</h3>
            <pre>{{ response }}</pre>
        </div>
        {% endif %}
    </div>
    <script>
        const dropZone = document.getElementById('drop-zone');
        const fileInput = document.getElementById('files');
        const fileList = document.getElementById('file-list');

        dropZone.addEventListener('click', () => fileInput.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            const files = e.dataTransfer.files;
            fileInput.files = files;
            updateFileList(files);
        });

        fileInput.addEventListener('change', () => {
            updateFileList(fileInput.files);
        });

        function updateFileList(files) {
            fileList.innerHTML = '';
            for (const file of files) {
                const listItem = document.createElement('li');
                listItem.textContent = `${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
                fileList.appendChild(listItem);
            }
        }
    </script>
</body>
</html>
"""

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() for page in reader.pages)
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def extract_text_from_image(file_path):
    """Extracts text from an image using EasyOCR."""
    try:
        reader = easyocr.Reader(['en', 'uk'])  # Adjust languages as needed
        results = reader.readtext(file_path)
        return "\n".join([result[1] for result in results])
    except Exception as e:
        return f"Error reading image file: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        files = request.files.getlist("files")

        # Handle multiple uploaded files
        for file in files:
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                try:
                    if file.filename.endswith(".json"):
                        with open(file_path, "r") as f:
                            file_content = json.load(f)
                        prompt += f"\n\nFile Content ({file.filename}): {json.dumps(file_content)}"
                    elif file.filename.endswith(".pdf"):
                        file_content = extract_text_from_pdf(file_path)
                        prompt += f"\n\nExtracted PDF Text ({file.filename}): {file_content}"
                    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                        file_content = extract_text_from_image(file_path)
                        prompt += f"\n\nExtracted Image Text ({file.filename}): {file_content}"
                except Exception as e:
                    response = f"Error processing file {file.filename}: {str(e)}"

        if prompt:
            try:
                # Call OpenAI's chat completion endpoint
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                    model="chatgpt-4o-latest",  # Specify the GPT model
                    max_tokens=1024,
                )
                response = chat_completion.choices[0].message.content
            except Exception as e:
                response = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response)

if __name__ == "__main__":
    app.run(debug=True)
