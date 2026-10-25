"""
DreamsWorld 抽卡記錄 API · Python 範例（只用標準函式庫）

用法：
    export DREAMSWORLD_API_KEY="dwf_你的金鑰"
    python python_example.py <Discord 使用者 ID>
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = "https://dcplay.dreamsworld.top"
API_KEY = os.environ.get("DREAMSWORLD_API_KEY", "")


def fetch_page(kind: str, user_id: str, page: int = 1, per_page: int = 100) -> dict:
    """kind = "gacha"（抽卡記錄）或 "summon"（精靈召喚記錄）"""
    qs = urllib.parse.urlencode({"user_id": user_id, "page": page, "per_page": per_page})
    req = urllib.request.Request(f"{BASE_URL}/api/v1/{kind}_history?{qs}",
                                 headers={"Authorization": f"Bearer {API_KEY}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as exc:
        body = json.loads(exc.read() or b"{}")
        raise RuntimeError(f"HTTP {exc.code}：{body.get('error')}") from None


def fetch_all(kind: str, user_id: str) -> list:
    """把 90 天內的記錄全部抓下來（新到舊）。"""
    records, page = [], 1
    while True:
        data = fetch_page(kind, user_id, page)
        records.extend(data["records"])
        if page >= data["pages"]:
            return records
        page += 1
        time.sleep(0.6)  # 每分鐘最多 120 次，慢慢抓


def main():
    if not API_KEY.startswith("dwf_"):
        sys.exit("請先設定環境變數 DREAMSWORLD_API_KEY")
    if len(sys.argv) < 2:
        sys.exit("用法：python python_example.py <Discord 使用者 ID>")
    user_id = sys.argv[1]
    pulls = fetch_all("gacha", user_id)
    if not pulls:
        print("這位玩家 90 天內沒有抽卡記錄")
        return
    five = [p for p in pulls if p["stars"] >= 5]
    print(f"90 天內共 {len(pulls)} 抽，5★ {len(five)} 次（{len(five) / len(pulls):.2%}）")
    print(f"最新一抽是距離上次 5★ 的第 {pulls[0]['pull_no5']} 抽")
    for p in five[:10]:
        print(f"  {p['time']}  {p['item_name']}（第 {p['pull_no5']} 抽出貨）")


if __name__ == "__main__":
    main()
