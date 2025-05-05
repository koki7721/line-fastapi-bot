# ─────────────────────────────────────────
# main.py  ― LINE Messaging API × FastAPI
# （最小構成のサンプルボット）
# ─────────────────────────────────────────
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# ↓ ここの import に TextSendMessage を **必ず** 含める
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
)

import os
import re

app = FastAPI()

# ── 環境変数からチャネル情報を取得 ─────────────
bot_api  = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler  = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ── ヘルスチェック用エンドポイント ───────────
@app.get("/")
def healthcheck():
    return {"status": "ok"}

# ── LINE Webhook 受信エンドポイント ──────────
@app.post("/api/callback", response_class=PlainTextResponse)
async def callback(request: Request):
    signature = request.headers.get("X-Line-Signature", "")
    body      = await request.body()
    body_text = body.decode("utf-8")

    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Bad signature")

    return "OK"

# ── メッセージイベントハンドラ ───────────────
@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    msg = event.message.text.strip().lower()

    # 1) ping-pong テスト
    if msg == "ping":
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="pong")
        )
        return

    # 2) 不動産ボット簡易ロジック（例）
    if msg == "物件":
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ご希望エリアを教えてください！（例：大阪市北区）")
        )
        return

    if re.match(r".*(区|市)$", msg):
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ご予算を教えてください！（例：3000万円）")
        )
        return

    # 3) デフォルト応答
    bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="入力内容を確認できませんでした🤖")
    )
# --- dummy change (build trigger) ---
