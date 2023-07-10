import uvicorn

from fastapi import FastAPI


from starlette.middleware.cors import CORSMiddleware

from backend.create_user import create_first_user

from backend.core.db_settings import initialization_database
from backend.routes.api_routes import api_router


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
    await initialization_database()
    # await create_first_user()


app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Hello world!"}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
