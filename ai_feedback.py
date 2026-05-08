"""Local posture feedback.

This file does not use Anthropic or any paid API.
It gives posture advice using simple local rules.
"""

ISSUE_ADVICE = {
    "HEAD_FORWARD": "Bring your ea/rs back over your shoulders and gently tuck your chin.",
    "NECK_BENT": "Lift your screen or look straight ahead so your neck stays long.",
    "ROUNDED_SHOULDERS": "Open your chest, relax your shoulders down, and bring them slightly back.",
    "LEANING_FORWARD": "Sit back into the chair and stack your ribs over your hips.",
    "SHOULDER_TILT": "Level your shoulders and avoid leaning to one side.",
    "NO_PERSON": "Step into view so the camera can see your head, shoulders, and torso.",
    "LOW_CONFIDENCE": "Improve lighting and keep your upper body visible to the camera.",
}


def get_feedback(status, issues=None):
    """Return offline feedback for the current posture status."""
    issues = issues or []

    if status == "CORRECT":
        return "Good posture. Keep your head relaxed, shoulders level, and take regular movement breaks."

    if not issues:
        return "Adjust your sitting position so your head, shoulders, and torso are clearly aligned."

    advice = []
    for issue in issues[:3]:
        advice.append(ISSUE_ADVICE.get(issue, issue.replace("_", " ").capitalize()))

    return " ".join(advice)


def format_feedback_lines(text, max_chars=52):
    """Split feedback text into short lines for drawing on video."""
    words = text.split()
    lines = []
    current = []

    for word in words:
        candidate = " ".join(current + [word])

        if len(candidate) > max_chars and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)

    if current:
        lines.append(" ".join(current))

    return lines
