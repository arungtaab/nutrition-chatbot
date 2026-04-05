"""
Lightweight guardrails for sensitive queries: medical-style asks and eating-disorder harm.
Prefer short refusal over calling the LLM when patterns clearly match.
"""
import re

_REFUSAL = (
    "I cannot provide medical diagnosis, treatment, or medication advice. "
    "For health conditions, symptoms, or prescriptions, please talk to a qualified clinician "
    "or registered dietitian. I can still help with general meal ideas and food planning—feel free to rephrase."
)

# Case-insensitive triggers: diagnosis, prescribing, “for my condition”, etc.
_PATTERNS = [
    re.compile(r"\bdiagnos(e|is|ed|ing)?\b", re.I),
    re.compile(r"\bprognosis\b", re.I),
    re.compile(r"\bprescrib(e|ed|ing)?\b", re.I),
    re.compile(r"\bmedication(s)?\b.*\b(should i|can i|is it ok|safe)\b", re.I),
    re.compile(r"\b(should i stop|should i start)\b.*\b(med|medicine|pill|drug)\b", re.I),
    re.compile(r"\bdo i have\b", re.I),
    re.compile(r"\bis (this|it) (cancer|diabetes|covid)\b", re.I),
    re.compile(r"\btreat(ment|ing)?\b.*\b(condition|disease|disorder)\b", re.I),
    re.compile(r"\bwithdrawal\b.*\b(from )?(med|medicine|drug)\b", re.I),
    re.compile(r"\bdosage\b", re.I),
    re.compile(r"\binteraction\b.*\b(med|medicine|drug|supplement)\b", re.I),
]


def medical_sensitive_message(text: str) -> bool:
    if not text or not text.strip():
        return False
    t = text.strip()
    return any(p.search(t) for p in _PATTERNS)


def safety_refusal_reply() -> str:
    return _REFUSAL


# Eating-disorder / self-harm adjacent (high-confidence; avoid blocking generic “calories” or “healthy lunch”).
_ED_REFUSAL = (
    "I’m not able to help with requests about disordered eating, purging, extreme restriction, or "
    "pro–eating-disorder content. If you’re struggling with food or your body, you deserve real support—"
    "please reach out to a clinician, therapist, or registered dietitian who works with eating concerns. "
    "In the U.S., the National Eating Disorders Association (NEDA) offers a helpline and resources at "
    "nationaleatingdisorders.org; if you’re in acute crisis, you can call or text 988 (Suicide & Crisis Lifeline). "
    "If you’re elsewhere, search for an eating-disorder helpline in your country. "
    "I can help with general, balanced meal ideas if you’d like to ask in those terms."
)

_ED_PATTERNS = [
    re.compile(r"\bpro[- ]?ana\b", re.I),
    re.compile(r"\bpro[- ]?mia\b", re.I),
    re.compile(r"\bthinspo\b", re.I),
    re.compile(r"\bthinspiration\b", re.I),
    re.compile(r"\bhow (do i|to) purge\b", re.I),
    re.compile(r"\b(induce|make myself) vomit\b", re.I),
    re.compile(r"\b(self[- ]induced )?vomit(ing)?\b.*\b(after (eating|meals?)|lose weight)\b", re.I),
    re.compile(r"\bthrow\s+up\b.*\b(after (eating|every)|lose weight|stay thin)\b", re.I),
    re.compile(r"\bbinge\s+and\s+purge\b", re.I),
    re.compile(r"\bpurge\b.*\b(after (eating|binge)|calories)\b", re.I),
    re.compile(r"\blaxatives?\b.*\b(lose weight|weight loss|empty out|skinny|thinner)\b", re.I),
    re.compile(r"\bhow to become (anorexic|bulimic)\b", re.I),
    re.compile(r"\bteach me (anorexia|bulimia|how to starve)\b", re.I),
    re.compile(r"\bhow (few|little) calories\b.*\b(can i|should i|to lose|per day)\b", re.I),
    re.compile(r"\beat (nothing|no food)\b.*\b(for |)(a |)(\d+ )?(day|week|month)s?\b", re.I),
    re.compile(r"\bwater fast\b.*\b(\d+\s*(day|week)|two week|three week|month)\b", re.I),
    re.compile(r"\bfast\b.*\b(until i('m| am) (underweight|skinny|thin enough))\b", re.I),
]


def ed_sensitive_message(text: str) -> bool:
    if not text or not text.strip():
        return False
    t = text.strip()
    return any(p.search(t) for p in _ED_PATTERNS)


def ed_refusal_reply() -> str:
    return _ED_REFUSAL
