import uvicorn
from fastapi import FastAPI

from api.v1 import router




def create_app() -> FastAPI:
    app = FastAPI(

    )
    app.include_router(router)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
