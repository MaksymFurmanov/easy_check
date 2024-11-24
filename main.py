import os
import json
from flask import Flask, request, render_template_string, session
from flask_session import Session
from openai import OpenAI
from PyPDF2 import PdfReader
import easyocr

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = "super_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'  # Використовуємо файлову систему для сесій
Session(app)  # Ініціалізація Flask-Session
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

os.environ[
    'OPENAI_API_KEY'] = ''

# Initialize OpenAI client with your API key
client = OpenAI()

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
        .history {
            margin-top: 20px;
            padding: 10px;
            background: #f9f9f9;
            border-radius: 4px;
        }
        .history .message {
            margin-bottom: 10px;
        }
        .history .user {
            color: #007BFF;
            font-weight: bold;
        }
        .history .assistant {
            color: #28A745;
            font-weight: bold;
        }
        .history .file {
            color: #FF9900;
            font-weight: bold;
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

        {% if history %}
        <div class="history">
            <h3>Conversation History:</h3>
            {% for message in history %}
            <div class="message">
                {% if message.role == 'user' %}
                <div class="user">User:</div>
                <div>{{ message.content }}</div>
                {% elif message.role == 'assistant' %}
                <div class="assistant">Assistant:</div>
                <div>{{ message.content }}</div>
                {% elif message.role == 'file' %}
                <div class="file">File Uploaded:</div>
                <div>{{ message.content }}</div>
                {% endif %}
            </div>
            {% endfor %}
        </div>
        {% endif %}

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
    if "history" not in session:
        session["history"] = [{"role": "system", "content": "You are a helpful assistant."}]

    response = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        files = request.files.getlist("files")
        combined_prompt = prompt

        # Handle multiple uploaded files
        for file in files:
            if file:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(file_path)
                try:
                    if file.filename.endswith(".pdf"):
                        file_content = extract_text_from_pdf(file_path)
                        combined_prompt += f"\n\nPDF Extracted Text ({file.filename}): {file_content}"
                        session["history"].append({"role": "file", "content": f"PDF Extracted Text: {file_content}"})
                    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
                        file_content = extract_text_from_image(file_path)
                        combined_prompt += f"\n\nImage Extracted Text ({file.filename}): {file_content}"
                        session["history"].append({"role": "file", "content": f"Image Extracted Text: {file_content}"})
                    else:
                        combined_prompt += f"\n\nFile ({file.filename}) uploaded but not processed."
                        session["history"].append(
                            {"role": "file", "content": f"File {file.filename} uploaded but not processed."})
                except Exception as e:
                    session["history"].append(
                        {"role": "file", "content": f"Error processing file {file.filename}: {str(e)}"})

        if combined_prompt:
            session["history"].append({"role": "user", "content": combined_prompt})
            try:
                chat_completion = client.chat.completions.create(
                    messages=session["history"],
                    model="chatgpt-4o-latest",
                )
                assistant_response = chat_completion.choices[0].message.content
                session["history"].append({"role": "assistant", "content": assistant_response})
                session.modified = True
                response = assistant_response
            except Exception as e:
                response = f"Error: {str(e)}"

    return render_template_string(HTML_TEMPLATE, response=response, history=session.get("history", []))


if __name__ == "__main__":
    app.run(debug=True)
