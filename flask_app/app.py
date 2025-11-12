from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-oss-20b",  
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return jsonify({'response': result['choices'][0]['message']['content']})
        else:
            return jsonify({'error': response.text}), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
