from fastapi import FastAPI
from infrastructure.repositories.user_repository import UserRepository
from api.endpoints.user_endpoints import router as user_router

app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)