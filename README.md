# CruxEn

### Intelligent Prompt Optimization Engine
**Elevating Human-AI Interaction through Framework-Based Enhancement**

---

### 🚀 **The Concept**
**CruxEn** (Crux Enhancer) is a full-stack AI application designed to bridge the gap between user intent and LLM execution. By leveraging specialized optimization frameworks and high-performance inference (Groq), it automatically refines raw inputs into structured, high-fidelity prompts that unlock the full potential of Large Language Models.

### ⚡ **Key Features**
*   **Framework-Driven Optimization**: Intelligently detects user intent and applies specific prompt engineering frameworks to maximize output quality.
*   **High-Performance AI Layer**: Integrated with **Groq API** (Llama-3-70b) for sub-second, near-real-time prompt enhancement.
*   **Enterprise-Ready Backend**: A robust Flask API featuring rate limiting, CORS security, structured logging, and input sanitization.
*   **Immersive UX**: A highly interactive, starry-themed frontend built with Next.js, featuring smooth animations and a responsive design.

### 🛠️ **Tech Stack**

| Domain | Technologies |
| :--- | :--- |
| **Frontend** | **Next.js 14**, TypeScript, Tailwind CSS, Framer Motion |
| **Backend** | **Python (Flask)**, Flask-Limiter, Flask-CORS |
| **AI / ML** | **Groq API**, Llama-3 Models, Prompt Engineering Frameworks |
| **DevOps** | Vercel (Frontend), Environment-based Configuration (12-Factor App) |

### 🏗️ **System Architecture**
CruxEn operates on a decoupled client-server architecture:
1.  **Client**: A React-based SPA that captures user input and provides real-time visual feedback.
2.  **API Gateway**: A Python Flask server that validates requests, manages rate limits, and routes traffic.
3.  **Optimization Engine**: The core logic that processes the prompt against selected frameworks before sending it to the Inference Engine.

### 💡 **Project Impact**
*   **Efficiency**: Reduces the "trial and error" phase of prompting, saving users significant time.
*   **Accessibility**: Makes advanced prompt engineering techniques accessible to non-technical users.
*   **Scalability**: Designed with production standards (logging, error handling, modular code) ready for real-world deployment.

---

### 🔧 **Quick Start**

**Backend Setup**
```bash
cd flask_app
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
flask run
```

**Frontend Setup**
```bash
npm install
npm run dev
```

---

*Developed by [Hardyx07](https://github.com/Hardyx07)*
