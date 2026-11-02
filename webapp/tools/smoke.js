// End-to-end smoke test: opens every page of the app at phone and desktop sizes and drives each feature.
// Usage (needs Playwright + Chromium):  node webapp/tools/smoke.js [screenshot-dir]
// Fails (exit 1) on any page error, console error, horizontal scroll, or broken flow.
const { chromium } = require("playwright");
const path = require("path");
const http = require("http");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const SHOTS = process.argv[2];
const TYPES = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".webp": "image/webp", ".mp3": "audio/mpeg", ".png": "image/png", ".webmanifest": "application/manifest+json", ".md": "text/markdown" };

const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
  if (!p.startsWith(ROOT) || !fs.existsSync(p)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": TYPES[path.extname(p)] || "application/octet-stream" });
  fs.createReadStream(p).pipe(res);
});

(async () => {
  await new Promise((r) => server.listen(0, r));
  const base = `http://localhost:${server.address().port}/`;
  const chapters = JSON.parse(fs.readFileSync(path.join(ROOT, "data/chapters.json"))).chapters.map((c) => String(c.num).padStart(2, "0"));
  const tabs = ["words", "flash", "quiz", "listen", "speak", "order", "talk", "read"];
  const b = await chromium.launch();
  const problems = [];
  for (const [w, h, tag] of [[390, 844, "phone"], [1280, 900, "desktop"]]) {
    const ctx = await b.newContext({ viewport: { width: w, height: h } });
    const p = await ctx.newPage();
    p.on("pageerror", (e) => problems.push(`${tag} pageerror: ${e.message}`));
    p.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource|service worker|NotSupportedError/i.test(m.text())) problems.push(`${tag} console: ${m.text()}`); });
    const visit = async (hash) => {
      await p.goto(base + hash); await p.waitForTimeout(250);
      const over = await p.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (over > 1) problems.push(`${tag} ${hash}: horizontal scroll ${over}px`);
      const err = await p.$(".empty");
      if (err && /불러오지 못했/.test(await err.textContent())) problems.push(`${tag} ${hash}: load error`);
      if (SHOTS && (tag === "phone" || hash === "#/")) await p.screenshot({ path: path.join(SHOTS, `${tag}_${hash.replace(/[#/]+/g, "_") || "home"}.png`) });
    };
    for (const r of ["#/", "#/review", "#/mine", "#/settings", "#/credits", "#/search/toalla", "#/search/수건"]) await visit(r);
    for (const c of chapters) for (const t of tabs) await visit(`#/ch/${c}/${t}`);

    if (tag === "phone") {
      // quiz: answer 10 questions of each mode
      for (const mode of ["choice", "type", "gender", "mix"]) {
        await p.goto(base + "#/ch/01/quiz"); await p.click(`[data-qm="${mode}"]`);
        for (let i = 0; i < 10; i++) {
          if (await p.$("#ans")) { await p.fill("#ans", "la toalla"); await p.press("#ans", "Enter"); }
          else await p.click(".choice >> nth=0");
          await p.click("#next");
        }
        if (!(await p.$(".score"))) problems.push(`quiz ${mode}: did not finish`);
      }
      // dictation: one wrong, one exact
      await p.goto(base + "#/ch/02/listen");
      const target = await p.evaluate(() => document.querySelector("#big").dataset.say);
      await p.fill("#ans", target); await p.click("#dForm button[type=submit]");
      const sc = await p.textContent("#after .tag");
      if (sc.trim() !== "100점") problems.push(`dictation exact answer scored ${sc}`);
      await p.click("#next");
      await p.fill("#ans", "xxx"); await p.click("#dForm button[type=submit]");
      if ((await p.textContent("#after .tag")).trim() === "100점") problems.push("dictation wrong answer scored 100");
      // flashcards + review + my words
      await p.goto(base + "#/ch/03/flash");
      await p.click("#card"); await p.click("#no"); await p.click("#yes");
      await p.goto(base + "#/ch/03/read"); await p.waitForTimeout(200);
      const wEl = await p.$(".w:not(.nogl) >> nth=3"); await wEl.click(); await p.click("#saveWord");
      await p.goto(base + "#/mine");
      if (!(await p.$("[data-rm]"))) problems.push("my words: saved word not listed");
      await p.goto(base + "#/review"); await p.waitForTimeout(200);
      if (!(await p.$("#card"))) problems.push("review: no due card after a miss");
      // dialogue role play (no mic in headless: reveal path)
      await p.goto(base + "#/ch/07/talk"); await p.click("[data-role=B]");
      for (let i = 0; i < 12; i++) {
        await p.waitForTimeout(150);
        const rv = await p.$("#rp .reveal"); if (rv) { await rv.click(); await p.click("#rp .out .btn"); }
        if (await p.$("#again")) break;
        await p.evaluate(() => window.speechSynthesis && speechSynthesis.cancel());
      }
      // home dashboard reflects activity
      await p.goto(base + "#/"); await p.waitForTimeout(200);
      const todayN = await p.textContent(".dash .stat:nth-child(2) b");
      if (parseInt(todayN, 10) < 10) problems.push(`dashboard today count looks wrong: ${todayN}`);
    }
    await ctx.close();
  }
  await b.close(); server.close();
  if (problems.length) { console.log(problems.join("\n")); process.exit(1); }
  console.log(`smoke ok: ${chapters.length} chapters × ${tabs.length} tabs × 2 sizes + flows`);
})().catch((e) => { console.error(e); process.exit(1); });
