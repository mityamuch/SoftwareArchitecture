from typing import List, Optional
from domain.models.user import User

class UserRepository:
    def __init__(self):
        self.users_db = []

    def get_all_users(self) -> List[User]:
        return self.users_db

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        for user in self.users_db:
            if user.id == user_id:
                return user
        return None

    def create_user(self, user: User) -> User:
        self.users_db.append(user)
        return user

    def update_user(self, user_id: int, updated_user: User) -> Optional[User]:
        for index, user in enumerate(self.users_db):
            if user.id == user_id:
                self.users_db[index] = updated_user
                return updated_user
        return None

    def delete_user(self, user_id: int) -> Optional[User]:
        for index, user in enumerate(self.users_db):
            if user.id == user_id:
                return self.users_db.pop(index)
        return None