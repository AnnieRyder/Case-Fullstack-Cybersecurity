from datetime import datetime

from api.models import Finding

SPECIAL_CATEGORIES = set([
        "SQL Injection",
        "Command Injection",
        "Remote Code Execution",
        "SSRF",
        "Authentication Bypass",
        "Deserialization",
        "Hardcoded Secret",
        "Hardcoded Password",
        "Path Traversal"
    ])

def classify(type: str, score: int, category: str) -> str:
    """Utiliza o critério de classificação descrito no documento do Business Case para classificar os findings"""
    
    classification_number = 0
    if score >= 700:
        classification_number = 1
    elif score >= 400:
        classification_number = 2
    elif score >= 300:
        classification_number = 3
    elif score >= 200:
        classification_number = 4
    else:
        classification_number = 5

    if type == "SAST" and category in SPECIAL_CATEGORIES:
        classification_number = max(classification_number - 1, 1)
    classification=f"P{classification_number}"
    return classification
    
def convert_finding(data: dict) -> dict:
    return {
        "id": data["id"],
        "type": data["type"],
        "repository": data["repository"],
        "branch": data["branch"],
        "commit": data["commit"],
        "language": data["language"],
        "title": data["title"],
        "category": data["category"],
        "description": data["description"],
        "rule_id": data["ruleId"],
        "file": data["file"],
        "line": data["line"],
        "score": data["score"],
        "status": data["status"],
        "author": data["author"],
        "detected_at": datetime.fromisoformat(
            data["detectedAt"].replace("Z", "+00:00")
        ),
        "updated_at": datetime.fromisoformat(
            data["updatedAt"].replace("Z", "+00:00")
        ),
        "classification": classify(data["type"], data["score"], data["category"]),
    }