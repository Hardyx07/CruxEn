# 📡 Flask API Documentation v2.0

## Base URL
```
http://localhost:5000
```

---

## Endpoints

### 1. Health Check
**GET** `/`

Simple health check endpoint.

**Response:**
```
Hello, World!
```

---

### 2. List All Frameworks
**GET** `/frameworks`

Get a list of all available prompt optimization frameworks.

**Response:** `200 OK`
```json
[
  {
    "id": "reasoning_problem_solving",
    "name": "Reasoning & Problem-Solving",
    "description": "Logical step-by-step thinking, complex problem solving, decision analysis",
    "ideal_for": [
      "Complex multi-step problems",
      "Logical reasoning tasks",
      "Decision-making scenarios",
      "Strategic analysis",
      "Cause-effect analysis",
      "Comparative evaluation"
    ],
    "example_inputs": [
      "Should I quit my job to start a business?",
      "How do I solve this complex math problem?",
      "Help me decide between option A and B"
    ],
    "role_personas": [
      "Strategic Consultant",
      "Problem-Solving Expert",
      "Decision Analyst",
      "Critical Thinking Coach"
    ]
  },
  // ... 6 more frameworks
]
```

**Error Response:** `500 Internal Server Error`
```json
{
  "error": "Failed to fetch frameworks"
}
```

---

### 3. Get Framework Details
**GET** `/frameworks/<framework_id>`

Get detailed information about a specific framework.

**Parameters:**
- `framework_id` (path parameter): Framework identifier
  - Valid values: `reasoning_problem_solving`, `research_exploration`, `instruction_learning`, `coding_technical`, `creative_ideation`, `writing_communication`, `optimization_review`

**Example:**
```
GET /frameworks/coding_technical
```

**Response:** `200 OK`
```json
{
  "id": "coding_technical",
  "name": "Coding & Technical",
  "description": "Code generation, debugging, technical architecture, algorithm design",
  "ideal_for": [
    "Code writing",
    "Debugging",
    "Algorithm design",
    "Technical documentation",
    "API development",
    "System architecture"
  ],
  "trigger_keywords": [
    "code", "program", "function", "class", "algorithm", 
    "debug", "fix", "error", "bug", "implement"
    // ... more keywords (limited to 20 for readability)
  ],
  "example_inputs": [
    "Write a Python function to sort an array",
    "Debug this JavaScript code",
    "Create a REST API in Node.js"
  ],
  "role_personas": [
    "Senior Software Engineer",
    "Full-Stack Developer",
    "System Architect",
    "DevOps Expert"
  ]
}
```

**Error Response:** `404 Not Found`
```json
{
  "error": "Framework \"invalid_framework\" not found"
}
```

---

### 4. Optimize Prompt (No LLM)
**POST** `/optimize`

Optimize a user prompt using the framework system. This endpoint returns the raw optimized prompt without LLM processing.

**Request Body:**
```json
{
  "prompt": "Write code to sort numbers",
  "framework": "coding_technical"  // Optional - omit for auto-detection
}
```

**Parameters:**
- `prompt` (string, required): The user's original prompt
- `framework` (string, optional): Explicit framework ID to use. If omitted, the system will auto-detect the best framework.

**Response:** `200 OK`
```json
{
  "original_input": "Write code to sort numbers",
  "optimized_prompt": "You are a Senior Software Engineer. Provide technical solution with best practices.\n\n**Technical Request:** Write code to sort numbers\n\n**Development Approach:**\n1. **Requirements** - Clarify specifications and constraints\n2. **Design** - Plan architecture and approach\n...",
  "framework": {
    "id": "coding_technical",
    "name": "Coding & Technical",
    "description": "Code generation, debugging, technical architecture, algorithm design",
    "role": "Senior Software Engineer"
  },
  "confidence": 0.95,
  "reasoning": "Selected Coding & Technical based on detected patterns in your request.",
  "quality_metrics": {
    "original": {
      "clarity": 0.45,
      "specificity": 0.30,
      "structure": 0.20,
      "completeness": 0.35,
      "overall": 0.33
    },
    "optimized": {
      "clarity": 0.85,
      "specificity": 0.78,
      "structure": 0.90,
      "completeness": 0.82,
      "overall": 0.84
    },
    "improvement": 0.51,
    "overall_score": 0.85
  }
}
```

**Error Responses:**

`400 Bad Request` - Missing prompt
```json
{
  "error": "No prompt provided"
}
```

`400 Bad Request` - Invalid input
```json
{
  "error": "user_input cannot be empty"
}
```

`500 Internal Server Error`
```json
{
  "error": "Prompt optimization failed"
}
```

---

### 5. Chat (With LLM Enhancement)
**POST** `/chat`

Enhanced chat endpoint that optimizes the prompt AND sends it to Groq API for final LLM-enhanced output.

**Request Body:**
```json
{
  "prompt": "Write code to sort numbers",
  "framework": "coding_technical",  // Optional
  "include_meta": true              // Optional - include framework metadata
}
```

**Parameters:**
- `prompt` (string, required): The user's original prompt
- `framework` (string, optional): Explicit framework ID. Auto-detects if omitted.
- `include_meta` (boolean, optional): Include framework metadata in response. Default: `false`

**Response:** `200 OK` (without metadata)
```json
{
  "optimized_prompt": "Here's an efficient Python implementation of a sorting algorithm:\n\n```python\ndef sort_numbers(arr):\n    \"\"\"\n    Sort a list of numbers using Python's built-in Timsort algorithm.\n    \n    Args:\n        arr: List of numbers to sort\n    \n    Returns:\n        Sorted list in ascending order\n    \"\"\"\n    return sorted(arr)\n\n# Example usage\nnumbers = [64, 34, 25, 12, 22, 11, 90]\nsorted_numbers = sort_numbers(numbers)\nprint(sorted_numbers)  # Output: [11, 12, 22, 25, 34, 64, 90]\n```\n\nThis implementation..."
}
```

**Response:** `200 OK` (with metadata)
```json
{
  "optimized_prompt": "Here's an efficient Python implementation...",
  "metadata": {
    "framework": {
      "id": "coding_technical",
      "name": "Coding & Technical",
      "description": "Code generation, debugging, technical architecture, algorithm design",
      "role": "Senior Software Engineer"
    },
    "confidence": 0.95,
    "reasoning": "Selected Coding & Technical based on detected patterns in your request.",
    "quality_metrics": {
      "original": { /* ... */ },
      "optimized": { /* ... */ },
      "improvement": 0.51,
      "overall_score": 0.85
    }
  }
}
```

**Error Responses:**

`400 Bad Request`
```json
{
  "error": "No prompt provided"
}
```

`504 Gateway Timeout`
```json
{
  "error": "Groq API request timed out"
}
```

`500 Internal Server Error` (Groq API failure)
```json
{
  "error": "Groq API error: 500",
  "details": "Internal server error details..."
}
```

---

## Framework IDs Reference

| Framework ID | Name | Use For |
|-------------|------|---------|
| `reasoning_problem_solving` | Reasoning & Problem-Solving | Decision-making, complex problems |
| `research_exploration` | Research & Exploration | Research, topic exploration |
| `instruction_learning` | Instruction, Learning & Explanation | Teaching, tutorials, explanations |
| `coding_technical` | Coding & Technical | Code generation, debugging |
| `creative_ideation` | Creative & Ideation | Brainstorming, creative writing |
| `writing_communication` | Writing & Communication | Emails, blogs, professional writing |
| `optimization_review` | Optimization, Review & Improvement | Code review, text improvement |

---

## Quality Metrics Explanation

### Individual Scores (0.0 - 1.0)

- **clarity**: How clear and understandable the prompt is
- **specificity**: How specific and detailed the instructions are
- **structure**: How well-organized the prompt is (sections, lists, etc.)
- **completeness**: How comprehensive the prompt is (context, goals, constraints)
- **overall**: Average of all metrics

### Overall Score (0.0 - 1.0)

Combined quality assessment based on:
- Length adequacy (25%)
- Structure (25%)
- Specificity (25%)
- Instructions (25%)

---

## Auto-Detection vs Explicit Selection

### Auto-Detection (Recommended)
```json
{
  "prompt": "How do I learn Python?"
}
```
System automatically detects: `instruction_learning` framework

### Explicit Selection
```json
{
  "prompt": "How do I learn Python?",
  "framework": "coding_technical"
}
```
Forces the use of `coding_technical` framework with 100% confidence

---

## Example cURL Requests

### Get All Frameworks
```bash
curl http://localhost:5000/frameworks
```

### Optimize Prompt (Auto-detect)
```bash
curl -X POST http://localhost:5000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Help me decide between two job offers"
  }'
```

### Optimize Prompt (Explicit Framework)
```bash
curl -X POST http://localhost:5000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Help me decide between two job offers",
    "framework": "reasoning_problem_solving"
  }'
```

### Chat with LLM Enhancement
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a function to calculate factorial",
    "framework": "coding_technical",
    "include_meta": true
  }'
```

---

## Error Handling

All endpoints follow standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (invalid framework ID)
- `500` - Internal Server Error
- `504` - Gateway Timeout (LLM API timeout)

Error responses always include an `error` field with a descriptive message.

---

## Rate Limiting

Currently no rate limiting is implemented. Consider adding rate limiting for production use.

---

## CORS

CORS is enabled for all origins (`*`). Adjust in production for security.

---

## Environment Variables

Required:
- `GROQ_API_KEY`: API key for Groq LLM service

---

## Running the Server

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export GROQ_API_KEY="your_api_key_here"

# Run the server
python app.py
```

Server will start on `http://localhost:5000` in debug mode.

---

**Version**: 2.0  
**Last Updated**: November 2025  
**Maintained by**: CruxEn Team
