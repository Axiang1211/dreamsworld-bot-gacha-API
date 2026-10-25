// DreamsWorld 抽卡記錄 API · Node.js 範例（Node 18 以上，內建 fetch）
//
// 用法：
//   export DREAMSWORLD_API_KEY="dwf_你的金鑰"
//   node node_example.js <Discord 使用者 ID>
//
// ⚠️ 這段程式要跑在你的伺服器上，不要把金鑰放進瀏覽器端的 JavaScript。

const BASE_URL = "https://dcplay.dreamsworld.top";
const API_KEY = process.env.DREAMSWORLD_API_KEY || "";

async function fetchPage(kind, userId, page = 1, perPage = 100) {
  // kind = "gacha"（抽卡記錄）或 "summon"（精靈召喚記錄）
  const qs = new URLSearchParams({ user_id: userId, page: String(page), per_page: String(perPage) });
  const res = await fetch(`${BASE_URL}/api/v1/${kind}_history?${qs}`, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(`HTTP ${res.status}：${data.error || "未知錯誤"}`);
  return data;
}

async function fetchAll(kind, userId) {
  const records = [];
  for (let page = 1; ; page++) {
    const data = await fetchPage(kind, userId, page);
    records.push(...data.records);
    if (page >= data.pages) return records;
    await new Promise((r) => setTimeout(r, 600)); // 每分鐘最多 120 次
  }
}

async function main() {
  if (!API_KEY.startsWith("dwf_")) throw new Error("請先設定環境變數 DREAMSWORLD_API_KEY");
  const userId = process.argv[2];
  if (!userId) throw new Error("用法：node node_example.js <Discord 使用者 ID>");
  const summons = await fetchAll("summon", userId);
  const count = summons.reduce((m, s) => ((m[s.grade] = (m[s.grade] || 0) + 1), m), {});
  console.log(`90 天內精靈召喚 ${summons.length} 次：`, count);
}

main().catch((e) => { console.error(e.message); process.exit(1); });
