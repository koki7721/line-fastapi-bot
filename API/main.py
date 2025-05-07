from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import os
import re

app = FastAPI()

# 環境変数からLINEチャネルの情報を取得
bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ヘルスチェック用
@app.get("/")
def healthcheck():
    return {"status": "ok"}

# Webhook受信用エンドポイント
@app.post("/api/callback", response_class=PlainTextResponse)
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()
    body_text = body.decode("utf-8")

    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"

# メッセージイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip().lower()

    if text == "ping":
        reply = "pong"
    elif text == "物件":
        reply = "ご希望エリアを教えてください！（例：大阪市北区）"
    elif re.match(r".*(区|市)$", text):
        reply = "ご予算を教えてください！（例：3000万円）"
    else:
        reply = "入力内容を確認できませんでした。"

    bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# Vercel用エントリーポイント
def handler_entry(req, context):
    return app

