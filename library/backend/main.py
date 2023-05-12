from fastapi import FastAPI

import logging
import uvicorn

from backend.routes import router
from backend.db.db import init_db as inicialization_database


app = FastAPI()



origins = ["*"]
app.add_middleware(
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

app.include_router(router)
@app.get("/")
async def root():
    return {"message": "Hello world!"}


if __name__ == '__main__':
    inicialization_database()
    uvicorn.run(app, host="0.0.0.0", port=8000)