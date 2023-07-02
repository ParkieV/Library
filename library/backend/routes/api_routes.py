from backend.main import app
from fastapi import APIRouter


api_router = APIRouter(prefix="/api")

app.include_router(api_router)




@app.get("/")
async def root():
    return {"message": "Hello world!"}