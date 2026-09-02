# Projeto: Consumo de dados de API externa

## Descrição

Nesse projeto, foram consumidos dados da API externa disponibilizada em `https://github.com/andrejr971/interview-test/`, persistidos os dados em um banco de dados após sua classificação, e disponibilizada uma API para pesquisa dos dados.

## Estrutura do repositório
```
/
  .env
  alembic.ini
  docker-compose.yml
  README.md
  requirements.txt
  api/
  alembic/
```

## Dependências (requirements.txt)

```
fastapi
uvicorn[standard]
sqlalchemy
psycopg[binary]
httpx
pydantic
tenacity
alembic
```

## Execução

Para que a sincronização funcione, a API disponibilizada em `https://github.com/andrejr971/interview-test/` deve estar em execução.

Na pasta principal execute o comando `docker compose build` e então `docker compose up -d`, a API disponibilizada nesse projeto estará funcionando em `http://localhost:8000`.

Na primeira execução, execute `docker-compose exec -w /app api alembic revision --autogenerate -m "Initial migration"` para criar a migração inicial e `docker-compose exec -w /app api alembic upgrade head` para aplicá-la.

## Resumo da API

`POST /sync`: sincroniza dados com a API externa.

`GET /issues`: lista findings com paginação e filtros.

`GET /issues/{id}`: obtém um finding a partir de seu id.

`GET /metrics`: retorna as métricas dos findings.

A documentação da API está disponível em `http://localhost:8000/docs`.