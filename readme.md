# Mini Blog API

This is a simple blog API built with FastAPI and SQLAlchemy. It uses a SQLite database to store blog posts and comments. The endpoints uses Basic Authentication for authentication.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run the server

```bash
uvicorn main:app --reload
```

### Authenticate a user

```bash
curl -X 'POST' \
  'http://localhost:8000/auth/me' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic base64_encoded_user_credentials' \
  -d ''
```

### Create a new user

```bash
curl -X 'POST' \
  'http://localhost:8000/create-user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "User",
    "email": "user@example.com",
    "password": "12345678"
  }'
```

### Get all users

```bash
curl -X 'GET' \
  'http://localhost:8000/users' \
  -H 'accept: application/json'
```

### Create a new post

```bash
curl -X 'POST' \
  'http://localhost:8000/create-post' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic base64_encoded_user_credentials' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Title",
  "content": "Content"
}'
```

### Get all posts by user

```bash
curl -X 'GET' \
  'https://front-basic-auth-api.vercel.app/posts' \
  -H 'accept: application/json' \
  -H 'Authorization: Basic base64_encoded_user_credentials'
```