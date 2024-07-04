from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Session, get_db
from auth import verify_user_credentials
from typing import Annotated
import models
import schemas
import users_crud, posts_crud

models.Base.metadata.create_all(engine)

app = FastAPI()
security = HTTPBasic()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mini-blogs-wine.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{path:path}")
def preflight_request(path: str):
    return {"status": "ok"}

@app.post("/create-user")
def create_user(user: schemas.UserCreate):
    with Session() as session:
        new_user = users_crud.create_user(session, user)
        return new_user

@app.get("/users")
def get_users():
    with Session() as session:
        users = users_crud.get_users(session)
        return users

@app.post("/auth/me")
def get_user_me(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    with Session() as session:
        user = verify_user_credentials(session, email=credentials.username, password=credentials.password)
        return user

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    with Session() as session:
        user = users_crud.get_user_by_id(session, user_id, credentials)
        return user

@app.post("/create-post")
def create_post(post: schemas.PostCreate, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    with Session() as session:
        new_post = posts_crud.create_post(session, post, credentials)
        return new_post

@app.get("/posts")
def get_posts_by_user(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    with Session() as session:
        posts = posts_crud.get_app_post_by_user(session, credentials)
        return posts
