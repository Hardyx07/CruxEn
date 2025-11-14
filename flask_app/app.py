from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

from prompt_optimizer import PromptOptimizationSystem

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["*"]}})
prompt_system = PromptOptimizationSystem()

api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/use-cases', methods=['GET'])
def get_use_cases():
    """Return list of all available use cases from the taxonomy"""
    try:
        cases = prompt_system.list_available_use_cases()
        return jsonify(cases)
    except Exception as e:
        app.logger.exception('Failed to fetch use cases: %s', e)
        return jsonify({'error': 'Failed to fetch use cases'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    prompt = data.get('prompt')
    explicit_use_case = data.get('use_case')
    include_meta = bool(data.get('include_meta', False))

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    if not explicit_use_case:
        return jsonify({'error': 'use_case is required'}), 400

    try:
        opt_result = prompt_system.process(prompt, explicit_use_case=explicit_use_case)
    except Exception as optimization_error:
        app.logger.exception('Prompt optimization failed: %s', optimization_error)
        return jsonify({'error': 'Prompt optimization failed'}), 500

    # Build context for LLM to improve the prompt
    frameworks_str = ', '.join(opt_result['frameworks'])
    role_template = opt_result['use_case']['role'] or 'Expert'
    
    system_message = f"""You are a prompt engineering specialist. 
Your task is to improve and optimize user prompts based on the following framework and context.

Framework: {frameworks_str}
Role/Context: {role_template}
Use Case: {opt_result['use_case']['subcategory']} ({opt_result['use_case']['description']})

Take the user's raw prompt and rewrite it to be more systematic, structured, and result-oriented using the specified framework.
Return ONLY the optimized prompt, nothing else."""

    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "openai/gpt-oss-120b",
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            llm_optimized_prompt = result['choices'][0]['message']['content']
            
            response_body = {
                'optimized_prompt': llm_optimized_prompt
            }
            return jsonify(response_body)
        else:
            return jsonify({'error': f'Groq API error: {response.status_code}', 'details': response.text}), response.status_code
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Groq API request timed out'}), 504
    except Exception as e:
        app.logger.exception('Groq API call failed: %s', e)
        return jsonify({'error': f'Groq API call failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
