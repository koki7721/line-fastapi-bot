from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/api/callback")  # ← LINEに合わせた正しいエンドポイント
async def callback(request: Request):
    body = await request.body()
    print(body)  # 後で本処理追加できます
    return {"status": "ok"}