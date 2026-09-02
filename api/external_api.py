import os

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import httpx

EXTERNAL_API_URL = os.environ["EXTERNAL_API_URL"]
EXTERNAL_API_TOKEN = os.environ["EXTERNAL_API_TOKEN"]

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(
        (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPStatusError)
    )
)
def fetch_findings(page: int, limit: int = 100) -> dict:
    """
    Acessa os findings da API externa e retorna os resultados em formato JSON.
    """
    response = httpx.get(
        f"{EXTERNAL_API_URL}/api/v1/findings",
        params={
            "page": page,
            "limit": limit,
        },
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {EXTERNAL_API_TOKEN}",
        },
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()