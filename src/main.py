import uvicorn
from fastapi import FastAPI

from api.v1 import router
from core.container import Container


def create_container() -> Container:
    return Container()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    app.state.container = create_container()

    return app


app = create_app()


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)
