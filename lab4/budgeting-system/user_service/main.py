from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import text
from infrastructure.database_init import init_db, SessionLocal
from api.endpoints.user_endpoints import router as user_router
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1 FROM users LIMIT 1"))
        db.commit()
    except Exception as e:
        raise RuntimeError(f"Database initialization failed: {str(e)}")
    finally:
        db.close()
    
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)