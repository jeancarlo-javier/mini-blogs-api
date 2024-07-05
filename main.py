from fastapi import FastAPI, Depends, HTTPException, status, Request
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

origins = [
    "https://mini-blogs-wine.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request headers: {request.headers}")
    response = await call_next(request)
    print(f"Response headers: {response.headers}")
    return response

# @app.options("/{path:path}")
# def preflight_request(path: str):
#     return {"status": "ok"}

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
