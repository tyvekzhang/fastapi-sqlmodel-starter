from fastapi import FastAPI
import uvicorn

from fss.starter.modules.system.router.system_router import system_router

app = FastAPI()
app.include_router(system_router)


def run() -> None:
    uvicorn.run(app, host="0.0.0.0")
