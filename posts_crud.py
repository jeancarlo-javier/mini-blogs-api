from sqlalchemy.orm import Session
from models import Post
from auth import verify_user_credentials

def get_all_posts(session: Session):
    return session.query(Post).all()

def get_post_by_id(session: Session, post_id: int, credentials):
    verify_user_credentials(session, credentials.username, credentials.password)
    
    return session.query(Post).filter(Post.id == post_id).first()

def create_post(session: Session, post, credentials):
    user = verify_user_credentials(session, credentials.username, credentials.password)

    new_post = Post(user_id=user['id'], title=post.title, content=post.content)

    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post

def get_app_post_by_user(session: Session, credentials):
    user = verify_user_credentials(session, credentials.username, credentials.password)

    return session.query(Post).filter(Post.user_id == user['id']).all()
