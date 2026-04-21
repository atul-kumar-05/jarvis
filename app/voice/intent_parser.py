"""
Advanced voice intent parser — extracts intent + entities from spoken text.

Supports natural language variations like:
  - "add task buy groceries with high priority"
  - "delete the running task"
  - "what should I do next"
  - "mark task 3 as done"
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedCommand:
    """Structured result of voice intent parsing."""
    intent: str
    task_title: str = ""
    task_id: Optional[int] = None
    priority: str = "medium"
    raw_text: str = ""
    confidence: float = 1.0


_INTENT_PATTERNS: list[tuple[str, list[str]]] = [
    ("add_task", [
        r"(?:add|create|new|make)\s+(?:a\s+)?task\s+(.+)",
        r"(?:i need to|i have to|remind me to)\s+(.+)",
        r"(?:schedule|plan)\s+(.+)",
    ]),
    ("delete_task", [
        r"(?:delete|remove|cancel|drop)\s+(?:the\s+)?task\s+(.+)",
        r"(?:delete|remove|cancel|drop)\s+(.+?)(?:\s+task)?$",
        r"(?:get rid of)\s+(.+)",
    ]),
    ("complete_task", [
        r"(?:complete|finish|done|mark)\s+(?:task\s+)?(?:#?\s*)?(\d+)",
        r"(?:mark|set)\s+(?:task\s+)?(.+?)\s+(?:as\s+)?(?:done|completed|finished)",
        r"(?:i'?ve?\s+)?(?:done|finished|completed)\s+(?:task\s+)?(.+)",
    ]),
    ("next_action", [
        r"(?:what\s+)?(?:should\s+i\s+do|next|recommend)",
        r"(?:what'?s?\s+)?(?:my\s+)?(?:next|top|most important|urgent)\s+task",
        r"(?:jarvis|hey)\s*,?\s*(?:what|tell me)",
        r"(?:suggest|pick|choose)\s+(?:a\s+)?task",
        r"(?:what|which)\s+task",
    ]),
    ("list_tasks", [
        r"(?:show|list|display|get|read)\s+(?:me\s+)?(?:all\s+)?(?:my\s+)?tasks",
        r"(?:what\s+)?tasks?\s+(?:do\s+i\s+have|are\s+(?:there|pending))",
        r"(?:how\s+many)\s+tasks",
    ]),
    ("task_status", [
        r"(?:status|progress|update)\s+(?:of\s+)?(?:task\s+)?(.+)",
        r"(?:how\s+is)\s+(.+?)(?:\s+going)?$",
    ]),
    ("help", [
        r"(?:help|what can you do|commands|how do i)",
        r"(?:jarvis|hey)\s*,?\s*help",
    ]),
]

_PRIORITY_PATTERNS = {
    "critical": [r"\b(?:critical|urgent|asap|emergency)\b"],
    "high":     [r"\b(?:high|important|priority)\b"],
    "low":      [r"\b(?:low|later|whenever|someday)\b"],
}


def _extract_priority(text: str) -> str:
    lower = text.lower()
    for priority, patterns in _PRIORITY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, lower):
                return priority
    return "medium"


def _clean_task_title(title: str) -> str:
    title = re.sub(r"\b(?:with\s+)?(?:critical|urgent|high|medium|low|important|asap)\b\s*(?:priority)?\s*",
                   "", title, flags=re.IGNORECASE)
    title = re.sub(r"\s+$", "", title)
    title = re.sub(r"^(?:the|a|an)\s+", "", title, flags=re.IGNORECASE)
    return title.strip()


def _extract_task_id(text: str) -> Optional[int]:
    match = re.search(r"(?:task\s+)?#?\s*(\d+)", text)
    return int(match.group(1)) if match else None


def parse_voice_command(text: str) -> ParsedCommand:
    """Parse a voice command into a structured ParsedCommand."""
    stripped = text.strip()
    lower = re.sub(r"^(?:hey\s+)?(?:jarvis)\s*,?\s*", "", stripped.lower()).strip()

    for intent, patterns in _INTENT_PATTERNS:
        for pattern in patterns:
            match = re.search(pattern, lower, re.IGNORECASE)
            if match:
                entity = match.group(1).strip() if match.lastindex and match.lastindex >= 1 else ""
                priority = _extract_priority(entity or lower)
                task_title = _clean_task_title(entity) if entity else ""
                task_id = _extract_task_id(entity or lower)
                return ParsedCommand(intent=intent, task_title=task_title, task_id=task_id,
                                     priority=priority, raw_text=stripped)

    return ParsedCommand(intent="unknown", raw_text=stripped, confidence=0.3)


def detect_intent(voice: str) -> str:
    """Legacy compat — returns just the intent string."""
    return parse_voice_command(voice).intent
