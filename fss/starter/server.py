from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def healthz():
    return {"code": 0, "msg": "healthy"}


def run() -> None:
    uvicorn.run(app, host="0.0.0.0")
