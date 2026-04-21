# Blog API (FastAPI + PostgreSQL)

Simple REST API to manage blogs using FastAPI and PostgreSQL.

## Features

* Create, Read, Update, Delete Blogs

## Setup

```bash id="zbpkso"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

```id="abzi6f"
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
DB_NAME=blogdb
```

## Run

```bash id="b1z82w"
uvicorn app.main:app --reload
```

## Endpoints

* GET `/blogs/`
* POST `/blogs/`
* GET `/blogs/{id}`
* PUT `/blogs/{id}`
* DELETE `/blogs/{id}`

## Docs

http://127.0.0.1:8000/docs

## Author

Aniket Gupta
