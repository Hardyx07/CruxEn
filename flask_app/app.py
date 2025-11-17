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

@app.route('/frameworks', methods=['GET'])
def get_frameworks():
    """Return list of all available frameworks"""
    try:
        frameworks = prompt_system.list_available_frameworks()
        return jsonify(frameworks)
    except Exception as e:
        app.logger.exception('Failed to fetch frameworks: %s', e)
        return jsonify({'error': 'Failed to fetch frameworks'}), 500

@app.route('/frameworks/<framework_id>', methods=['GET'])
def get_framework_details(framework_id):
    """Get details about a specific framework"""
    try:
        framework = prompt_system.get_framework_by_id(framework_id)
        if framework:
            return jsonify(framework)
        else:
            return jsonify({'error': f'Framework "{framework_id}" not found'}), 404
    except Exception as e:
        app.logger.exception('Failed to fetch framework details: %s', e)
        return jsonify({'error': 'Failed to fetch framework details'}), 500

@app.route('/optimize', methods=['POST'])
def optimize_prompt():
    """
    Optimize a user prompt using the framework system.
    Can auto-detect or use explicit framework.
    
    Request body:
    {
        "prompt": "user prompt text",
        "framework": "optional framework ID" // e.g., "coding_technical"
    }
    """
    data = request.get_json() or {}
    prompt = data.get('prompt')
    explicit_framework = data.get('framework')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        opt_result = prompt_system.process(prompt, explicit_framework=explicit_framework)
        return jsonify(opt_result)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        app.logger.exception('Prompt optimization failed: %s', e)
        return jsonify({'error': 'Prompt optimization failed'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    """
    Enhanced chat endpoint with LLM integration.
    Uses framework optimization + Groq API for final output.
    
    Request body:
    {
        "prompt": "user prompt text",
        "framework": "optional framework ID",
        "include_meta": false // include framework metadata in response
    }
    """
    data = request.get_json() or {}
    prompt = data.get('prompt')
    explicit_framework = data.get('framework')
    include_meta = bool(data.get('include_meta', False))

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        opt_result = prompt_system.process(prompt, explicit_framework=explicit_framework)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as optimization_error:
        app.logger.exception('Prompt optimization failed: %s', optimization_error)
        return jsonify({'error': 'Prompt optimization failed'}), 500

    # Build context for LLM to improve the prompt
    framework_name = opt_result['framework']['name']
    framework_desc = opt_result['framework']['description']
    role_template = opt_result['framework']['role']
    
    system_message = f"""You are a prompt engineering specialist. 
Your task is to improve and optimize user prompts based on the following framework and context.

Framework: {framework_name}
Description: {framework_desc}
Role/Context: {role_template}
Confidence: {opt_result['confidence']:.0%}

Take the user's raw prompt and rewrite it to be more systematic, structured, and result-oriented using the specified framework principles.
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
                'optimized_prompt': llm_optimized_prompt,
            }
            
            # Include metadata if requested
            if include_meta:
                response_body['metadata'] = {
                    'framework': opt_result['framework'],
                    'confidence': opt_result['confidence'],
                    'reasoning': opt_result['reasoning'],
                    'quality_metrics': opt_result['quality_metrics']
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
