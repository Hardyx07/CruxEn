"""Context-Aware Prompt Optimization System v2.0
A streamlined 7-framework system for intelligent prompt generation and enhancement.
"""

import re
import os
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from enum import Enum

try:
    import requests  # noqa: F401
    REQUESTS_AVAILABLE = True
except ImportError:  # pragma: no cover - optional dependency warning
    REQUESTS_AVAILABLE = False
    print("\u26a0\ufe0f  Warning: 'requests' library not installed. Groq integration disabled.")
    print("   Install with: pip install requests")


# ==================== ENUMS & DATA STRUCTURES ====================


class Framework(Enum):
    """Streamlined 7 core prompt frameworks."""

    REASONING_PROBLEM_SOLVING = "reasoning_problem_solving"
    RESEARCH_EXPLORATION = "research_exploration"
    INSTRUCTION_LEARNING = "instruction_learning"
    CODING_TECHNICAL = "coding_technical"
    CREATIVE_IDEATION = "creative_ideation"
    WRITING_COMMUNICATION = "writing_communication"
    OPTIMIZATION_REVIEW = "optimization_review"


@dataclass
class FrameworkConfig:
    """Framework configuration with patterns and triggers."""

    framework: Framework
    name: str
    description: str
    ideal_for: List[str]
    trigger_keywords: Set[str]
    trigger_patterns: List[str]
    role_personas: List[str]
    structure_template: str
    example_inputs: List[str]


@dataclass
class OptimizedPrompt:
    """Result of prompt optimization."""

    original_input: str
    detected_framework: Framework
    framework_name: str
    optimized_prompt: str
    confidence_score: float
    reasoning: str
    suggested_role: str
    quality_score: float


# ==================== FRAMEWORK REGISTRY ====================


class FrameworkRegistry:
    """Central registry for all 7 core frameworks with comprehensive pattern matching."""

    def __init__(self) -> None:
        self.frameworks = self._build_frameworks()

    def _build_frameworks(self) -> Dict[Framework, FrameworkConfig]:
        """Build the complete framework registry."""

        return {
            # Framework 1: Reasoning & Problem-Solving
            Framework.REASONING_PROBLEM_SOLVING: FrameworkConfig(
                framework=Framework.REASONING_PROBLEM_SOLVING,
                name="Reasoning & Problem-Solving",
                description="Logical step-by-step thinking, complex problem solving, decision analysis",
                ideal_for=[
                    "Complex multi-step problems",
                    "Logical reasoning tasks",
                    "Decision-making scenarios",
                    "Strategic analysis",
                    "Cause-effect analysis",
                    "Comparative evaluation",
                ],
                trigger_keywords={
                    "solve", "problem", "decide", "choose", "analyze", "reason",
                    "why", "how", "logic", "think", "evaluate", "compare",
                    "should i", "what if", "scenario", "decision", "option",
                    "best way", "figure out", "work through", "break down",
                    "approach", "strategy", "tradeoff", "pros and cons",
                },
                trigger_patterns=[
                    r"how (do|can|should) i",
                    r"what('s| is) the best",
                    r"help me (decide|choose|figure)",
                    r"which (is|would be) better",
                    r"(solve|resolve|fix) (this|the)",
                    r"think through",
                    r"step by step",
                ],
                role_personas=[
                    "Strategic Consultant",
                    "Problem-Solving Expert",
                    "Decision Analyst",
                    "Critical Thinking Coach",
                ],
                structure_template="chain_of_thought",
                example_inputs=[
                    "Should I quit my job to start a business?",
                    "How do I solve this complex math problem?",
                    "Help me decide between option A and B",
                ],
            ),
            # Framework 2: Research & Exploration
            Framework.RESEARCH_EXPLORATION: FrameworkConfig(
                framework=Framework.RESEARCH_EXPLORATION,
                name="Research & Exploration",
                description="Deep research, multi-source synthesis, investigations, insight extraction",
                ideal_for=[
                    "Research tasks",
                    "Topic deep-dives",
                    "Literature reviews",
                    "Market research",
                    "Trend analysis",
                    "Information synthesis",
                ],
                trigger_keywords={
                    "research", "explore", "investigate", "find out", "learn about",
                    "tell me about", "what is", "explain", "overview", "summary",
                    "background", "history", "trends", "insights", "data",
                    "study", "examine", "discover", "uncover", "synthesize",
                    "compare sources", "literature", "findings",
                },
                trigger_patterns=[
                    r"tell me (about|everything)",
                    r"what (is|are|do you know)",
                    r"research on",
                    r"find (out|information)",
                    r"give me (an overview|insights)",
                    r"latest (trends|developments)",
                ],
                role_personas=[
                    "Research Analyst",
                    "Subject Matter Expert",
                    "Knowledge Synthesizer",
                    "Academic Researcher",
                ],
                structure_template="multi_source",
                example_inputs=[
                    "Research the impact of AI on healthcare",
                    "What are the latest trends in renewable energy?",
                    "Give me an overview of quantum computing",
                ],
            ),
            # Framework 3: Instruction, Learning & Explanation
            Framework.INSTRUCTION_LEARNING: FrameworkConfig(
                framework=Framework.INSTRUCTION_LEARNING,
                name="Instruction, Learning & Explanation",
                description="How-to guides, tutorials, teaching complex concepts, step-by-step instructions",
                ideal_for=[
                    "Teaching tasks",
                    "Step-by-step guides",
                    "Concept explanations",
                    "Tutorials",
                    "Educational content",
                    "Learning materials",
                ],
                trigger_keywords={
                    "how to", "teach", "explain", "show me", "guide", "tutorial",
                    "instruct", "demonstrate", "walk through", "learn", "understand",
                    "eli5", "simple terms", "beginner", "introduce", "basics",
                    "fundamentals", "lesson", "course", "training", "educate",
                },
                trigger_patterns=[
                    r"how (to|do i)",
                    r"teach me",
                    r"explain (like|in simple)",
                    r"show me how",
                    r"walk me through",
                    r"step.by.step",
                    r"guide (to|for)",
                ],
                role_personas=[
                    "Expert Educator",
                    "Patient Teacher",
                    "Tutorial Creator",
                    "Learning Facilitator",
                ],
                structure_template="instructional",
                example_inputs=[
                    "Teach me how to code in Python",
                    "Explain quantum physics in simple terms",
                    "Show me how to bake a cake step by step",
                ],
            ),
            # Framework 4: Coding & Technical
            Framework.CODING_TECHNICAL: FrameworkConfig(
                framework=Framework.CODING_TECHNICAL,
                name="Coding & Technical",
                description="Code generation, debugging, technical architecture, algorithm design",
                ideal_for=[
                    "Code writing",
                    "Debugging",
                    "Algorithm design",
                    "Technical documentation",
                    "API development",
                    "System architecture",
                ],
                trigger_keywords={
                    "code", "program", "function", "class", "algorithm", "debug",
                    "fix", "error", "bug", "implement", "build", "create",
                    "develop", "script", "api", "database", "query", "test",
                    "refactor", "optimize", "compile", "syntax", "runtime",
                    "method", "variable", "loop", "array", "object",
                },
                trigger_patterns=[
                    r"write (a|an|the|some) (code|function|class|program)",
                    r"(create|build|implement|generate) (a|an)",
                    r"debug (this|the|my)",
                    r"fix (this|the|my) (code|error|bug)",
                    r"(python|javascript|java|c\+\+|sql)",
                ],
                role_personas=[
                    "Senior Software Engineer",
                    "Full-Stack Developer",
                    "System Architect",
                    "DevOps Expert",
                ],
                structure_template="code_focused",
                example_inputs=[
                    "Write a Python function to sort an array",
                    "Debug this JavaScript code",
                    "Create a REST API in Node.js",
                ],
            ),
            # Framework 5: Creative & Ideation
            Framework.CREATIVE_IDEATION: FrameworkConfig(
                framework=Framework.CREATIVE_IDEATION,
                name="Creative & Ideation",
                description="Brainstorming, idea generation, creative writing, concept creation",
                ideal_for=[
                    "Brainstorming sessions",
                    "Creative writing",
                    "Idea generation",
                    "Concept development",
                    "Innovation tasks",
                    "Artistic projects",
                ],
                trigger_keywords={
                    "brainstorm", "ideas", "creative", "imagine", "invent",
                    "create", "design", "story", "poem", "lyrics", "novel",
                    "fiction", "concept", "innovative", "unique", "original",
                    "artistic", "inspiration", "theme", "plot", "character",
                    "world building", "narrative",
                },
                trigger_patterns=[
                    r"(brainstorm|generate) (ideas|concepts)",
                    r"write a (story|poem|song|script)",
                    r"create (something|a concept)",
                    r"come up with",
                    r"imagine (a|an)",
                    r"creative (ideas|solutions)",
                ],
                role_personas=[
                    "Creative Director",
                    "Innovation Consultant",
                    "Creative Writer",
                    "Brainstorming Facilitator",
                ],
                structure_template="divergent",
                example_inputs=[
                    "Brainstorm ideas for a sci-fi novel",
                    "Write a poem about the ocean",
                    "Generate creative marketing campaign ideas",
                ],
            ),
            # Framework 6: Writing & Communication
            Framework.WRITING_COMMUNICATION: FrameworkConfig(
                framework=Framework.WRITING_COMMUNICATION,
                name="Writing & Communication",
                description="Professional writing, emails, blogs, scripts, messaging, content creation",
                ideal_for=[
                    "Email writing",
                    "Blog posts",
                    "Professional documents",
                    "Social media content",
                    "Presentations",
                    "Communication tasks",
                ],
                trigger_keywords={
                    "write", "draft", "compose", "email", "letter", "message",
                    "blog", "article", "post", "content", "copy", "text",
                    "communicate", "respond", "reply", "announcement",
                    "newsletter", "report", "document", "memo", "press release",
                    "social media", "tweet", "caption", "description",
                },
                trigger_patterns=[
                    r"write (an|a) (email|letter|blog|article)",
                    r"draft (a|an)",
                    r"compose (a|an)",
                    r"help me write",
                    r"create (content|copy)",
                ],
                role_personas=[
                    "Professional Writer",
                    "Communications Specialist",
                    "Content Creator",
                    "Copywriter",
                ],
                structure_template="narrative",
                example_inputs=[
                    "Write a professional email to my boss",
                    "Draft a blog post about productivity tips",
                    "Create an engaging social media caption",
                ],
            ),
            # Framework 7: Optimization, Review & Improvement
            Framework.OPTIMIZATION_REVIEW: FrameworkConfig(
                framework=Framework.OPTIMIZATION_REVIEW,
                name="Optimization, Review & Improvement",
                description="Improving text or code, refining ideas, quality evaluation, feedback",
                ideal_for=[
                    "Code review",
                    "Text improvement",
                    "Quality assessment",
                    "Performance optimization",
                    "Feedback generation",
                    "Refinement tasks",
                ],
                trigger_keywords={
                    "improve", "optimize", "enhance", "refine", "review",
                    "feedback", "critique", "evaluate", "assess", "better",
                    "revise", "polish", "upgrade", "streamline", "fix",
                    "make better", "suggestions", "recommendations",
                    "quality", "efficiency", "performance",
                },
                trigger_patterns=[
                    r"(improve|optimize|enhance|refine) (this|my|the)",
                    r"make (this|it) better",
                    r"review (this|my|the)",
                    r"give (me |)(feedback|suggestions)",
                    r"how can i improve",
                    r"what('s| is) wrong with",
                ],
                role_personas=[
                    "Quality Assurance Expert",
                    "Optimization Specialist",
                    "Performance Coach",
                    "Editorial Reviewer",
                ],
                structure_template="evaluative",
                example_inputs=[
                    "Review and improve this code",
                    "Give me feedback on this essay",
                    "Optimize this SQL query for performance",
                ],
            ),
        }

    def get_all_frameworks(self) -> List[FrameworkConfig]:
        """Get list of all framework configurations."""
        return list(self.frameworks.values())

    def get_framework(self, framework: Framework) -> FrameworkConfig:
        """Get specific framework configuration."""
        return self.frameworks[framework]

# ==================== INTELLIGENT FRAMEWORK DETECTOR ====================


class FrameworkDetector:
    """Intelligently detect the best framework for a given prompt."""

    def __init__(self) -> None:
        self.registry = FrameworkRegistry()

    def detect(self, user_input: str) -> Tuple[Framework, float, str]:
        """
        Detect the most appropriate framework for the user input.
        Returns: (framework, confidence_score, reasoning)
        """
        
        input_lower = user_input.lower()
        scores: Dict[Framework, float] = {}
        
        # Score each framework based on keyword and pattern matching
        for framework_config in self.registry.get_all_frameworks():
            score = 0.0
            matched_keywords: List[str] = []
            matched_patterns: List[str] = []
            
            # Keyword matching (40% weight)
            for keyword in framework_config.trigger_keywords:
                if keyword in input_lower:
                    score += 0.5
                    matched_keywords.append(keyword)
            
            # Pattern matching (60% weight)
            for pattern in framework_config.trigger_patterns:
                if re.search(pattern, input_lower):
                    score += 1.0
                    matched_patterns.append(pattern)
            
            # Normalize score
            max_possible = len(framework_config.trigger_keywords) * 0.5 + len(framework_config.trigger_patterns) * 1.0
            if max_possible > 0:
                scores[framework_config.framework] = min(score / max_possible * 100, 100)
            else:
                scores[framework_config.framework] = 0.0
        
        # Get best match
        if not scores or max(scores.values()) == 0:
            # Default to reasoning framework
            best_framework = Framework.REASONING_PROBLEM_SOLVING
            confidence = 0.5
        else:
            best_framework = max(scores, key=scores.get)  # type: ignore
            confidence = min(scores[best_framework] / 100, 1.0)
        
        # Generate reasoning
        framework_config = self.registry.get_framework(best_framework)
        reasoning = f"Selected {framework_config.name} based on detected patterns in your request."
        
        return best_framework, confidence, reasoning


# ==================== FRAMEWORK APPLIERS ====================


class FrameworkApplier:
    """Apply framework-specific prompt optimization patterns."""

    def __init__(self) -> None:
        self.registry = FrameworkRegistry()

    def apply(self, prompt: str, framework: Framework) -> Tuple[str, str]:
        """
        Apply the framework to the prompt.
        Returns: (optimized_prompt, suggested_role)
        """
        
        config = self.registry.get_framework(framework)
        
        # Select appropriate role persona
        role = config.role_personas[0] if config.role_personas else "Expert Assistant"
        
        # Apply framework-specific template
        if config.structure_template == "chain_of_thought":
            optimized = self._apply_chain_of_thought(prompt, config, role)
        elif config.structure_template == "multi_source":
            optimized = self._apply_multi_source(prompt, config, role)
        elif config.structure_template == "instructional":
            optimized = self._apply_instructional(prompt, config, role)
        elif config.structure_template == "code_focused":
            optimized = self._apply_code_focused(prompt, config, role)
        elif config.structure_template == "divergent":
            optimized = self._apply_divergent(prompt, config, role)
        elif config.structure_template == "narrative":
            optimized = self._apply_narrative(prompt, config, role)
        elif config.structure_template == "evaluative":
            optimized = self._apply_evaluative(prompt, config, role)
        else:
            optimized = self._apply_default(prompt, config, role)
        
        return optimized, role

    def _apply_chain_of_thought(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply chain-of-thought reasoning framework."""
        return f"""You are a {role}. Let's approach this problem systematically.

**Task:** {prompt}

**Approach:**
1. **Analyze** - Break down the problem into key components
2. **Reason** - Think through each part logically, considering all factors
3. **Evaluate** - Weigh different options, pros/cons, and implications
4. **Synthesize** - Combine insights into a comprehensive solution
5. **Validate** - Check reasoning and ensure completeness

Please show your step-by-step reasoning throughout your response."""

    def _apply_multi_source(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply research and exploration framework."""
        return f"""You are a {role}. Conduct a thorough exploration of this topic.

**Research Request:** {prompt}

**Research Framework:**
1. **Overview** - Provide foundational understanding and context
2. **Key Findings** - Present main insights, facts, and discoveries
3. **Analysis** - Examine trends, patterns, and relationships
4. **Multiple Perspectives** - Consider different viewpoints and sources
5. **Synthesis** - Draw connections and derive meaningful conclusions
6. **Implications** - Discuss significance and applications

Provide comprehensive, well-researched information with depth and nuance."""

    def _apply_instructional(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply instruction and learning framework."""
        return f"""You are a {role}. Provide clear, accessible instruction.

**Learning Goal:** {prompt}

**Teaching Approach:**
1. **Introduction** - Set context and explain why this matters
2. **Prerequisites** - Identify what learners need to know first
3. **Step-by-Step Breakdown** - Present information in logical, digestible steps
4. **Examples** - Provide concrete, relatable examples
5. **Practice Tips** - Suggest how to apply and reinforce learning
6. **Common Pitfalls** - Warn about typical mistakes to avoid

Ensure clarity, use analogies where helpful, and adapt to different learning levels."""

    def _apply_code_focused(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply coding and technical framework."""
        return f"""You are a {role}. Provide technical solution with best practices.

**Technical Request:** {prompt}

**Development Approach:**
1. **Requirements** - Clarify specifications and constraints
2. **Design** - Plan architecture and approach
3. **Implementation** - Provide clean, efficient, well-documented code
4. **Explanation** - Explain how the solution works and why
5. **Testing** - Suggest test cases and edge cases to consider
6. **Optimization** - Highlight performance considerations and best practices

Follow language conventions, use proper naming, include comments, and ensure robustness."""

    def _apply_divergent(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply creative ideation framework."""
        return f"""You are a {role}. Let's explore creative possibilities.

**Creative Challenge:** {prompt}

**Ideation Process:**
1. **Expand** - Generate diverse ideas without judgment
2. **Explore** - Push boundaries and think unconventionally
3. **Combine** - Mix concepts in unexpected ways
4. **Refine** - Develop the most promising directions
5. **Present** - Showcase ideas with vivid descriptions

Embrace creativity, think outside the box, provide multiple unique concepts (aim for 5-10), and make each idea distinct and compelling."""

    def _apply_narrative(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply writing and communication framework."""
        return f"""You are a {role}. Craft clear, engaging communication.

**Writing Task:** {prompt}

**Writing Framework:**
1. **Purpose** - Define the goal and intended audience
2. **Structure** - Organize content logically and effectively
3. **Tone** - Match voice to context (professional, casual, persuasive, etc.)
4. **Clarity** - Use precise language and clear expression
5. **Engagement** - Make content compelling and reader-friendly
6. **Polish** - Ensure grammatical correctness and flow

Focus on effective communication that resonates with the intended audience."""

    def _apply_evaluative(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply optimization and review framework."""
        return f"""You are a {role}. Provide comprehensive evaluation and improvement recommendations.

**Review Request:** {prompt}

**Evaluation Framework:**
1. **Assessment** - Analyze current state and identify strengths/weaknesses
2. **Issues** - Pinpoint specific problems, inefficiencies, or areas for improvement
3. **Root Causes** - Understand why issues exist
4. **Recommendations** - Provide concrete, actionable improvement suggestions
5. **Implementation** - Explain how to apply improvements
6. **Expected Outcomes** - Describe benefits of proposed changes

Be constructive, specific, and focus on practical improvements with clear impact."""

    def _apply_default(self, prompt: str, config: FrameworkConfig, role: str) -> str:
        """Apply default framework when no specific template matches."""
        return f"""You are a {role}.

**Task:** {prompt}

Please provide a comprehensive, high-quality response that:
- Addresses all aspects of the request
- Demonstrates expertise and knowledge
- Is well-structured and clear
- Includes relevant examples or details
- Considers edge cases and nuances

Ensure your response is thorough, accurate, and valuable."""


# ==================== PROMPT OPTIMIZER ====================


class PromptOptimizer:
    """Main optimization engine with intelligent framework detection."""

    def __init__(self) -> None:
        self.detector = FrameworkDetector()
        self.applier = FrameworkApplier()
        self.registry = FrameworkRegistry()

    def optimize(self, user_input: str, explicit_framework: Optional[str] = None) -> OptimizedPrompt:
        """
        Optimize user prompt with automatic or explicit framework selection.
        
        Args:
            user_input: The original user prompt
            explicit_framework: Optional framework name (e.g., "coding_technical")
        
        Returns:
            OptimizedPrompt with all optimization details
        """

        if not user_input or not user_input.strip():
            raise ValueError("user_input cannot be empty")

        # Determine framework
        if explicit_framework:
            framework, confidence, reasoning = self._get_explicit_framework(explicit_framework)
        else:
            framework, confidence, reasoning = self.detector.detect(user_input)

        # Apply framework
        optimized_prompt, suggested_role = self.applier.apply(user_input, framework)
        
        # Add quality controls
        optimized_prompt = self._add_quality_controls(optimized_prompt)
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(optimized_prompt)
        
        # Get framework details
        framework_config = self.registry.get_framework(framework)

        return OptimizedPrompt(
            original_input=user_input,
            detected_framework=framework,
            framework_name=framework_config.name,
            optimized_prompt=optimized_prompt,
            confidence_score=confidence,
            reasoning=reasoning,
            suggested_role=suggested_role,
            quality_score=quality_score,
        )

    def _get_explicit_framework(self, framework_name: str) -> Tuple[Framework, float, str]:
        """Get framework from explicit name with validation."""
        
        framework_name = framework_name.lower().strip()
        
        # Try to match framework by value
        for framework in Framework:
            if framework.value == framework_name or framework.name.lower() == framework_name:
                config = self.registry.get_framework(framework)
                reasoning = f"Explicitly selected {config.name} framework as requested."
                return framework, 1.0, reasoning
        
        # Fallback: try fuzzy matching
        for framework in Framework:
            if framework_name in framework.value or framework_name in framework.name.lower():
                config = self.registry.get_framework(framework)
                reasoning = f"Matched to {config.name} framework based on your selection."
                return framework, 0.9, reasoning
        
        # Default fallback
        default = Framework.REASONING_PROBLEM_SOLVING
        config = self.registry.get_framework(default)
        reasoning = f"Could not match '{framework_name}'. Defaulted to {config.name}."
        return default, 0.5, reasoning

    @staticmethod
    def _add_quality_controls(prompt: str) -> str:
        """Add quality control instructions."""

        quality_suffix = """

---
**Quality Standards:**
- Ensure accuracy and factual correctness
- Use clear, appropriate language for the context
- Provide complete, well-structured responses
- Include relevant examples or evidence
- Address edge cases and potential issues
- Maintain consistency throughout"""

        return prompt + quality_suffix

    @staticmethod
    def _calculate_quality_score(prompt: str) -> float:
        """Calculate quality score for the optimized prompt."""
        
        score = 0.0
        
        # Length adequacy (0-25 points)
        length = len(prompt)
        if length > 200:
            score += 25
        elif length > 100:
            score += 15
        elif length > 50:
            score += 10
        
        # Structure (0-25 points)
        if "\n" in prompt:
            score += 10
        if "**" in prompt or "##" in prompt:
            score += 10
        if any(marker in prompt for marker in ["1.", "2.", "-", "•"]):
            score += 5
        
        # Specificity (0-25 points)
        specific_words = ["specific", "exactly", "must", "should", "ensure", "provide", "include"]
        matches = sum(1 for word in specific_words if word.lower() in prompt.lower())
        score += min(matches * 5, 25)
        
        # Instructions (0-25 points)
        instruction_markers = ["please", "ensure", "focus on", "consider", "remember"]
        matches = sum(1 for marker in instruction_markers if marker.lower() in prompt.lower())
        score += min(matches * 5, 25)
        
        return min(score / 100, 1.0)


# ==================== EVALUATION & SIMILARITY ====================


class PromptEvaluator:
    """Evaluate and compare prompts."""

    @staticmethod
    def calculate_similarity(prompt1: str, prompt2: str) -> float:
        """Calculate simple similarity score between two prompts."""

        words1 = set(prompt1.lower().split())
        words2 = set(prompt2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        return len(intersection) / len(union)

    @staticmethod
    def evaluate_quality(prompt: str) -> Dict[str, float]:
        """Evaluate prompt quality metrics."""

        metrics = {
            "clarity": PromptEvaluator._score_clarity(prompt),
            "specificity": PromptEvaluator._score_specificity(prompt),
            "structure": PromptEvaluator._score_structure(prompt),
            "completeness": PromptEvaluator._score_completeness(prompt),
        }
        metrics["overall"] = sum(metrics.values()) / len(metrics)
        return metrics

    @staticmethod
    def _score_clarity(prompt: str) -> float:
        """Score prompt clarity (0-1)."""

        has_questions = "?" in prompt
        has_structure = any(marker in prompt for marker in [":", "\n", "1.", "-"])
        length_score = min(len(prompt) / 500, 1.0)

        return (length_score + has_structure * 0.3 + has_questions * 0.2) / 1.5

    @staticmethod
    def _score_specificity(prompt: str) -> float:
        """Score prompt specificity."""

        specific_words = [
            "specific",
            "exactly",
            "must",
            "should",
            "require",
            "include",
            "format",
            "step",
            "example",
        ]
        count = sum(1 for word in specific_words if word in prompt.lower())
        return min(count / 5, 1.0)

    @staticmethod
    def _score_structure(prompt: str) -> float:
        """Score prompt structure."""

        has_sections = prompt.count("\n") > 2
        has_numbering = bool(re.search(r"\d+\.", prompt))
        has_bullets = "-" in prompt or "•" in prompt

        structure_elements = sum([has_sections, has_numbering, has_bullets])
        return structure_elements / 3

    @staticmethod
    def _score_completeness(prompt: str) -> float:
        """Score prompt completeness."""

        has_context = len(prompt) > 100
        has_goal = any(word in prompt.lower() for word in ["goal", "objective", "want", "need"])
        has_constraints = any(
            word in prompt.lower() for word in ["must", "should", "requirement"]
        )

        completeness_elements = sum([has_context, has_goal, has_constraints])
        return completeness_elements / 3


# ==================== MAIN SYSTEM INTERFACE ====================


class PromptOptimizationSystem:
    """Main system interface for context-aware prompt optimization."""

    def __init__(self) -> None:
        self.optimizer = PromptOptimizer()
        self.evaluator = PromptEvaluator()
        self.registry = FrameworkRegistry()

    def process(self, user_input: str, explicit_framework: Optional[str] = None) -> Dict:
        """
        Process user input and return comprehensive optimization results.
        
        Args:
            user_input: The original user prompt
            explicit_framework: Optional framework name (e.g., "coding_technical", "creative_ideation")
        
        Returns:
            Dictionary with optimization results and quality metrics
        """

        result = self.optimizer.optimize(user_input, explicit_framework)
        original_quality = self.evaluator.evaluate_quality(user_input)
        optimized_quality = self.evaluator.evaluate_quality(result.optimized_prompt)
        improvement = optimized_quality["overall"] - original_quality["overall"]

        framework_config = self.registry.get_framework(result.detected_framework)

        return {
            "original_input": result.original_input,
            "optimized_prompt": result.optimized_prompt,
            "framework": {
                "id": result.detected_framework.value,
                "name": result.framework_name,
                "description": framework_config.description,
                "role": result.suggested_role,
            },
            "confidence": result.confidence_score,
            "reasoning": result.reasoning,
            "quality_metrics": {
                "original": original_quality,
                "optimized": optimized_quality,
                "improvement": improvement,
                "overall_score": result.quality_score,
            },
        }

    def list_available_frameworks(self) -> List[Dict]:
        """List all available frameworks with details."""

        frameworks = []
        for framework_config in self.registry.get_all_frameworks():
            frameworks.append({
                "id": framework_config.framework.value,
                "name": framework_config.name,
                "description": framework_config.description,
                "ideal_for": framework_config.ideal_for,
                "example_inputs": framework_config.example_inputs,
                "role_personas": framework_config.role_personas,
            })

        return frameworks

    def get_framework_by_id(self, framework_id: str) -> Optional[Dict]:
        """Get detailed information about a specific framework."""

        try:
            framework = Framework(framework_id)
            config = self.registry.get_framework(framework)
            
            return {
                "id": config.framework.value,
                "name": config.name,
                "description": config.description,
                "ideal_for": config.ideal_for,
                "trigger_keywords": list(config.trigger_keywords)[:20],  # Limit for readability
                "example_inputs": config.example_inputs,
                "role_personas": config.role_personas,
            }
        except (ValueError, KeyError):
            return None


def main() -> None:
    """Example usage of the new streamlined 7-framework system."""

    system = PromptOptimizationSystem()

    print("=" * 80)
    print("🚀 CONTEXT-AWARE PROMPT OPTIMIZATION SYSTEM v2.0")
    print("=" * 80)
    print("\n✨ New Streamlined 7-Framework Architecture\n")

    # Example 1: Auto-detection - Reasoning
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Auto-Detection - Reasoning & Problem Solving")
    print("=" * 80)

    user_input1 = "Should I invest in stocks or real estate right now?"
    result1 = system.process(user_input1)

    print(f"\n📝 Original Input: {result1['original_input']}")
    print(f"\n🎯 Detected Framework: {result1['framework']['name']}")
    print(f"   Confidence: {result1['confidence']:.1%}")
    print(f"   Role: {result1['framework']['role']}")
    print(f"\n💡 Reasoning: {result1['reasoning']}")
    print(f"\n✨ Optimized Prompt:\n{'-' * 80}\n{result1['optimized_prompt']}\n{'-' * 80}")
    print(f"\n📊 Quality Metrics:")
    print(f"   Improvement: {result1['quality_metrics']['improvement']:+.2f}")
    print(f"   Overall Score: {result1['quality_metrics']['overall_score']:.2f}")

    # Example 2: Auto-detection - Coding
    print("\n\n" + "=" * 80)
    print("EXAMPLE 2: Auto-Detection - Coding & Technical")
    print("=" * 80)

    user_input2 = "Write a Python function to find all prime numbers up to n"
    result2 = system.process(user_input2)

    print(f"\n📝 Original Input: {result2['original_input']}")
    print(f"\n🎯 Detected Framework: {result2['framework']['name']}")
    print(f"   Confidence: {result2['confidence']:.1%}")
    print(f"\n✨ Optimized Prompt (First 400 chars):\n{'-' * 80}\n{result2['optimized_prompt'][:400]}...\n{'-' * 80}")

    # Example 3: Explicit framework selection - Creative
    print("\n\n" + "=" * 80)
    print("EXAMPLE 3: Explicit Framework - Creative & Ideation")
    print("=" * 80)

    user_input3 = "I need ideas for a marketing campaign"
    result3 = system.process(user_input3, explicit_framework="creative_ideation")

    print(f"\n📝 Original Input: {result3['original_input']}")
    print(f"\n🎯 Selected Framework: {result3['framework']['name']}")
    print(f"   Confidence: {result3['confidence']:.1%}")
    print(f"   Role: {result3['framework']['role']}")
    print(f"\n✨ Optimized Prompt (First 400 chars):\n{'-' * 80}\n{result3['optimized_prompt'][:400]}...\n{'-' * 80}")

    # Example 4: Writing framework
    print("\n\n" + "=" * 80)
    print("EXAMPLE 4: Auto-Detection - Writing & Communication")
    print("=" * 80)

    user_input4 = "Draft an email to my team about the new project deadline"
    result4 = system.process(user_input4)

    print(f"\n📝 Original Input: {result4['original_input']}")
    print(f"\n🎯 Detected Framework: {result4['framework']['name']}")
    print(f"   Confidence: {result4['confidence']:.1%}")

    # List all available frameworks
    print("\n\n" + "=" * 80)
    print("📚 AVAILABLE FRAMEWORKS")
    print("=" * 80 + "\n")

    frameworks = system.list_available_frameworks()
    
    for i, fw in enumerate(frameworks, 1):
        print(f"{i}. {fw['name']}")
        print(f"   ID: {fw['id']}")
        print(f"   Description: {fw['description']}")
        print(f"   Ideal for:")
        for ideal in fw['ideal_for'][:3]:  # Show first 3
            print(f"      - {ideal}")
        print(f"   Example: \"{fw['example_inputs'][0]}\"")
        print()

    # Show detection capabilities
    print("\n" + "=" * 80)
    print("🔍 INTELLIGENT AUTO-DETECTION EXAMPLES")
    print("=" * 80 + "\n")

    test_inputs = [
        "How do I learn machine learning from scratch?",
        "Improve this code snippet for me",
        "Research the benefits of meditation",
        "Brainstorm startup ideas in fintech",
    ]

    for test_input in test_inputs:
        result = system.process(test_input)
        print(f"Input: \"{test_input}\"")
        print(f"→ Detected: {result['framework']['name']} ({result['confidence']:.0%} confidence)\n")


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    main()
