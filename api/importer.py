from api.external_api import fetch_findings
from api.convert_finding import convert_finding
from sqlalchemy.dialects.postgresql import insert
from api.models import Finding

from sqlalchemy.orm import Session

def import_findings(db: Session):
    """Importa findings da API externa e insere/atualiza no banco de dados local."""
    page = 1
    while True:
        response = fetch_findings(page=page, limit=100)
        findings = response["data"]
        classified_findings=[convert_finding(finding) for finding in findings]
        
        statement = insert(Finding).values(classified_findings)

        statement = statement.on_conflict_do_update(
            index_elements=[Finding.id],
            set_={
                "type": statement.excluded.type,
                "repository": statement.excluded.repository,
                "branch": statement.excluded.branch,
                "commit": statement.excluded.commit,
                "language": statement.excluded.language,
                "category": statement.excluded.category,
                "description": statement.excluded.description,
                "rule_id": statement.excluded.rule_id,
                "file": statement.excluded.file,
                "line": statement.excluded.line,
                "score": statement.excluded.score,
                "status": statement.excluded.status,
                "author": statement.excluded.author,
                "detected_at": statement.excluded.detected_at,
                "updated_at": statement.excluded.updated_at,
                "classification": statement.excluded.classification,
            },
        )
        db.execute(statement)
        db.commit()

        if not response["hasNext"]:
            break
        page += 1
    