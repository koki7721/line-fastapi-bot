### 開発仕様（外注向け）

#### 🔹 エンドポイント要件
- `GET /api` → `{"status":"ok"}` を返す（ヘルスチェック用）
- `POST /api/callback` → LINE Webhook受信用エンドポイント（署名検証あり）

#### 🔹 Bot機能要件
- メッセージ `"ping"` → `"pong"` を返す
- メッセージ `"物件"` → `"対応エリアは〇〇です"` を返す
- メッセージ `"〇〇区" または "〇〇市"` → `"〇〇の物件はこちら"` を返す（エリア別固定文言）
- その他のメッセージ → `"申し訳ありません。別のキーワードでお試しください"` を返す

#### 🔹 .env の構成例（環境変数）
```env
LINE_CHANNEL_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxx
LINE_CHANNEL_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
