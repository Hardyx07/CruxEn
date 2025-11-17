# 🚀 Prompt Optimization Framework Guide v2.0

## Overview

The new Context-Aware Prompt Optimization System features **7 streamlined frameworks** that intelligently enhance user prompts for maximum effectiveness. Each framework is designed to handle specific types of tasks with specialized optimization patterns.

---

## 🎯 The 7 Core Frameworks

### 1. **Reasoning & Problem-Solving** 
**ID:** `reasoning_problem_solving`

**Best For:**
- Complex multi-step problems
- Logical reasoning tasks
- Decision-making scenarios
- Strategic analysis
- Cause-effect analysis
- Comparative evaluation

**Triggers:**
- Questions with "should I", "how do I"
- Words like "solve", "decide", "choose", "analyze"
- Problem-solving contexts
- Decision comparisons

**Example Inputs:**
- "Should I quit my job to start a business?"
- "Help me decide between option A and B"
- "What's the best approach to solve this issue?"

**Role Personas:** Strategic Consultant, Problem-Solving Expert, Decision Analyst

---

### 2. **Research & Exploration**
**ID:** `research_exploration`

**Best For:**
- Research tasks
- Topic deep-dives
- Literature reviews
- Market research
- Trend analysis
- Information synthesis

**Triggers:**
- "research", "explore", "investigate", "find out"
- "tell me about", "what is", "overview"
- "latest trends", "insights", "data"

**Example Inputs:**
- "Research the impact of AI on healthcare"
- "What are the latest trends in renewable energy?"
- "Give me an overview of quantum computing"

**Role Personas:** Research Analyst, Subject Matter Expert, Knowledge Synthesizer

---

### 3. **Instruction, Learning & Explanation**
**ID:** `instruction_learning`

**Best For:**
- Teaching tasks
- Step-by-step guides
- Concept explanations
- Tutorials
- Educational content
- Learning materials

**Triggers:**
- "how to", "teach", "explain", "show me"
- "guide", "tutorial", "walk through"
- "eli5", "simple terms", "beginner"

**Example Inputs:**
- "Teach me how to code in Python"
- "Explain quantum physics in simple terms"
- "Show me how to bake a cake step by step"

**Role Personas:** Expert Educator, Patient Teacher, Tutorial Creator

---

### 4. **Coding & Technical**
**ID:** `coding_technical`

**Best For:**
- Code writing
- Debugging
- Algorithm design
- Technical documentation
- API development
- System architecture

**Triggers:**
- "code", "program", "function", "algorithm"
- "debug", "fix", "error", "bug"
- "implement", "build", "create"
- Programming language names

**Example Inputs:**
- "Write a Python function to sort an array"
- "Debug this JavaScript code"
- "Create a REST API in Node.js"

**Role Personas:** Senior Software Engineer, Full-Stack Developer, System Architect

---

### 5. **Creative & Ideation**
**ID:** `creative_ideation`

**Best For:**
- Brainstorming sessions
- Creative writing
- Idea generation
- Concept development
- Innovation tasks
- Artistic projects

**Triggers:**
- "brainstorm", "ideas", "creative"
- "imagine", "invent", "design"
- "story", "poem", "lyrics", "novel"

**Example Inputs:**
- "Brainstorm ideas for a sci-fi novel"
- "Write a poem about the ocean"
- "Generate creative marketing campaign ideas"

**Role Personas:** Creative Director, Innovation Consultant, Creative Writer

---

### 6. **Writing & Communication**
**ID:** `writing_communication`

**Best For:**
- Email writing
- Blog posts
- Professional documents
- Social media content
- Presentations
- Communication tasks

**Triggers:**
- "write", "draft", "compose"
- "email", "letter", "message", "blog"
- "article", "post", "content", "copy"

**Example Inputs:**
- "Write a professional email to my boss"
- "Draft a blog post about productivity tips"
- "Create an engaging social media caption"

**Role Personas:** Professional Writer, Communications Specialist, Content Creator

---

### 7. **Optimization, Review & Improvement**
**ID:** `optimization_review`

**Best For:**
- Code review
- Text improvement
- Quality assessment
- Performance optimization
- Feedback generation
- Refinement tasks

**Triggers:**
- "improve", "optimize", "enhance", "refine"
- "review", "feedback", "critique"
- "make better", "suggestions"

**Example Inputs:**
- "Review and improve this code"
- "Give me feedback on this essay"
- "Optimize this SQL query for performance"

**Role Personas:** Quality Assurance Expert, Optimization Specialist, Performance Coach

---

## 🔧 How to Use

### Automatic Detection (Recommended)

```python
from prompt_optimizer import PromptOptimizationSystem

system = PromptOptimizationSystem()

# System automatically detects the best framework
result = system.process("How do I learn Python programming?")

print(result['framework']['name'])  # "Instruction, Learning & Explanation"
print(result['optimized_prompt'])
```

### Explicit Framework Selection

```python
# Force a specific framework
result = system.process(
    "Generate some ideas", 
    explicit_framework="creative_ideation"
)
```

### Get All Available Frameworks

```python
frameworks = system.list_available_frameworks()

for fw in frameworks:
    print(f"{fw['name']}: {fw['description']}")
```

---

## 📊 Understanding Results

Each optimization returns:

- **original_input**: Your original prompt
- **optimized_prompt**: Enhanced version with framework patterns
- **framework**: Details about the selected framework
  - `id`: Framework identifier
  - `name`: Human-readable name
  - `description`: What it's designed for
  - `role`: The expert persona applied
- **confidence**: How confident the system is (0-1)
- **reasoning**: Why this framework was chosen
- **quality_metrics**: 
  - `original`: Quality score of input (0-1)
  - `optimized`: Quality score of output (0-1)
  - `improvement`: Difference between them
  - `overall_score`: Final quality rating

---

## 🎨 Framework Selection Logic

The system uses sophisticated pattern matching:

1. **Keyword Matching (40% weight)**: Scans for framework-specific trigger words
2. **Pattern Matching (60% weight)**: Uses regex to identify common phrase patterns
3. **Confidence Scoring**: Normalizes scores to determine best fit
4. **Smart Fallback**: Defaults to Reasoning & Problem-Solving if uncertain

---

## 💡 Best Practices

### For Best Results:

1. **Be Clear**: Use specific language about what you want
2. **Use Keywords**: Include words that signal your intent
3. **Trust Auto-Detection**: The system is highly accurate
4. **Use Explicit Selection**: Override when you know exactly what you need

### Framework Selection Tips:

- **Need to make a decision?** → Reasoning & Problem-Solving
- **Want to learn something?** → Instruction, Learning & Explanation
- **Need to write code?** → Coding & Technical
- **Need creative ideas?** → Creative & Ideation
- **Writing content?** → Writing & Communication
- **Need improvement?** → Optimization, Review & Improvement
- **Researching a topic?** → Research & Exploration

---

## 🚨 Edge Cases Handled

The system intelligently handles:

- **Empty inputs**: Validation errors with clear messages
- **Ambiguous requests**: Smart defaulting to most likely framework
- **Mixed intents**: Prioritizes primary detected pattern
- **Unknown frameworks**: Graceful fallback with helpful suggestions
- **Multiple keywords**: Weighted scoring to find best match

---

## 🔄 Migration from Old System

### Old System (10+ categories):
```python
result = system.process(input, explicit_use_case="blog_article")
```

### New System (7 frameworks):
```python
result = system.process(input)  # Auto-detects
# OR
result = system.process(input, explicit_framework="writing_communication")
```

### Benefits:
- ✅ Simpler API (7 vs 10+ categories)
- ✅ Better auto-detection
- ✅ More accurate results
- ✅ Clearer framework purposes
- ✅ Handles more edge cases

---

## 📈 Quality Scoring

The system evaluates prompts on:

1. **Length Adequacy** (25%): Sufficient detail and context
2. **Structure** (25%): Organization with headers, lists, sections
3. **Specificity** (25%): Clear instructions and requirements
4. **Instructions** (25%): Explicit guidance for the AI

Score Range: 0.0 - 1.0 (higher is better)

---

## 🎓 Example Transformations

### Before Optimization:
```
"write code to sort array"
```

### After Optimization:
```
You are a Senior Software Engineer. Provide technical solution with best practices.

**Technical Request:** write code to sort array

**Development Approach:**
1. **Requirements** - Clarify specifications and constraints
2. **Design** - Plan architecture and approach
3. **Implementation** - Provide clean, efficient, well-documented code
4. **Explanation** - Explain how the solution works and why
5. **Testing** - Suggest test cases and edge cases to consider
6. **Optimization** - Highlight performance considerations and best practices

Follow language conventions, use proper naming, include comments, and ensure robustness.

---
**Quality Standards:**
- Ensure accuracy and factual correctness
- Use clear, appropriate language for the context
- Provide complete, well-structured responses
- Include relevant examples or evidence
- Address edge cases and potential issues
- Maintain consistency throughout
```

**Result**: More comprehensive, structured, and likely to get high-quality code!

---

## 🔗 API Integration

See `app.py` for Flask API endpoints:
- `POST /api/optimize` - Optimize a prompt
- `GET /api/frameworks` - List all frameworks
- `GET /api/frameworks/<id>` - Get framework details

---

## 📞 Support

For issues or questions about framework selection, check:
1. This guide
2. Example outputs in `prompt_optimizer.py`
3. Test the system with: `python prompt_optimizer.py`

---

**Version**: 2.0  
**Last Updated**: November 2025  
**Maintained by**: CruxEn Team
