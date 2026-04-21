"""Reviewer agent prompt templates."""

REVIEWER_PROMPT = """
You are a performance reviewer.

Executed Action:
{result}

Evaluate:
- Is this effective?
- Any improvement?

Output:
Verdict: [GOOD / NEEDS_IMPROVEMENT / FAILED]
Feedback:
Adjustment:
"""

REVIEW_SUCCESS_KEYWORDS = frozenset({"good", "effective", "successful", "well done", "excellent"})
REVIEW_FAILURE_KEYWORDS = frozenset({"failed", "poor", "ineffective", "bad", "wrong"})
