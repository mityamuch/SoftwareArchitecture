from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from domain.models.user import User
from infrastructure.repositories.user_repository import UserRepository
from security.auth import get_current_client, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, check_user



router = APIRouter()
user_repository = UserRepository()


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    password_check = check_user(form_data.username, form_data.password)
    if password_check:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get("/users", response_model=List[User])
def get_users(current_user: str = Depends(get_current_client)):
    return user_repository.get_all_users()

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, current_user: str = Depends(get_current_client)):
    user = user_repository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=User)
def create_user(user: User, current_user: str = Depends(get_current_client)):
    return user_repository.create_user(user)

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User, current_user: str = Depends(get_current_client)):
    user = user_repository.update_user(user_id, updated_user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, current_user: str = Depends(get_current_client)):
    user = user_repository.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user