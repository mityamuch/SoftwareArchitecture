from fastapi import FastAPI
from api.budget_endpoints import router as budget_router

app = FastAPI()

app.include_router(budget_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)