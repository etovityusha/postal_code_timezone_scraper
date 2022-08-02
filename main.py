import uvicorn
from fastapi import FastAPI

from database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("run:app", host='0.0.0.0', port=6100, reload=True)