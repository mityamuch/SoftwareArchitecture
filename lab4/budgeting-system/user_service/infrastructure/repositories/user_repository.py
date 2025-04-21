from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.user import User
from infrastructure.database_init import DBUser, SessionLocal
from security.auth import hash_password 

class UserRepository:
    def __init__(self):
        self.db: Session = SessionLocal()

    def get_all_users(self) -> List[User]:
        db_users = self.db.query(DBUser).all()
        return [User(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            age=user.age
        ) for user in db_users]

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        if db_user:
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                age=db_user.age
            )
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        db_user = self.db.query(DBUser).filter(DBUser.username == username).first()
        if db_user:
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                age=db_user.age
            )
        return None

    def create_user(self, user: User) -> User:
        if self.db.query(DBUser).filter(DBUser.username == user.username).first():
            raise ValueError("username already exists")
        if self.db.query(DBUser).filter(DBUser.email == user.email).first():
            raise ValueError("email already exists")
        hash = hash_password(user.hashed_password)
        db_user = DBUser(
            username=user.username,
            email=user.email,
            hashed_password=hash,
            age=user.age
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            age=db_user.age
        )

    def update_user(self, user_id: int, updated_user: User) -> Optional[User]:
        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        if db_user:
            db_user.username = updated_user.username
            db_user.email = updated_user.email
            db_user.hashed_password = updated_user.hashed_password
            db_user.age = updated_user.age
            self.db.commit()
            self.db.refresh(db_user)
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                age=db_user.age
            )
        return None

    def delete_user(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                age=db_user.age
            )
        return None