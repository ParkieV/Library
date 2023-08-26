import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import Base  # noqa: F401

from app.core.db_conn import check_connection
from app.routes.api import api_router

app = FastAPI()


origins = ["http://localhost:3000"]
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["GET", "PUT", "POST", "DELETE"],
	allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origins", "Authorization"],
)


@app.on_event("startup")
async def startup_event():
	await check_connection()


app.include_router(api_router)


@app.get("/")
async def root():
	return {"message": "Hello world!"}

if __name__ == '__main__':
	uvicorn.run(app, host="0.0.0.0", port=8000)
