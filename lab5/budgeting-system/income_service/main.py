from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.budget_endpoints import router as budget_router
from init_db import init_test_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_test_data()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(budget_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
