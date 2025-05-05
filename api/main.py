from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os, re

app = FastAPI()

# ── 環境変数を読む ──────────────────────
bot_api  = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler  = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ── ヘルスチェック ───────────────────────
@app.get("/")
def healthcheck():
    return {"status": "ok"}

# ── LINE からのコールバック受信 ───────────
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

# ── メッセージハンドラ ────────────────────
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    msg = event.message.text.strip()

    # 動作テスト
    if msg == "ping":
        bot_api.reply_message(event.reply_token, TextSendMessage("pong"))
        return

    # 不動産 bot の簡易ロジック
    if msg == "物件":
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage("ご希望のエリアを教えてください！（例：大阪市北区）")
        )
        return

    if re.match(r".*(区|市)$", msg):
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage("ご予算を教えてください！（例：3000万円）")
        )
        return

    # デフォルト応答
    bot_api.reply_message(
        event.reply_token,
        TextSendMessage("入力内容を確認できませんでした💦")
    )
# － メッセージハンドラ ---------------
@handler.add(MessageEvent, message=TextMessage)
def handle_text(event):
    text = event.message.text.lower()

    if text == "ping":
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="pong"))
    else:
        bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「ping」と送ってみてください 😊"))
