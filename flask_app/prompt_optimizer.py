"""Context-Aware Prompt Optimization System
A multi-layered framework for intelligent prompt generation and enhancement.
"""

import re
import os
import json
from typing import Dict, List, Tuple, Optional
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
    """Prompt design frameworks."""

    CHAIN_OF_THOUGHT = "chain_of_thought"
    FEW_SHOT = "few_shot"
    MULTI_SHOT = "multi_shot"
    FUNCTION_CALLING = "function_calling"
    ROLE_BASED = "role_based"
    INSTRUCTION_BASED = "instruction_based"
    BRAINSTORM = "brainstorm"


@dataclass
class UseCase:
    """Use case definition with metadata."""

    category: str
    subcategory: str
    description: str
    frameworks: List[Framework]
    role_template: Optional[str] = None
    keywords: Optional[List[str]] = None


@dataclass
class OptimizedPrompt:
    """Result of prompt optimization."""

    original_input: str
    detected_use_case: UseCase
    applied_frameworks: List[Framework]
    optimized_prompt: str
    confidence_score: float
    reasoning: str


# ==================== USE CASE TAXONOMY ====================


class UseCaseTaxonomy:
    """Comprehensive use case mapping system."""

    def __init__(self) -> None:
        self.use_cases = self._build_taxonomy()

    def _build_taxonomy(self) -> Dict[str, List[UseCase]]:
        """Build the complete use case taxonomy."""

        return {
            # Category 1: Content Creation
            "content_creation": [
                UseCase(
                    category="content_creation",
                    subcategory="blog_article",
                    description="Long-form SEO-friendly text",
                    frameworks=[Framework.FEW_SHOT, Framework.INSTRUCTION_BASED],
                    role_template="Professional Content Writer",
                    keywords=["blog", "article", "write", "content", "seo", "post"],
                ),
                UseCase(
                    category="content_creation",
                    subcategory="social_media",
                    description="Social media content generation",
                    frameworks=[Framework.FEW_SHOT, Framework.ROLE_BASED],
                    role_template="Social Media Marketing Expert",
                    keywords=["social", "tweet", "instagram", "facebook", "post", "caption"],
                ),
                UseCase(
                    category="content_creation",
                    subcategory="video_script",
                    description="Video script structure and tone",
                    frameworks=[Framework.INSTRUCTION_BASED],
                    role_template="Video Script Writer",
                    keywords=["video", "script", "youtube", "screenplay"],
                ),
                UseCase(
                    category="content_creation",
                    subcategory="ad_copy",
                    description="Short-form persuasive writing",
                    frameworks=[Framework.ROLE_BASED],
                    role_template="Ad Copywriter",
                    keywords=["ad", "advertisement", "copy", "product description", "marketing"],
                ),
            ],
            # Category 2: Business and Marketing
            "business_marketing": [
                UseCase(
                    category="business_marketing",
                    subcategory="business_plan",
                    description="Formal business plan structure",
                    frameworks=[Framework.CHAIN_OF_THOUGHT, Framework.ROLE_BASED],
                    role_template="Business Strategy Consultant",
                    keywords=["business plan", "strategy", "startup", "venture"],
                ),
                UseCase(
                    category="business_marketing",
                    subcategory="sales_pitch",
                    description="Persuasive sales content",
                    frameworks=[Framework.ROLE_BASED],
                    role_template="Investor Relations Expert",
                    keywords=["pitch", "investor", "sales", "proposal", "presentation"],
                ),
                UseCase(
                    category="business_marketing",
                    subcategory="customer_persona",
                    description="Customer persona creation",
                    frameworks=[Framework.MULTI_SHOT, Framework.FUNCTION_CALLING],
                    role_template="Marketing Analyst",
                    keywords=["persona", "customer", "audience", "target market"],
                ),
            ],
            # Category 3: Education and Training
            "education_training": [
                UseCase(
                    category="education_training",
                    subcategory="explain_complex",
                    description="Simplify complex concepts",
                    frameworks=[Framework.CHAIN_OF_THOUGHT],
                    role_template="Expert Educator",
                    keywords=["explain", "teach", "understand", "learn", "concept"],
                ),
                UseCase(
                    category="education_training",
                    subcategory="quiz_generation",
                    description="Structured quiz output",
                    frameworks=[Framework.FUNCTION_CALLING],
                    role_template="Assessment Designer",
                    keywords=["quiz", "test", "questions", "assessment", "exam"],
                ),
                UseCase(
                    category="education_training",
                    subcategory="lesson_plan",
                    description="Organized lesson templates",
                    frameworks=[Framework.ROLE_BASED],
                    role_template="Curriculum Designer",
                    keywords=["lesson", "curriculum", "teaching plan", "course"],
                ),
            ],
            # Category 4: Technical/Programming
            "technical_programming": [
                UseCase(
                    category="technical_programming",
                    subcategory="code_generation",
                    description="Generate or debug code",
                    frameworks=[Framework.FUNCTION_CALLING, Framework.FEW_SHOT],
                    role_template="Senior Software Engineer",
                    keywords=["code", "debug", "program", "function", "algorithm", "implement"],
                ),
                UseCase(
                    category="technical_programming",
                    subcategory="code_explanation",
                    description="Step-by-step code reasoning",
                    frameworks=[Framework.CHAIN_OF_THOUGHT, Framework.ROLE_BASED],
                    role_template="Senior Developer",
                    keywords=["explain code", "how does", "code review", "analyze"],
                ),
                UseCase(
                    category="technical_programming",
                    subcategory="api_documentation",
                    description="API explanation and docs",
                    frameworks=[Framework.FEW_SHOT, Framework.ROLE_BASED],
                    role_template="Technical Writer",
                    keywords=["api", "documentation", "endpoint", "integration"],
                ),
            ],
            # Category 5: Data Analysis
            "data_analysis": [
                UseCase(
                    category="data_analysis",
                    subcategory="data_summary",
                    description="Analyze and summarize data",
                    frameworks=[Framework.FUNCTION_CALLING, Framework.CHAIN_OF_THOUGHT],
                    role_template="Data Analyst",
                    keywords=["analyze", "data", "statistics", "insights", "trends"],
                ),
                UseCase(
                    category="data_analysis",
                    subcategory="visualization",
                    description="Data visualization insights",
                    frameworks=[Framework.CHAIN_OF_THOUGHT, Framework.ROLE_BASED],
                    role_template="Data Visualization Expert",
                    keywords=["visualize", "chart", "graph", "plot", "dashboard"],
                ),
            ],
            # Category 6: Personal Productivity
            "personal_productivity": [
                UseCase(
                    category="personal_productivity",
                    subcategory="time_management",
                    description="Schedule and time optimization",
                    frameworks=[Framework.FUNCTION_CALLING],
                    role_template="Productivity Coach",
                    keywords=["schedule", "time", "calendar", "organize", "plan day"],
                ),
                UseCase(
                    category="personal_productivity",
                    subcategory="goal_planning",
                    description="Goal setting and planning",
                    frameworks=[Framework.CHAIN_OF_THOUGHT],
                    role_template="Life Coach",
                    keywords=["goal", "plan", "achieve", "objective", "milestone"],
                ),
            ],
            # Category 7: Communication & Summarization
            "communication_summarization": [
                UseCase(
                    category="communication_summarization",
                    subcategory="email_draft",
                    description="Email composition",
                    frameworks=[Framework.FEW_SHOT, Framework.ROLE_BASED],
                    role_template="Professional Communications Specialist",
                    keywords=["email", "message", "write to", "draft", "letter"],
                ),
                UseCase(
                    category="communication_summarization",
                    subcategory="meeting_summary",
                    description="Meeting notes summarization",
                    frameworks=[Framework.FUNCTION_CALLING],
                    role_template="Executive Assistant",
                    keywords=["summarize", "meeting", "notes", "key points", "minutes"],
                ),
            ],
            # Category 8: Creative and Design
            "creative_design": [
                UseCase(
                    category="creative_design",
                    subcategory="design_ideas",
                    description="Creative design concepts",
                    frameworks=[Framework.BRAINSTORM, Framework.FEW_SHOT],
                    role_template="Creative Director",
                    keywords=["design", "logo", "brand", "creative", "concept"],
                ),
                UseCase(
                    category="creative_design",
                    subcategory="creative_writing",
                    description="Poetry, fiction, stories",
                    frameworks=[Framework.INSTRUCTION_BASED, Framework.FEW_SHOT],
                    role_template="Creative Writer",
                    keywords=["story", "poem", "fiction", "lyrics", "creative writing"],
                ),
            ],
            # Category 9: Research and Knowledge
            "research_knowledge": [
                UseCase(
                    category="research_knowledge",
                    subcategory="academic_summary",
                    description="Academic content synthesis",
                    frameworks=[Framework.CHAIN_OF_THOUGHT],
                    role_template="Research Analyst",
                    keywords=["research", "academic", "summarize paper", "literature review"],
                ),
                UseCase(
                    category="research_knowledge",
                    subcategory="multi_source",
                    description="Multi-source synthesis",
                    frameworks=[Framework.MULTI_SHOT, Framework.CHAIN_OF_THOUGHT],
                    role_template="Knowledge Synthesis Expert",
                    keywords=["compare", "synthesize", "multiple sources", "analysis"],
                ),
            ],
            # Category 10: Personal Advice
            "personal_advice": [
                UseCase(
                    category="personal_advice",
                    subcategory="motivational",
                    description="Motivational support",
                    frameworks=[Framework.ROLE_BASED],
                    role_template="Life Coach",
                    keywords=["motivate", "inspire", "advice", "help me", "support"],
                ),
                UseCase(
                    category="personal_advice",
                    subcategory="journaling",
                    description="Journaling prompts",
                    frameworks=[Framework.INSTRUCTION_BASED],
                    role_template="Mindfulness Coach",
                    keywords=["journal", "reflect", "thoughts", "feelings"],
                ),
            ],
        }

    def get_all_use_cases(self) -> List[UseCase]:
        """Get flattened list of all use cases."""

        all_cases: List[UseCase] = []
        for category_cases in self.use_cases.values():
            all_cases.extend(category_cases)
        return all_cases

# ==================== FRAMEWORK APPLIERS ====================


class FrameworkApplier:
    """Apply specific prompt framework patterns."""

    @staticmethod
    def apply_chain_of_thought(prompt: str, use_case: UseCase) -> str:
        """Apply Chain-of-Thought reasoning pattern."""

        return f"""Let's approach this step-by-step:

Task: {prompt}

Please think through this systematically:
1. First, break down the key components
2. Then, analyze each part carefully
3. Finally, synthesize a comprehensive solution

Show your reasoning at each step."""

    @staticmethod
    def apply_few_shot(prompt: str, use_case: UseCase) -> str:
        """Apply Few-shot learning pattern."""

        examples = FrameworkApplier._get_examples_for_use_case(use_case)

        return f"""Here are some examples of similar tasks:

{examples}

Now, please complete this task following the same pattern:
{prompt}"""

    @staticmethod
    def apply_role_based(prompt: str, use_case: UseCase) -> str:
        """Apply Role-based prompting."""

        role = use_case.role_template or "Expert"

        return f"""You are a {role} with deep expertise in this domain.

Task: {prompt}

Please respond as this expert would, leveraging your specialized knowledge and professional approach."""

    @staticmethod
    def apply_function_calling(prompt: str, use_case: UseCase) -> str:
        """Apply Function-calling / Structured output pattern."""

        return f"""{prompt}

Please provide your response in a structured format:
- Use clear sections and headers
- Include actionable items where applicable
- Format data in tables or lists as appropriate
- Ensure the output is machine-readable if needed"""

    @staticmethod
    def apply_instruction_based(prompt: str, use_case: UseCase) -> str:
        """Apply clear instruction-based pattern."""

        return f"""Task: {prompt}

Please complete this task following these guidelines:
- Be clear and direct
- Focus on the specific requirements
- Provide concrete, actionable output
- Maintain high quality standards"""

    @staticmethod
    def apply_brainstorm(prompt: str, use_case: UseCase) -> str:
        """Apply brainstorming pattern."""

        return f"""Creative brainstorming session:

Topic: {prompt}

Please generate multiple diverse ideas:
- Think outside the box
- Explore different angles and perspectives
- Prioritize creativity and originality
- Provide at least 5-7 distinct concepts"""

    @staticmethod
    def _get_examples_for_use_case(use_case: UseCase) -> str:
        """Generate contextual examples based on use case."""

        examples_map = {
            "blog_article": """Example 1: \"Write about AI trends\" → \"Top 5 AI Trends Reshaping Business in 2024\"
Example 2: \"Tech startups guide\" → \"The Complete Guide to Launching Your Tech Startup: From Idea to IPO\" """,
            "social_media": """Example 1: Product launch → \"🚀 Excited to unveil our latest innovation! Game-changing features that'll transform how you work. Link in bio! #TechLaunch\"
Example 2: Behind-the-scenes → \"Ever wondered what goes into creating our products? Here's a sneak peek at our design process 🎨✨\" """,
            "code_generation": """Example 1: \"Sort array\" → def quick_sort(arr): ...
Example 2: \"API endpoint\" → @app.route('/api/users', methods=['GET']) ...""",
        }

        return examples_map.get(
            use_case.subcategory,
            "Example: Input → High-quality output following best practices",
        )


# ==================== PROMPT OPTIMIZER ====================


class PromptOptimizer:
    """Main optimization engine."""

    def __init__(self) -> None:
        self.taxonomy = UseCaseTaxonomy()
        self.applier = FrameworkApplier()

    def optimize(self, user_input: str, explicit_use_case: str) -> OptimizedPrompt:
        """Optimize user prompt based on the explicitly provided use case."""

        if not explicit_use_case:
            raise ValueError("explicit_use_case is required for optimization")

        use_case = self._find_use_case_by_name(explicit_use_case)
        confidence = 1.0

        optimized = self._apply_frameworks(user_input, use_case)
        optimized = self._add_quality_controls(optimized)
        reasoning = self._generate_reasoning(user_input, use_case, confidence)

        return OptimizedPrompt(
            original_input=user_input,
            detected_use_case=use_case,
            applied_frameworks=use_case.frameworks,
            optimized_prompt=optimized,
            confidence_score=confidence,
            reasoning=reasoning,
        )

    def _apply_frameworks(self, prompt: str, use_case: UseCase) -> str:
        """Apply the primary framework for the use case."""

        if not use_case.frameworks:
            return prompt

        primary_framework = use_case.frameworks[0]
        framework_methods = {
            Framework.CHAIN_OF_THOUGHT: self.applier.apply_chain_of_thought,
            Framework.FEW_SHOT: self.applier.apply_few_shot,
            Framework.MULTI_SHOT: self.applier.apply_few_shot,
            Framework.ROLE_BASED: self.applier.apply_role_based,
            Framework.FUNCTION_CALLING: self.applier.apply_function_calling,
            Framework.INSTRUCTION_BASED: self.applier.apply_instruction_based,
            Framework.BRAINSTORM: self.applier.apply_brainstorm,
        }

        method = framework_methods.get(primary_framework)
        if method:
            return method(prompt, use_case)

        return prompt

    @staticmethod
    def _add_quality_controls(prompt: str) -> str:
        """Add quality control instructions."""

        quality_suffix = """

Quality requirements:
- Ensure accuracy and relevance
- Use clear, professional language
- Provide complete, well-structured output
- Double-check for errors before responding"""

        return prompt + quality_suffix

    @staticmethod
    def _generate_reasoning(original: str, use_case: UseCase, confidence: float) -> str:
        """Generate explanation of optimization decisions."""

        frameworks = ", ".join(f.value for f in use_case.frameworks)
        return f"""Optimization Analysis:
        
1. Selected Use Case: {use_case.category} → {use_case.subcategory}
    Confidence: {confidence:.1%}
   
2. Applied Frameworks: {frameworks}
   
3. Role Template: {use_case.role_template or 'General Assistant'}

4. Optimization Strategy:
   - Primary framework provides structure
   - Role context adds expertise
   - Quality controls ensure high output standards
   
5. Expected Improvement:
   - More focused and relevant responses
   - Better structured output
   - Enhanced domain-specific knowledge application"""

    def _find_use_case_by_name(self, name: str) -> UseCase:
        """Find use case by category or subcategory name."""

        all_cases = self.taxonomy.get_all_use_cases()
        for case in all_cases:
            if name.lower() in [case.category.lower(), case.subcategory.lower()]:
                return case

        return all_cases[0]


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

    def process(self, user_input: str, explicit_use_case: Optional[str] = None) -> Dict:
        """Process user input and return comprehensive optimization results."""

        if not explicit_use_case:
            raise ValueError("explicit_use_case is required")

        result = self.optimizer.optimize(user_input, explicit_use_case)
        original_quality = self.evaluator.evaluate_quality(user_input)
        optimized_quality = self.evaluator.evaluate_quality(result.optimized_prompt)
        improvement = optimized_quality["overall"] - original_quality["overall"]

        return {
            "original_input": result.original_input,
            "optimized_prompt": result.optimized_prompt,
            "use_case": {
                "category": result.detected_use_case.category,
                "subcategory": result.detected_use_case.subcategory,
                "description": result.detected_use_case.description,
                "role": result.detected_use_case.role_template,
            },
            "frameworks": [f.value for f in result.applied_frameworks],
            "confidence": result.confidence_score,
            "reasoning": result.reasoning,
            "quality_metrics": {
                "original": original_quality,
                "optimized": optimized_quality,
                "improvement": improvement,
            },
        }

    def list_available_use_cases(self) -> List[Dict]:
        """List all available use cases."""

        taxonomy = UseCaseTaxonomy()
        cases = []

        for category, use_case_list in taxonomy.use_cases.items():
            for use_case in use_case_list:
                cases.append(
                    {
                        "category": use_case.category,
                        "subcategory": use_case.subcategory,
                        "description": use_case.description,
                        "frameworks": [f.value for f in use_case.frameworks],
                        "role": use_case.role_template,
                    }
                )

        return cases


def main() -> None:
    """Example usage of the system requiring explicit use cases."""

    system = PromptOptimizationSystem()

    print("=" * 80)
    print("EXAMPLE 1: Blog Writing (Explicit)")
    print("=" * 80)

    user_input1 = "Write a blog post about the future of AI"
    result1 = system.process(user_input1, explicit_use_case="blog_article")

    print(f"\n📝 Original Input:\n{result1['original_input']}\n")
    print(f"🎯 Use Case: {result1['use_case']['subcategory']}")
    print(f"   Category: {result1['use_case']['category']}")
    print(f"   Confidence: {result1['confidence']:.1%}\n")
    print(f"⚙️  Applied Frameworks: {', '.join(result1['frameworks'])}\n")
    print(f"✨ Optimized Prompt:\n{result1['optimized_prompt']}\n")
    print(f"📊 Quality Improvement: {result1['quality_metrics']['improvement']:+.2f}")
    print(
        f"   Original Score: {result1['quality_metrics']['original']['overall']:.2f}"
    )
    print(
        f"   Optimized Score: {result1['quality_metrics']['optimized']['overall']:.2f}\n"
    )

    print("\n" + "=" * 80)
    print("EXAMPLE 2: Code Generation")
    print("=" * 80)

    user_input2 = "Create a function to sort a list of numbers"
    result2 = system.process(user_input2, explicit_use_case="code_generation")

    print(f"\n📝 Original Input:\n{user_input2}\n")
    print(f"🎯 Use Case: {result2['use_case']['subcategory']}")
    print(f"⚙️  Applied Frameworks: {', '.join(result2['frameworks'])}\n")
    print(f"✨ Optimized Prompt:\n{result2['optimized_prompt']}\n")

    print("\n" + "=" * 80)
    print("EXAMPLE 3: Business Plan")
    print("=" * 80)

    user_input3 = "I need help planning my startup"
    result3 = system.process(user_input3, explicit_use_case="business_plan")

    print(f"\n📝 Original Input:\n{user_input3}\n")
    print(f"🎯 Use Case: {result3['use_case']['subcategory']}")
    print(f"👔 Role: {result3['use_case']['role']}\n")
    print(f"✨ Optimized Prompt:\n{result3['optimized_prompt']}\n")

    print("\n" + "=" * 80)
    print("AVAILABLE USE CASES")
    print("=" * 80 + "\n")

    cases = system.list_available_use_cases()
    current_category = None

    for case in cases[:10]:
        if case["category"] != current_category:
            current_category = case["category"]
            print(f"\n📂 {current_category.upper().replace('_', ' ')}")

        print(f"  • {case['subcategory']}: {case['description']}")
        print(f"    Frameworks: {', '.join(case['frameworks'])}")


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    main()
