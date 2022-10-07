from fastapi import FastAPI
from views import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def say_hello():
    return {"Say": "Hello There!"}
