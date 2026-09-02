from datetime import datetime
from pydantic import BaseModel, ConfigDict

#Modelos de serialização de resposta para a API, utilizando Pydantic para validação e documentação.
class SyncResponse(BaseModel):
    status: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "Sincronização realizada."
            }
        }
    }

class FindingResponse(BaseModel):
    id: str
    type: str
    repository: str
    branch: str
    commit: str
    language: str | None
    category: str | None
    title: str | None
    description: str | None
    rule_id: str | None
    file: str | None
    line: int | None
    score: int
    status: str
    author: str | None
    detected_at: datetime | None
    updated_at: datetime | None
    classification: str

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "ISS-123456",
            "type": "SCA",
            "repository": "my-repo",
            "branch": "main",
            "commit": "abc123",
            "language": "Python",
             "category": "Transitive Dependency Risk",
            "title": "Transitive Dependency Risk",
            "description": "Detected Transitive Dependency Risk.",
            "ruleId": "transitive_dependency_risk",
            "file": "/path/to/file.py",
            "line": 42,
            "score": 750,
            "status": "OPEN",
            "author": "John Doe",
            "detected_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "classification": "P1"
        }
    })

class FindingListResponse(BaseModel):
    page: int
    limit: int
    total: int
    totalPages: int
    hasNext: bool
    findings: list[FindingResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "page": 1,
                "limit": 25,
                "total": 100,
                "totalPages": 4,
                "hasNext": True,
                "findings": [
                    FindingResponse.model_json_schema()["example"]
                ]
            }
        }
    }

class MetricsResponse(BaseModel):
    total: int
    open: int
    fixed: int
    ignored: int
    classification: dict[str, int]

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 100,
                "open": 50,
                "fixed": 30,
                "ignored": 20,
                "classification": {
                    "P1": 10,
                    "P2": 20,
                    "P3": 30,
                    "P4": 20,
                    "P5": 20
                }
            }
        }
    }