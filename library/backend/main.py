import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.routes import router
from backend.db.db import init_db as initialization_database


app = FastAPI()



origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

app.include_router(router)
@app.get("/")
async def root():
    initialization_database()
    return {"message": "Hello world!"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)