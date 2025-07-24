from fastapi import APIRouter

app = APIRouter()

@app.get("/")
async def hello():
    return "hello"