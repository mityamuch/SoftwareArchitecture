import time
from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.user import User
from infrastructure.database_init import DBUser, SessionLocal
from security.auth import hash_password 
import redis
import json
import os

class UserRepository:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.redis_client = redis.from_url("redis://cache:6379/0", decode_responses=True)
        self.redis_client.ping()
        self.user_cache_prefix = "user:"
        self.all_users_key = "all_users"

    def _user_to_dict(self, user: User) -> dict:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "age": user.age
        }

    def _dict_to_user(self, user_dict: dict) -> User:
        return User(
            id=user_dict["id"],
            username=user_dict["username"],
            email=user_dict["email"],
            hashed_password=user_dict["hashed_password"],
            age=user_dict["age"]
        )

    def get_all_users(self) -> List[User]:
        cached_users = self.redis_client.get(self.all_users_key)
        if cached_users:
            return [self._dict_to_user(user_dict) for user_dict in json.loads(cached_users)]
        
        db_users = self.db.query(DBUser).all()
        users = [User(
            id=user.id,
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
            age=user.age
        ) for user in db_users]
        
        self.redis_client.setex(
            self.all_users_key,
            3600,  # TTL 1 час
            json.dumps([self._user_to_dict(user) for user in users])
        )
        return users

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        cache_key = f"{self.user_cache_prefix}{user_id}"
        cached_user = self.redis_client.get(cache_key)
        if cached_user:
            return self._dict_to_user(json.loads(cached_user))

        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        if not db_user:
            return None
            
        user = User(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            age=db_user.age
        )
        self.redis_client.setex(
            cache_key,
            3600,  # TTL 1 час
            json.dumps(self._user_to_dict(user))
        )
        return user
    
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
        self.redis_client.delete(self.all_users_key)
        
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
            
            cache_key = f"{self.user_cache_prefix}{user_id}"
            user = User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                age=db_user.age
            )
            self.redis_client.setex(
                cache_key,
                3600,
                json.dumps(self._user_to_dict(user))
            )
            
            self.redis_client.delete(self.all_users_key)
            
            return user
        return None

    def delete_user(self, user_id: int) -> Optional[User]:
        db_user = self.db.query(DBUser).filter(DBUser.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            cache_key = f"{self.user_cache_prefix}{user_id}"
            self.redis_client.delete(cache_key)
            
            self.redis_client.delete(self.all_users_key)
            
            return User(
                id=db_user.id,
                username=db_user.username,
                email=db_user.email,
                hashed_password=db_user.hashed_password,
                age=db_user.age
            )
        return None