import logging
import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.create_user import create_first_user

from backend.core.db_settings import initialization_database


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

@app.on_event("startup")
async def startup_event():
    initialization_database()
    create_first_user()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
