from fastapi import Depends, FastAPI, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from typing import Optional

from api.database import get_db

from api.importer import import_findings

from api.finding_query import finding_query

from api.responsemodels import SyncResponse, FindingListResponse, FindingResponse, MetricsResponse

from api.models import Finding

api = FastAPI()

# Definição de valores válidos para filtros
VALID_TYPES = {"SCA", "SAST"}
VALID_STATUSES = {"OPEN", "FIXED", "IGNORED"}
VALID_CLASSIFICATIONS = {"P1", "P2", "P3", "P4", "P5"}


def validate_enum_value(value: Optional[str], valid_values: set, param_name: str, error_code: int = 400):
    """Valida que um valor está no conjunto permitido."""
    if value is None:
        return None
    if value not in valid_values:
        raise HTTPException(
            status_code=error_code,
            detail=f"Invalid {param_name}: '{value}'. Must be one of: {', '.join(sorted(valid_values))}"
        )
    return value

@api.post("/sync", response_model=SyncResponse, summary = "Sincroniza findings com a API externa.")
def sync_findings(db: Session = Depends(get_db)):
    import_findings(db)
    return {"status": "Sincronização realizada."}

@api.get("/issues", response_model=FindingListResponse, summary = "Lista findings com paginação e filtros.", description = "Lista findings com paginação e filtros opcionais. Os filtros disponíveis são: repository, type, status e classification.")
def get_findings(
    page: int = Query(1, ge=1),
    limit: int = Query(25, ge=1, le=100),
    repository: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    classification: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    type = validate_enum_value(type, VALID_TYPES, "type")
    status = validate_enum_value(status, VALID_STATUSES, "status")
    classification = validate_enum_value(classification, VALID_CLASSIFICATIONS, "classification")

    return finding_query(page, limit, repository, type, status, classification, db)


@api.get("/issues/{id}", response_model=FindingResponse, summary = "Retorna finding por id.")
def get_finding(id: str, db: Session = Depends(get_db)):
    finding = db.get(Finding, id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return finding

@api.get("/metrics", response_model=MetricsResponse, summary = "Retorna métricas de findings.", description = "Retorna métricas de findings, incluindo total, abertos, corrigidos, ignorados e classificação.")
def get_metrics(db: Session = Depends(get_db)):
    total=db.scalar(select(func.count())
        .select_from(Finding))
    open=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.status=="OPEN"))
    fixed=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.status=="FIXED"))
    ignored=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.status=="IGNORED"))
    p1=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.classification=="P1"))
    p2=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.classification=="P2"))
    p3=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.classification=="P3"))
    p4=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.classification=="P4"))
    p5=db.scalar(select(func.count())
        .select_from(Finding)
        .where(Finding.classification=="P5"))

    return {
        "total": total,
        "open": open,
        "fixed": fixed,
        "ignored": ignored,
        "classification": {
            "P1": p1,
            "P2": p2,
            "P3": p3,
            "P4": p4,
            "P5": p5
        }
    }