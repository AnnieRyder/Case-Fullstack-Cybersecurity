from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from api.models import Finding



def finding_query(
    page: int,
    limit: int,
    repository: Optional[str],
    type: Optional[str],
    status: Optional[str],
    classification: Optional[str],
    db: Session
) -> dict:
    """Consulta findings com paginação e filtros opcionais."""

    offset = (page - 1) * limit

    conditions=[]

    if repository is not None:
        conditions.append(Finding.repository == repository)
    if type is not None:
        conditions.append(Finding.type == type)
    if status is not None:
        conditions.append(Finding.status == status)
    if classification is not None:
        conditions.append(Finding.classification == classification)


    total_count = db.scalar(select(func.count())
        .select_from(Finding)
        .where(*conditions)
        )

    query = (select(Finding)
        .order_by(Finding.id)
        .where(*conditions)
        .offset(offset)
        .limit(limit))

    findings = db.scalars(query).all()

    return {
        "page": page,
        "limit": limit,
        "total": total_count,
        "totalPages": (total_count + limit - 1) // limit,
        "hasNext": page * limit < total_count,
        "findings": findings
    }
