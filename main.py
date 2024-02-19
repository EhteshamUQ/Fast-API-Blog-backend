from fastapi import FastAPI
from db.session import create_tables
from routes import base_router
from utils.config import Configuration


def create_app():
    app = FastAPI(title=Configuration.PROJECT_TITLE)
    app.include_router(base_router)
    create_tables()
    return app


app = create_app()


@app.get("/status")
def get_status():
    return "Working"
