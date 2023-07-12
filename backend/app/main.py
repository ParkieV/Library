import uvicorn

from fastapi import FastAPI


from starlette.middleware.cors import CORSMiddleware

from app.core.db_conn import check_connection
from app.routes.api import api_router


app = FastAPI()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
