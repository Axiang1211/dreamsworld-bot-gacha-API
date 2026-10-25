# DreamsWorld 農場機器人 · 抽卡記錄 API

讓你的網站、Discord 機器人或 APP 讀取 **DreamsWorld 農場機器人**玩家的抽卡記錄與精靈召喚記錄，
可以用來做出金率統計、保底進度、歐非排行等等。

> 使用 API 之前，請先閱讀並同意 **[使用條款（使用要求、隱私權、停用權利）](./TERMS.md)**。
> DreamsWorld 保留隨時停用任何金鑰的權利。

---

## 目錄

1. [申請金鑰](#1-申請金鑰)
2. [驗證方式](#2-驗證方式)
3. [接口](#3-接口)
4. [回傳格式](#4-回傳格式)
5. [錯誤碼](#5-錯誤碼)
6. [使用限制](#6-使用限制)
7. [範例程式](#7-範例程式)
8. [常見問題](#8-常見問題)

---

## 1. 申請金鑰

金鑰要透過 Discord 向機器人申請，由管理員人工審核：

1. 在 Discord **私訊 DreamsWorld 農場機器人**，輸入 `/api_keys`。
   （如果斜線指令沒有跳出來，直接打字送出 `/api_keys` 也可以。）
2. 機器人會回一張卡片，上面寫著**使用要求、隱私權與停用權利**。讀完之後按
   **「✅ 我已閱讀並同意，開始申請」**（不按同意就無法申請）。
3. 填寫申請表：
   | 欄位 | 說明 |
   | --- | --- |
   | 專案 / 服務名稱 | 你的網站或機器人叫什麼 |
   | 網站 | 要用 `https://` 或 `http://` 開頭的完整網址 |
   | 聯絡 Email | 有問題時聯絡你用 |
   | 用途說明 | 你要拿抽卡記錄做什麼（至少 10 個字） |
   | 備註（選填） | 預計呼叫量、其他聯絡方式等 |
4. 送出後等待審核。通過時，機器人會**私訊**把金鑰發給你；沒通過也會私訊通知你原因。

> ⚠️ 請保持 Discord「允許來自伺服器成員的私訊」開啟，不然金鑰會發不出去。
> 完整金鑰**只會出現在那一則私訊裡一次**，我們只保存無法還原的雜湊值，弄丟了只能重新申請。

每個人同一時間只能有一筆申請在審核中，24 小時內最多送出 3 次申請。

---

## 2. 驗證方式

金鑰的格式是 `dwf_` 開頭的一串字。每次呼叫都要放在 HTTP Header 裡，以下兩種擇一：

```http
Authorization: Bearer dwf_xxxxxxxxxxxxxxxxxxxxxxxx
```

```http
X-API-Key: dwf_xxxxxxxxxxxxxxxxxxxxxxxx
```

> 🔒 **金鑰只能放在你的伺服器端**。不要寫進網頁前端 JavaScript、APP 原始碼或公開的 GitHub 倉庫。

---

## 3. 接口

Base URL：`https://dcplay.dreamsworld.top`

| 方法 | 路徑 | 說明 |
| --- | --- | --- |
| `GET` | `/api/v1/gacha_history` | 抽卡記錄（`/gacha` 的每一抽） |
| `GET` | `/api/v1/summon_history` | 精靈召喚記錄（森林深處的祈願，跟抽卡記錄分開） |

### 查詢參數

`user_id` 跟 `email` **擇一**：

| 參數 | 必填 | 說明 |
| --- | --- | --- |
| `user_id` | 擇一 | 玩家的 Discord 使用者 ID（例如 `123456789012345678`），或網頁帳號的 `web:…` ID |
| `email` | 擇一 | 玩家網頁版帳號的登入 Email。網頁帳號綁定 Discord 之後，用 Email 查也會對到同一個玩家 |
| `page` | 否 | 第幾頁，預設 `1`（第 1 頁 = 最新的記錄） |
| `per_page` | 否 | 每頁幾筆，預設 `20`，最多 `100` |

> 只會回傳**最近 3 個月（90 天）**的記錄。更舊的記錄已經封存，API 拿不到。
> 記錄由**新到舊**排列。

### 範例請求

```bash
curl -H "Authorization: Bearer dwf_你的金鑰" \
  "https://dcplay.dreamsworld.top/api/v1/gacha_history?user_id=123456789012345678&page=1&per_page=20"
```

---

## 4. 回傳格式

### 抽卡記錄 `GET /api/v1/gacha_history`

```json
{
  "ok": true,
  "account": { "user_id": "123456789012345678", "nickname": "小明" },
  "kind": "gacha",
  "page": 1,
  "pages": 3,
  "per_page": 20,
  "total": 47,
  "first_no": 47,
  "since": "2026-07-27T12:00:00",
  "retention_days": 90,
  "records": [
    {
      "id": 1024,
      "time": "2026-10-25T08:15:02",
      "batch_id": "a1b2c3d4e5f6",
      "batch_size": 10,
      "seq": 3,
      "item_key": "spirit_owl",
      "item_name": "守護貓頭鷹",
      "item_type": "spirit",
      "stars": 4,
      "is_new": true,
      "stones": 0,
      "pull_no4": 7,
      "pull_no5": 31,
      "cost": 100
    }
  ]
}
```

| 欄位 | 說明 |
| --- | --- |
| `account` | 查到的玩家（`user_id`、暱稱） |
| `page` / `pages` / `per_page` / `total` | 分頁資訊；`total` 是 90 天內的總筆數 |
| `first_no` | 這一頁第一筆是這位玩家 90 天內的「第幾抽」（由舊到新數） |
| `since` | 最早能查到的時間（再早的已封存） |
| `records[].time` | 抽卡時間（ISO 8601，伺服器時間） |
| `records[].batch_id` | 同一次抽卡共用的編號（10 連抽 = 10 筆同一個 `batch_id`） |
| `records[].batch_size` / `seq` | 那次抽了幾抽 / 這是其中第幾抽 |
| `records[].item_key` / `item_name` | 抽到的東西（固定代號 / 顯示名稱） |
| `records[].item_type` | `spirit`（精靈）或 `seed`（種子） |
| `records[].stars` | 星級 1～5 |
| `records[].is_new` | 是否第一次抽到 |
| `records[].stones` | 重複時換成的突破石數量 |
| `records[].pull_no4` | 距離上一次 4★（含）以上的第幾抽 |
| `records[].pull_no5` | 距離上一次 5★ 的第幾抽（5★ 保底進度） |
| `records[].cost` | 這一抽花了多少金幣 |

### 精靈召喚記錄 `GET /api/v1/summon_history`

```json
{
  "ok": true,
  "account": { "user_id": "123456789012345678", "nickname": "小明" },
  "kind": "summon",
  "page": 1, "pages": 1, "per_page": 20, "total": 2, "first_no": 2,
  "since": "2026-07-27T12:00:00", "retention_days": 90,
  "records": [
    { "id": 88, "time": "2026-10-24T21:03:11", "grade": "S", "pull_no": 12, "cost": 500, "reward": null }
  ]
}
```

| 欄位 | 說明 |
| --- | --- |
| `records[].grade` | 召喚結果等級：`A`、`S`、`SS`、`SSS` |
| `records[].pull_no` | 距離上一次 SSS 的第幾次 |
| `records[].cost` | 消耗幾顆損毀的突破石 |
| `records[].reward` | 額外獎勵（沒有就是 `null`） |

---

## 5. 錯誤碼

錯誤時一律回傳 `{"ok": false, "error": "說明文字"}`。

| HTTP 狀態 | 意思 |
| --- | --- |
| `400` | `page` / `per_page` 不是數字 |
| `401` | 金鑰無效、已停用或沒帶金鑰 |
| `404` | 找不到這個玩家 / 沒提供 `user_id` 或 `email` / 路徑不對 |
| `429` | 請求太頻繁，請稍後再試 |

---

## 6. 使用限制

- 每把金鑰**每分鐘最多 120 次**請求，超過會回 `429`。請自行快取結果，不要一直輪詢。
- 只回傳最近 90 天的記錄。
- 每一次呼叫都會被記錄（時間、金鑰開頭、接口、查詢的帳號、結果、筆數、IP）。
- 只能查詢**已經同意讓你查詢**的玩家，詳見 [TERMS.md](./TERMS.md)。
- 違反條款，或我們認為有需要時，金鑰會被**直接停用**。

---

## 7. 範例程式

- Python：[`examples/python_example.py`](./examples/python_example.py)
- Node.js（18 以上）：[`examples/node_example.js`](./examples/node_example.js)

金鑰請放在環境變數 `DREAMSWORLD_API_KEY`，不要寫死在程式裡：

```bash
export DREAMSWORLD_API_KEY="dwf_你的金鑰"
python examples/python_example.py 123456789012345678
```

---

## 8. 常見問題

**Q：金鑰弄丟了 / 外洩了怎麼辦？**
A：私訊機器人或到 DreamsWorld Discord 社群通知我們停用，然後重新用 `/api_keys` 申請一把新的。

**Q：可以查超過 3 個月的記錄嗎？**
A：不行，超過 90 天的記錄已封存，只有管理員看得到。

**Q：玩家的 Discord ID 要怎麼拿？**
A：請讓玩家自己提供（例如在你的網站登入 Discord 授權），不要用猜的或批量掃描。

**Q：條款更新了怎麼辦？**
A：條款更新後繼續使用就代表同意新版本，請不定期回來看 [TERMS.md](./TERMS.md)。

---

DreamsWorld 農場 · Discord：https://discord.gg/FFMDQwdxnN · 網頁版：https://dcplay.dreamsworld.top
