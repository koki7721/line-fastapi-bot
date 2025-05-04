from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"status":"ok"}

@app.post("/callback")
async def callback():
    return {"status":"ok"}
