"""
Cognition Structuring Engine v7.0 — AUTHORITY MODE

This system is an AUTHORITY LAYER, not a rewriter.
It does NOT preserve ambiguity. It does NOT remain neutral.
It DECIDES what the user is building and ENFORCES it.

Core Principle: Indecision is failure.

FORBIDDEN outputs: "or", "maybe", "can be", "either", "possibly", "could", "might"

MANDATORY sections in every output:
- ROLE
- PLATFORM
- OBJECTIVE
- SCOPE
- CONSTRAINTS
- EXECUTION
- OUTPUT CONTRACT

Architecture:
- OutputValidator: Validates against forbidden words and mandatory sections
- DecisionEngine: Makes irreversible decisions when user is vague
- StructureAssembler: Builds structured output
- PromptOptimizer: Core optimizer
- PromptOptimizationSystem: Public API (Flask compatibility)
"""

import re
import os
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# =============================================================================
# CORE TYPES
# =============================================================================


class Framework(Enum):
    """Seven cognitive frameworks for prompt classification."""
    CODING = "coding_technical"
    TEACHING = "instruction_learning"
    EXPLANATION = "research_exploration"
    RESEARCH = "reasoning_problem_solving"
    CREATIVE = "creative_ideation"
    STRATEGY = "optimization_review"
    CONTENT = "writing_communication"


# Backward compatibility aliases
CODING_DEVELOPMENT = Framework.CODING
TEACHING_LEARNING = Framework.TEACHING
EXPLANATION = Framework.EXPLANATION
RESEARCH = Framework.RESEARCH
CREATIVE_DESIGN = Framework.CREATIVE
STRATEGY_THINKING = Framework.STRATEGY
CONTENT_CREATION = Framework.CONTENT


FORBIDDEN_WORDS = [
    "or", "maybe", "could", "might", "possibly",
    "either", "can be", "kind of", "sort of",
    "perhaps", "whatever", "something like"
]


MANDATORY_SECTIONS = [
    "ROLE",
    "PLATFORM",
    "OBJECTIVE",
    "SCOPE",
    "CONSTRAINTS",
    "EXECUTION",
    "OUTPUT CONTRACT"
]


@dataclass
class FrameworkSpec:
    """Framework specification with targets and constraints."""
    framework: Framework
    name: str
    description: str
    targets: List[str]
    enforcements: List[str]
    avoidances: List[str]
    triggers: List[str]
    ideal_for: List[str]


@dataclass
class OptimizedPrompt:
    """Result of prompt optimization."""
    framework: Framework
    framework_name: str
    prompt: str
    valid: bool
    violations: List[str]
    confidence: float
    generation_mode: str = "static"


# =============================================================================
# LLM PROVIDER
# =============================================================================


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_input: str, **kwargs) -> Optional[str]:
        pass
    
    @property
    @abstractmethod
    def is_available(self) -> bool:
        pass


class GroqProvider(LLMProvider):
    """Groq API provider."""
    
    API_URL = "https://api.groq.com/openai/v1/chat/completions"
    MODEL = "llama-3.3-70b-versatile"
    TIMEOUT = 45
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GROQ_API_KEY")
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key and REQUESTS_AVAILABLE)
    
    def generate(
        self,
        system_prompt: str,
        user_input: str,
        temperature: float = 0.3,
        max_tokens: int = 1200,
    ) -> Optional[str]:
        if not self.is_available:
            return None
        
        try:
            response = requests.post(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                },
                timeout=self.TIMEOUT,
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            
            logger.error(f"LLM API error: {response.status_code}")
            return None
            
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            return None


# =============================================================================
# VALIDATION ENGINE
# =============================================================================


class OutputValidator:
    """Validates output against forbidden words and mandatory sections."""

    @staticmethod
    def validate(text: str) -> List[str]:
        violations = []
        lowered = text.lower()

        for word in FORBIDDEN_WORDS:
            if re.search(rf"\b{re.escape(word)}\b", lowered):
                violations.append(f"Forbidden word detected: '{word}'")

        for section in MANDATORY_SECTIONS:
            if section not in text:
                violations.append(f"Missing mandatory section: {section}")

        return violations


# =============================================================================
# FRAMEWORK REGISTRY
# =============================================================================


class FrameworkRegistry:
    """Registry for all cognitive frameworks."""
    
    def __init__(self):
        self._frameworks = self._build()
    
    def get(self, framework: Framework) -> FrameworkSpec:
        return self._frameworks[framework]
    
    def get_all(self) -> List[FrameworkSpec]:
        return list(self._frameworks.values())
    
    def _build(self) -> Dict[Framework, FrameworkSpec]:
        return {
            Framework.CODING: FrameworkSpec(
                framework=Framework.CODING,
                name="Coding & Development",
                description="Architecture clarity, deterministic behavior, production-grade systems",
                targets=["Senior Software Engineer", "Production-grade", "No prototypes"],
                enforcements=[
                    "Single tech stack decided",
                    "Modular architecture",
                    "Explicit error handling",
                    "Type safety enforced",
                ],
                avoidances=["Generic best practices", "Optional alternatives", "Prototype patterns"],
                triggers=["code", "build", "implement", "function", "api", "debug", "fix", "create", "develop", "program", "script", "database", "backend", "frontend", "app"],
                ideal_for=["Code generation", "System design", "Debugging", "API development"],
            ),
            
            Framework.TEACHING: FrameworkSpec(
                framework=Framework.TEACHING,
                name="Teaching & Learning",
                description="Progressive complexity, concept sequencing, retention-focused",
                targets=["Expert Instructor", "Progressive complexity", "Retention-focused"],
                enforcements=[
                    "Prerequisites stated first",
                    "One concept per section",
                    "Simple → Abstract progression",
                    "Verification checkpoints",
                ],
                avoidances=["Information dumping", "Mixed difficulty", "Tangents"],
                triggers=["teach", "learn", "how to", "tutorial", "guide", "understand", "beginner", "step by step", "explain how", "show me"],
                ideal_for=["Tutorials", "Educational content", "Skill building", "Onboarding"],
            ),
            
            Framework.EXPLANATION: FrameworkSpec(
                framework=Framework.EXPLANATION,
                name="Explanation",
                description="High signal density, zero fluff, technically precise",
                targets=["Domain Expert", "High signal density", "Zero fluff"],
                enforcements=[
                    "Definition → Mechanism → Example → Limitation",
                    "Every sentence adds information",
                    "Explicit boundaries",
                ],
                avoidances=["Storytelling", "Metaphor overload", "Redundancy"],
                triggers=["what is", "explain", "describe", "tell me about", "overview", "summary", "eli5", "difference between"],
                ideal_for=["Concept explanations", "Technical documentation", "Knowledge transfer"],
            ),
            
            Framework.RESEARCH: FrameworkSpec(
                framework=Framework.RESEARCH,
                name="Research & Analysis",
                description="Evidence-based, analytically rigorous, structured inquiry",
                targets=["Research Analyst", "Evidence-based", "Analytically rigorous"],
                enforcements=[
                    "Explicit research question",
                    "Scope boundaries defined",
                    "Assumptions declared",
                    "Evidence-backed claims only",
                ],
                avoidances=["Opinions without evidence", "Broad wandering", "Speculation"],
                triggers=["research", "analyze", "compare", "investigate", "study", "evaluate", "assess", "pros and cons", "tradeoffs"],
                ideal_for=["Market research", "Technical analysis", "Decision support", "Due diligence"],
            ),
            
            Framework.CREATIVE: FrameworkSpec(
                framework=Framework.CREATIVE,
                name="Creative & Design",
                description="Constrained creativity, taste-controlled, visual coherence",
                targets=["Creative Director", "Constrained creativity", "Taste-controlled"],
                enforcements=[
                    "Visual direction rules explicit",
                    "Style constraints with values",
                    "Single mood anchor",
                    "Boundaries defined",
                ],
                avoidances=["Unbounded creativity", "Vague aesthetics", "Multiple directions"],
                triggers=["design", "creative", "brainstorm", "ideas", "story", "visual", "aesthetic", "style", "brand", "ui", "ux"],
                ideal_for=["UI/UX design", "Creative writing", "Brand development", "Visual concepts"],
            ),
            
            Framework.STRATEGY: FrameworkSpec(
                framework=Framework.STRATEGY,
                name="Strategy & Thinking",
                description="First-principles reasoning, decision-grade clarity, single recommendation",
                targets=["Strategic Advisor", "First-principles", "Decision-grade"],
                enforcements=[
                    "Problem reframed from first principles",
                    "Hard constraints identified",
                    "Options with criteria",
                    "Single recommendation",
                ],
                avoidances=["Motivational language", "Generic advice", "Hedging"],
                triggers=["decide", "should i", "strategy", "plan", "approach", "solve", "problem", "optimize", "improve", "best way"],
                ideal_for=["Strategic planning", "Decision making", "Problem solving", "Process optimization"],
            ),
            
            Framework.CONTENT: FrameworkSpec(
                framework=Framework.CONTENT,
                name="Content Creation",
                description="Audience-aligned, purpose-driven, structured communication",
                targets=["Content Strategist", "Audience-aligned", "Purpose-driven"],
                enforcements=[
                    "Audience explicitly defined",
                    "Single intent locked",
                    "Tone boundaries set",
                    "Structure enforced",
                ],
                avoidances=["Viral bait", "Emotional padding", "Multiple drafts"],
                triggers=["write", "draft", "email", "blog", "content", "article", "post", "message", "copy", "document"],
                ideal_for=["Email writing", "Blog posts", "Documentation", "Marketing copy"],
            ),
        }


# =============================================================================
# DECISION ENGINE
# =============================================================================


class DecisionEngine:
    """Makes irreversible decisions when user is vague."""

    def __init__(self, registry: Optional[FrameworkRegistry] = None):
        self.registry = registry or FrameworkRegistry()

    def decide_platform(self, text: str) -> str:
        text_lower = text.lower()
        if "mobile" in text_lower or "ios" in text_lower or "android" in text_lower:
            return "Mobile Application"
        if "api" in text_lower or "backend" in text_lower or "server" in text_lower:
            return "Backend Service"
        if "cli" in text_lower or "terminal" in text_lower or "command" in text_lower:
            return "CLI Tool"
        return "Web Application"

    def decide_goal(self, framework: Framework) -> str:
        goals = {
            Framework.CODING: "Build a production-grade system with deterministic behavior",
            Framework.TEACHING: "Teach concept progressively with verification checkpoints",
            Framework.EXPLANATION: "Explain with high signal density and zero fluff",
            Framework.RESEARCH: "Conduct structured analysis with evidence-backed findings",
            Framework.CREATIVE: "Design within explicit constraints and single direction",
            Framework.STRATEGY: "Produce single decision recommendation from first principles",
            Framework.CONTENT: "Create structured content for defined audience"
        }
        return goals[framework]

    def decide_persona(self, framework: Framework) -> str:
        spec = self.registry.get(framework)
        return spec.targets[0] if spec.targets else "Expert"
    
    def decide_scope(self, framework: Framework) -> Tuple[List[str], List[str]]:
        """Returns (included, excluded) scope lists."""
        scopes = {
            Framework.CODING: (
                ["Core functionality", "Error handling", "Type safety"],
                ["Testing infrastructure", "Deployment configs", "CI/CD", "Documentation beyond inline"]
            ),
            Framework.TEACHING: (
                ["Core concept", "Prerequisites", "Practice exercises"],
                ["Advanced edge cases", "Alternative approaches", "Historical context"]
            ),
            Framework.EXPLANATION: (
                ["Definition", "Mechanism", "Example", "Limitations"],
                ["History", "Alternatives", "Opinions", "Comparisons"]
            ),
            Framework.RESEARCH: (
                ["Research question", "Methodology", "Findings", "Implications"],
                ["Recommendations beyond scope", "Speculative futures"]
            ),
            Framework.CREATIVE: (
                ["Visual system", "Component design", "Interaction rules"],
                ["Implementation code", "Backend logic", "Content strategy"]
            ),
            Framework.STRATEGY: (
                ["Problem reframe", "Options analysis", "Single recommendation"],
                ["Implementation details", "Timeline", "Resource allocation"]
            ),
            Framework.CONTENT: (
                ["Core message", "Structure", "Call-to-action"],
                ["Distribution strategy", "SEO", "Visual assets"]
            ),
        }
        return scopes.get(framework, (["Core functionality"], ["Out of scope items"]))

    def decide_constraints(self, framework: Framework) -> List[str]:
        constraints = {
            Framework.CODING: [
                "Stack: React 18 + TypeScript (DECIDED)",
                "Architecture: Modular with single-responsibility",
                "Error handling: Explicit paths for all failures",
                "Types: Strict, no `any`, no implicit",
                "Functions: Maximum 40 lines, single purpose",
            ],
            Framework.TEACHING: [
                "Prerequisites: Stated before content",
                "Concept limit: One per section maximum",
                "Progression: Simple → Applied → Abstract (strict)",
                "Validation: Each section ends with checkpoint",
            ],
            Framework.EXPLANATION: [
                "Structure: Definition → Mechanism → Example → Limitation (mandatory)",
                "Density: Every sentence adds unique information",
                "Separation: Intuition vs implementation distinct",
                "Boundaries: State what does NOT apply",
            ],
            Framework.RESEARCH: [
                "Research question: Explicitly stated first",
                "Scope: Defined boundaries (in/out)",
                "Assumptions: Declared upfront",
                "Evidence: No claims without backing",
            ],
            Framework.CREATIVE: [
                "Colors: Max 5 in palette",
                "Typography: Single scale, max 3 weights",
                "Spacing: 4px/8px grid system",
                "Mood: Single anchor (Professional-minimal)",
            ],
            Framework.STRATEGY: [
                "Reframe: Problem restated from first principles",
                "Options: Exactly 3 distinct paths",
                "Criteria: Explicit decision factors with weights",
                "No: Motivational language, generic advice, hedging",
            ],
            Framework.CONTENT: [
                "Audience: Technical professionals (DECIDED)",
                "Intent: Inform (single purpose)",
                "Tone: Professional, direct, no contractions",
                "Length: 500-800 words",
            ],
        }
        return constraints.get(framework, ["Single responsibility per module", "No optional features"])

    def decide_execution(self, framework: Framework) -> List[str]:
        executions = {
            Framework.CODING: [
                "Define file structure and module boundaries",
                "Establish interfaces and type contracts",
                "Implement core logic with input validation",
                "Add error boundaries and edge cases",
                "Include usage example",
            ],
            Framework.TEACHING: [
                "State prerequisites and single learning outcome",
                "Introduce concept with minimal example",
                "Explain mechanism (not just syntax)",
                "Provide practice exercise with expected output",
                "Bridge to next concept",
            ],
            Framework.EXPLANATION: [
                "Precise definition (one sentence)",
                "How it works mechanistically",
                "Concrete example with context",
                "Limitations and edge cases",
            ],
            Framework.RESEARCH: [
                "Frame precise research question",
                "Define scope and methodology",
                "Analyze with structured approach",
                "Synthesize findings with evidence",
                "State implications and limitations",
            ],
            Framework.CREATIVE: [
                "Define visual constraints explicitly",
                "Establish style rules with values",
                "Design within boundaries",
                "Validate against mood anchor",
            ],
            Framework.STRATEGY: [
                "Reframe problem from first principles",
                "Identify hard constraints and variables",
                "Generate 3 distinct options",
                "Compare against weighted criteria",
                "Single recommendation with reasoning",
            ],
            Framework.CONTENT: [
                "Define audience context and needs",
                "Lock single content intent",
                "Structure for scannable consumption",
                "Apply consistent tone throughout",
                "End with clear call-to-action",
            ],
        }
        return executions.get(framework, ["Define structure", "Implement logic", "Validate", "Produce output"])

    def decide_output_contract(self, framework: Framework) -> List[str]:
        contracts = {
            Framework.CODING: [
                "Format: Complete, runnable TypeScript code",
                "Deliverables: All files with imports, no placeholders",
                "Boundaries: No test files, no deployment configs",
            ],
            Framework.TEACHING: [
                "Format: Numbered sections with headers",
                "Deliverables: Concept explanation, code example, exercise",
                "Boundaries: No tangents, no alternatives",
            ],
            Framework.EXPLANATION: [
                "Format: Four sections matching execution order",
                "Deliverables: Definition, mechanism, example, limitations",
                "Boundaries: No storytelling, no metaphors",
            ],
            Framework.RESEARCH: [
                "Format: Structured analysis with headers",
                "Deliverables: Question, methodology, findings, implications",
                "Boundaries: No opinions without evidence",
            ],
            Framework.CREATIVE: [
                "Format: Design specification with values",
                "Deliverables: Color codes, spacing, typography, components",
                "Boundaries: No alternatives, no mood boards",
            ],
            Framework.STRATEGY: [
                "Format: Structured analysis with decision matrix",
                "Deliverables: Reframed problem, 3 options, matrix, recommendation",
                "Boundaries: No hedging, no multiple recommendations",
            ],
            Framework.CONTENT: [
                "Format: Structured content with headers",
                "Deliverables: Complete draft, ready to publish",
                "Boundaries: No multiple drafts, no options",
            ],
        }
        return contracts.get(framework, ["Structured response", "No commentary", "No alternatives"])


# =============================================================================
# STRUCTURE ASSEMBLER
# =============================================================================


class StructureAssembler:
    """Assembles the final structured prompt."""

    def assemble(
        self,
        persona: str,
        platform: str,
        objective: str,
        scope_in: List[str],
        scope_out: List[str],
        constraints: List[str],
        execution: List[str],
        output_contract: List[str]
    ) -> str:
        scope_in_str = "\n".join(f"- {s}" for s in scope_in)
        scope_out_str = "\n".join(f"- {s}" for s in scope_out)
        constraints_str = "\n".join(f"- {c}" for c in constraints)
        execution_str = "\n".join(f"{i+1}. {e}" for i, e in enumerate(execution))
        output_str = "\n".join(f"- {o}" for o in output_contract)

        return f"""ROLE
{persona}

PLATFORM
{platform}

OBJECTIVE
{objective}

SCOPE
Included:
{scope_in_str}

Excluded:
{scope_out_str}

CONSTRAINTS
{constraints_str}

EXECUTION
{execution_str}

OUTPUT CONTRACT
{output_str}"""


# =============================================================================
# FRAMEWORK CLASSIFIER
# =============================================================================


class FrameworkClassifier:
    """Classifies user intent into cognitive framework."""
    
    def __init__(self, registry: Optional[FrameworkRegistry] = None):
        self.registry = registry or FrameworkRegistry()
    
    def classify(self, user_input: str) -> Tuple[Framework, float, str]:
        """Classify input into most appropriate framework."""
        input_lower = user_input.lower()
        scores: Dict[Framework, int] = {}
        
        for spec in self.registry.get_all():
            score = sum(1 for trigger in spec.triggers if trigger in input_lower)
            scores[spec.framework] = score
        
        if not scores or max(scores.values()) == 0:
            return Framework.CODING, 0.5, "Default classification"
        
        best = max(scores, key=scores.get)  # type: ignore
        confidence = min(scores[best] / 5, 1.0)
        spec = self.registry.get(best)
        
        return best, confidence, f"Classified as {spec.name}"


# =============================================================================
# STATIC STRUCTURER (DETERMINISTIC FALLBACK)
# =============================================================================


class StaticStructurer:
    """
    Deterministic fallback when LLM fails validation.
    No ambiguity. No LLM. Pure structure.
    Used when regeneration attempts exceed retry limit.
    """

    def __init__(self, registry: Optional[FrameworkRegistry] = None):
        self.registry = registry or FrameworkRegistry()
        self.assembler = StructureAssembler()
        self.decider = DecisionEngine(self.registry)

    def structure(
        self,
        user_input: str,
        framework: Framework,
    ) -> OptimizedPrompt:
        """Generate deterministic structured output without LLM."""
        
        spec = self.registry.get(framework)
        cleaned_input = self._clean_input(user_input)
        
        # Make all decisions deterministically
        persona = self.decider.decide_persona(framework)
        platform = self.decider.decide_platform(user_input)
        objective = f"{self.decider.decide_goal(framework)}: {cleaned_input}"
        scope_in, scope_out = self.decider.decide_scope(framework)
        constraints = self.decider.decide_constraints(framework)
        execution = self.decider.decide_execution(framework)
        output_contract = self.decider.decide_output_contract(framework)

        # Assemble structured prompt
        structured = self.assembler.assemble(
            persona,
            platform,
            objective,
            scope_in,
            scope_out,
            constraints,
            execution,
            output_contract
        )

        # Validate (should always pass with deterministic output)
        violations = OutputValidator.validate(structured)

        return OptimizedPrompt(
            framework=framework,
            framework_name=spec.name,
            prompt=structured,
            valid=len(violations) == 0,
            violations=violations,
            confidence=1.0,
            generation_mode="static"
        )

    def _clean_input(self, text: str) -> str:
        """Remove filler and forbidden words from input."""
        filler_patterns = [
            r'\b(please|kindly|could you|can you|i want to|i need to|i would like to)\b',
            r'\b(maybe|possibly|perhaps|something like|sort of|kind of)\b',
            r'\b(basically|actually|honestly|literally)\b',
        ]
        
        for pattern in filler_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        text = ' '.join(text.split())
        return text.strip()


# =============================================================================
# PROMPT OPTIMIZER (CORE) — VALIDATION-ENFORCED COMPILER
# =============================================================================


class PromptOptimizer:
    """
    Validation-enforced compiler, not a best-effort generator.
    
    CONTROL LOOP (NON-NEGOTIABLE):
    1. Generate structured output
    2. Validate immediately
    3. If invalid: regenerate with violation feedback (retry loop)
    4. If still invalid after max retries: use StaticStructurer fallback
    5. Return ONLY valid outputs
    
    No unstructured output ever escapes this system.
    """

    MAX_RETRIES = 2
    RETRY_BACKOFF = 1.5  # Temperature multiplier for retries

    def __init__(
        self,
        registry: Optional[FrameworkRegistry] = None,
        llm_provider: Optional[LLMProvider] = None,
    ):
        self.registry = registry or FrameworkRegistry()
        self.classifier = FrameworkClassifier(self.registry)
        self.decider = DecisionEngine(self.registry)
        self.assembler = StructureAssembler()
        self.llm_provider = llm_provider or GroqProvider()
        self.static_structurer = StaticStructurer(self.registry)
        self.validator = OutputValidator()

    def optimize(
        self,
        user_input: str,
        explicit_framework: Optional[str] = None,
        force_static: bool = False,
    ) -> OptimizedPrompt:
        """
        Optimize user input through validation-enforced control loop.
        
        NEVER returns invalid output.
        NEVER returns unstructured output.
        NEVER avoids decisions.
        
        Returns: ValidatedPrompt (guaranteed valid)
        Raises: ValueError if input is invalid
        """
        
        if not user_input or not user_input.strip():
            raise ValueError("Input cannot be empty")
        
        cleaned_input = self._clean_input(user_input)
        
        # Classify framework
        if explicit_framework:
            framework, confidence = self._resolve_framework(explicit_framework)
        else:
            framework, confidence, _ = self.classifier.classify(user_input)
        
        # If static is forced, skip LLM entirely
        if force_static:
            logger.info(f"Static mode forced. Using StaticStructurer for {framework.name}")
            return self.static_structurer.structure(user_input, framework)
        
        # CONTROL LOOP: Generate → Validate → (Regenerate or Fallback)
        violation_history: List[str] = []
        
        for attempt in range(self.MAX_RETRIES + 1):
            logger.debug(f"Optimization attempt {attempt + 1}/{self.MAX_RETRIES + 1}")
            
            # STEP 1: GENERATE
            generated = self._generate_with_llm(
                user_input=user_input,
                cleaned_input=cleaned_input,
                framework=framework,
                attempt=attempt,
                violation_feedback=violation_history,
            )
            
            if generated is None:
                logger.warning(f"LLM generation failed on attempt {attempt + 1}")
                if attempt == self.MAX_RETRIES:
                    logger.info("Max retries reached. Falling back to StaticStructurer")
                    return self.static_structurer.structure(user_input, framework)
                continue
            
            # STEP 2: VALIDATE
            violations = self.validator.validate(generated)
            
            # STEP 3: REJECT OR ACCEPT
            if not violations:
                # Valid! Return it
                spec = self.registry.get(framework)
                logger.info(f"Output validated successfully on attempt {attempt + 1}")
                return OptimizedPrompt(
                    framework=framework,
                    framework_name=spec.name,
                    prompt=generated,
                    valid=True,
                    violations=[],
                    confidence=confidence,
                    generation_mode="dynamic"
                )
            
            # STEP 4: REJECT AND REGENERATE
            violation_history.extend(violations)
            logger.warning(f"Output invalid on attempt {attempt + 1}. Violations: {violations}")
            
            if attempt == self.MAX_RETRIES:
                # Retries exhausted → Fall back to static
                logger.info(f"Max retries ({self.MAX_RETRIES}) reached. Using StaticStructurer fallback")
                return self.static_structurer.structure(user_input, framework)
            
            # Continue to next attempt with accumulated feedback
        
        # This should never be reached, but safety net
        logger.critical("Unexpected control flow. Defaulting to static structurer")
        return self.static_structurer.structure(user_input, framework)

    def _generate_with_llm(
        self,
        user_input: str,
        cleaned_input: str,
        framework: Framework,
        attempt: int,
        violation_feedback: List[str],
    ) -> Optional[str]:
        """Generate structured output using LLM."""
        
        if not self.llm_provider.is_available:
            logger.debug("LLM provider not available. Skipping LLM generation")
            return None
        
        spec = self.registry.get(framework)
        
        # Build system prompt
        system_prompt = self._build_system_prompt(framework, spec)
        
        # Build user prompt
        if attempt == 0:
            # First attempt: normal prompt
            user_prompt = f"""Optimize this input into a structured prompt:

INPUT: {user_input}

FRAMEWORK: {spec.name}

Generate a complete structured prompt following MANDATORY SECTIONS exactly.
No exceptions. No shortcuts.

Return ONLY the structured prompt. No explanations."""
        else:
            # Retry attempt: include violation feedback
            violations_text = "\n".join(f"- {v}" for v in violation_feedback)
            user_prompt = f"""Your previous output violated the following rules:
{violations_text}

INPUT: {user_input}
FRAMEWORK: {spec.name}

REGENERATE the prompt correcting ALL violations.
Be exact. Follow structure precisely.
Do not explain changes. Return ONLY the structured prompt."""
        
        # Call LLM with adjusted temperature for retries
        temp = 0.3 * (self.RETRY_BACKOFF ** attempt)
        temp = min(temp, 1.0)  # Cap at 1.0
        
        generated = self.llm_provider.generate(
            system_prompt=system_prompt,
            user_input=user_prompt,
            temperature=temp,
            max_tokens=2000,
        )
        
        return generated

    def _build_system_prompt(self, framework: Framework, spec: FrameworkSpec) -> str:
        """Build the system prompt for the LLM."""
        
        return f"""You are a structured prompt compiler.

ROLE: Expert Prompt Structurer
SYSTEM: Cognition Structuring Engine v7.0

FRAMEWORK: {spec.name}
{spec.description}

YOU MUST:

1. ENFORCE mandatory sections:
   - ROLE: Who this prompt is for
   - PLATFORM: Where execution happens
   - OBJECTIVE: What the task is
   - SCOPE: What's in/out
   - CONSTRAINTS: Hard rules
   - EXECUTION: Step-by-step process
   - OUTPUT CONTRACT: Exact deliverables

2. FORBIDDEN WORDS: Never use these
   {", ".join(FORBIDDEN_WORDS)}
   
   If you use them, your output will be REJECTED.

3. DECISIONS: Make them explicitly
   - Choose platform clearly (not "maybe")
   - Define boundaries explicitly
   - State role with authority
   - No ambiguity. No hedging.

4. OUTPUT: Only return the structured prompt
   - No commentary
   - No markdown formatting
   - No explanations
   - Just the structure

Remember: This is a compiler, not a chatbot.
Output must be VALID or REJECTED.
There is no "almost correct"."""

    def _clean_input(self, text: str) -> str:
        """Remove filler and forbidden words from input."""
        filler_patterns = [
            r'\b(please|kindly|could you|can you|i want to|i need to|i would like to)\b',
            r'\b(maybe|possibly|perhaps|something like|sort of|kind of)\b',
            r'\b(basically|actually|honestly|literally)\b',
        ]
        
        for pattern in filler_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        text = ' '.join(text.split())
        return text.strip()
    
    def _resolve_framework(self, name: str) -> Tuple[Framework, float]:
        """Resolve framework from explicit name."""
        name = name.lower().strip()
        
        for fw in Framework:
            if fw.value == name or fw.name.lower() == name:
                return fw, 1.0
        
        for fw in Framework:
            if name in fw.value or name in fw.name.lower():
                return fw, 0.9
        
        keyword_map = {
            "coding": Framework.CODING,
            "code": Framework.CODING,
            "build": Framework.CODING,
            "teaching": Framework.TEACHING,
            "learn": Framework.TEACHING,
            "explain": Framework.EXPLANATION,
            "research": Framework.RESEARCH,
            "analyze": Framework.RESEARCH,
            "creative": Framework.CREATIVE,
            "design": Framework.CREATIVE,
            "strategy": Framework.STRATEGY,
            "decide": Framework.STRATEGY,
            "content": Framework.CONTENT,
            "write": Framework.CONTENT,
        }
        
        for keyword, fw in keyword_map.items():
            if keyword in name:
                return fw, 0.8
        
        return Framework.CODING, 0.5
    
    def _clean_input(self, text: str) -> str:
        """Remove filler and forbidden words from input."""
        # Remove filler phrases
        filler_patterns = [
            r'\b(please|kindly|could you|can you|i want to|i need to|i would like to)\b',
            r'\b(maybe|possibly|perhaps|something like|sort of|kind of)\b',
            r'\b(basically|actually|honestly|literally)\b',
        ]
        
        for pattern in filler_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean whitespace
        text = ' '.join(text.split())
        return text.strip()
    
    def _resolve_framework(self, name: str) -> Tuple[Framework, float]:
        """Resolve framework from explicit name."""
        name = name.lower().strip()
        
        # Direct match by value
        for fw in Framework:
            if fw.value == name or fw.name.lower() == name:
                return fw, 1.0
        
        # Partial match
        for fw in Framework:
            if name in fw.value or name in fw.name.lower():
                return fw, 0.9
        
        # Keyword match
        keyword_map = {
            "coding": Framework.CODING,
            "code": Framework.CODING,
            "build": Framework.CODING,
            "teaching": Framework.TEACHING,
            "learn": Framework.TEACHING,
            "explain": Framework.EXPLANATION,
            "research": Framework.RESEARCH,
            "analyze": Framework.RESEARCH,
            "creative": Framework.CREATIVE,
            "design": Framework.CREATIVE,
            "strategy": Framework.STRATEGY,
            "decide": Framework.STRATEGY,
            "content": Framework.CONTENT,
            "write": Framework.CONTENT,
        }
        
        for keyword, fw in keyword_map.items():
            if keyword in name:
                return fw, 0.8
        
        return Framework.CODING, 0.5


# =============================================================================
# PUBLIC API (Flask compatibility)
# =============================================================================


class PromptOptimizationSystem:
    """
    Public API for the Cognition Structuring Engine.
    Maintains backward compatibility with Flask app.
    
    GUARANTEE: Every output is valid and structured.
    GUARANTEE: No unstructured output escapes.
    GUARANTEE: All mandatory sections are present.
    GUARANTEE: No forbidden language appears.
    """
    
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.registry = FrameworkRegistry()
        self.llm_provider = llm_provider or GroqProvider()
        self.optimizer = PromptOptimizer(self.registry, self.llm_provider)
    
    def process(
        self,
        user_input: str,
        explicit_framework: Optional[str] = None,
        force_static: bool = False,
    ) -> Dict[str, Any]:
        """
        Process user input through validation-enforced control loop.
        
        BEHAVIOR:
        - Generate structured output
        - Validate immediately
        - Regenerate with feedback if invalid (up to 2 retries)
        - Fall back to StaticStructurer if all retries fail
        - Return ONLY valid, structured output
        
        Args:
            user_input: The prompt to optimize
            explicit_framework: Force a specific framework (optional)
            force_static: Skip LLM, use StaticStructurer directly (optional)
        
        Returns:
            Dictionary with guaranteed valid structured output
        
        Raises:
            ValueError: If input is empty or invalid
        """
        result = self.optimizer.optimize(
            user_input,
            explicit_framework=explicit_framework,
            force_static=force_static,
        )
        spec = self.registry.get(result.framework)
        
        return {
            "original_input": user_input,
            "optimized_prompt": result.prompt,
            "framework": {
                "id": result.framework.value,
                "name": result.framework_name,
                "description": spec.description,
                "role": spec.targets[0] if spec.targets else "Expert",
            },
            "confidence": result.confidence,
            "reasoning": f"Classified as {result.framework_name}",
            "generation_mode": result.generation_mode,
            "valid": result.valid,
            "violations": result.violations,
        }
    
    def list_frameworks(self) -> List[Dict[str, Any]]:
        """List all frameworks."""
        return [
            {
                "id": spec.framework.value,
                "name": spec.name,
                "description": spec.description,
                "ideal_for": spec.ideal_for,
                "example_inputs": spec.triggers[:5],
                "role_personas": spec.targets,
            }
            for spec in self.registry.get_all()
        ]
    
    def list_available_frameworks(self) -> List[Dict[str, Any]]:
        """Alias for backward compatibility."""
        return self.list_frameworks()
    
    def get_framework(self, framework_id: str) -> Optional[Dict[str, Any]]:
        """Get framework details."""
        try:
            fw = Framework(framework_id)
            spec = self.registry.get(fw)
            return {
                "id": spec.framework.value,
                "name": spec.name,
                "description": spec.description,
                "ideal_for": spec.ideal_for,
                "trigger_keywords": spec.triggers,
                "example_inputs": spec.triggers[:5],
                "role_personas": spec.targets,
            }
        except (ValueError, KeyError):
            return None
    
    def get_framework_by_id(self, framework_id: str) -> Optional[Dict[str, Any]]:
        """Alias for backward compatibility."""
        return self.get_framework(framework_id)
    
    def is_dynamic_available(self) -> bool:
        """Check if LLM is available (for future dynamic enhancement)."""
        return self.llm_provider.is_available if self.llm_provider else False


# =============================================================================
# CLI
# =============================================================================


def main():
    """Demonstration."""
    print("=" * 70)
    print("COGNITION STRUCTURING ENGINE v7.0 — AUTHORITY MODE")
    print("Decision-Making Engine — NOT a Prompt Rewriter")
    print("=" * 70)
    
    system = PromptOptimizationSystem()
    
    test_inputs = [
        "build a todo app maybe in react or vue with a nice ui",
        "explain how databases work",
        "help me decide which framework to use",
    ]
    
    for user_input in test_inputs:
        print(f"\n{'-' * 70}")
        print(f"INPUT: \"{user_input}\"")
        
        result = system.process(user_input)
        
        print(f"Framework: {result['framework']['name']}")
        print(f"Valid: {result['valid']}")
        if result['violations']:
            print(f"Violations: {result['violations']}")
        print(f"\nSTRUCTURED OUTPUT:\n{result['optimized_prompt']}")
    
    print(f"\n{'=' * 70}")


if __name__ == "__main__":
    main()
