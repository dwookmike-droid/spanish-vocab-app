/* Vocabulario visual — web app (no build step). Data: data/*.json, media: media/ */
"use strict";

const $app = document.getElementById("app");
const cache = {};
let index = null;

/* ---------- helpers ---------- */
const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pron = (p) => esc(p).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
const nn = (n) => String(n).padStart(2, "0");
const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const pick = (a, n) => shuffle(a).slice(0, n);
const norm = (s) => String(s).toLowerCase().normalize("NFC").replace(/[¿¡.,;:!?«»"“”()]/g, "").replace(/\s+/g, " ").trim();
const GENDER = { m: "m", f: "f", mpl: "m pl", fpl: "f pl" };
const img = (name, cls = "", alt = "") => name
  ? `<img class="${cls}" src="media/img/${name}_1x.webp" srcset="media/img/${name}_1x.webp 1x, media/img/${name}_2x.webp 2x" alt="${esc(alt)}" loading="lazy" decoding="async">`
  : "";

async function getJSON(url) {
  if (!cache[url]) cache[url] = fetch(url).then((r) => { if (!r.ok) throw new Error(url + " " + r.status); return r.json(); });
  return cache[url];
}
const getChapter = (n) => getJSON(`data/ch${nn(n)}.json`);

/* ---------- storage (per viewer, best effort) ---------- */
const store = {
  get(k, d) { try { const v = localStorage.getItem("vv." + k); return v ? JSON.parse(v) : d; } catch { return d; } },
  set(k, v) { try { localStorage.setItem("vv." + k, JSON.stringify(v)); } catch { /* private mode */ } },
};

/* ---------- spaced repetition (Leitner, 5 boxes) ---------- */
const DAY = 864e5;
const INTERVAL = [0, 1, 2, 4, 8, 16].map((d) => d * DAY);
const srs = {
  all() { return store.get("srs", {}); },
  get(id) { return this.all()[id]; },
  grade(id, ok) {
    const all = this.all();
    const c = all[id] || { box: 0 };
    c.box = ok ? Math.min(5, (c.box || 0) + 1) : 1;
    c.due = Date.now() + (ok ? INTERVAL[c.box] : 0); // missed cards are due right away
    c.seen = (c.seen || 0) + 1;
    all[id] = c;
    store.set("srs", all);
  },
  isKnown(id) { const c = this.get(id); return !!c && c.box >= 3; },
  dueIds() { const now = Date.now(); return Object.entries(this.all()).filter(([, c]) => c.due <= now).map(([id]) => id); },
};
const wid = (ch, w) => `${nn(ch)}:${w.key}`;

/* ---------- audio: v6 mp3 when present, browser TTS otherwise ---------- */
let rate = store.get("rate", 1);
const speedBtn = document.getElementById("speedBtn");
function paintSpeed() { speedBtn.textContent = rate === 1 ? "1×" : "0.75×"; speedBtn.setAttribute("aria-pressed", String(rate !== 1)); }
speedBtn.onclick = () => { rate = rate === 1 ? 0.75 : 1; store.set("rate", rate); paintSpeed(); };
paintSpeed();

const player = new Audio();
let esVoice = null;
function loadVoices() {
  if (!("speechSynthesis" in window)) return;
  const vs = speechSynthesis.getVoices();
  esVoice = vs.find((v) => v.lang === "es-ES") || vs.find((v) => v.lang && v.lang.startsWith("es")) || null;
}
if ("speechSynthesis" in window) { loadVoices(); speechSynthesis.onvoiceschanged = loadVoices; }

let playingBtn = null;
function stopAll() {
  player.pause();
  if ("speechSynthesis" in window) speechSynthesis.cancel();
  if (playingBtn) playingBtn.classList.remove("on");
  playingBtn = null;
}
function speak(text, file, btn) {
  return new Promise((resolve) => {
    stopAll();
    if (btn) { btn.classList.add("on"); playingBtn = btn; }
    const done = () => { if (btn) btn.classList.remove("on"); resolve(); };
    if (file) {
      player.src = "media/audio/" + file;
      player.playbackRate = rate;
      player.onended = done; player.onerror = () => tts(text, done);
      player.play().catch(() => tts(text, done));
    } else tts(text, done);
  });
}
function tts(text, done) {
  if (!("speechSynthesis" in window)) { done(); return; }
  const u = new SpeechSynthesisUtterance(text);
  u.lang = "es-ES"; if (esVoice) u.voice = esVoice; u.rate = rate === 1 ? 0.95 : 0.7;
  u.onend = done; u.onerror = done;
  speechSynthesis.speak(u);
}
const playBtn = (text, file, small = false) =>
  `<button class="play${small ? " s" : ""}${file ? "" : " tts"}" type="button" data-say="${esc(text)}" data-file="${esc(file || "")}" aria-label="듣기">▶</button>`;

/* ---------- tappable words + bottom sheet ---------- */
const SPLIT = /([\s.,;:!?¡¿«»"“”()—–…/]+)/;
function lookup(ch, raw) {
  const k = raw.toLowerCase().replace(/^['’-]+|['’-]+$/g, "");
  const g = ch.glossary;
  if (g[k]) return g[k];
  // a single word that belongs to a multi-word chapter entry (e.g. "cepillo" in "cepillo de dientes")
  return ch.words.find((w) => (w.base || "").toLowerCase().split(" ").includes(k)) || null;
}
function tappable(ch, text) {
  return text.split(SPLIT).map((part) => {
    if (!part || SPLIT.test(part) || /^\d/.test(part)) return esc(part);
    const has = lookup(ch, part);
    return `<span class="w${has ? "" : " nogl"}" data-w="${esc(part)}">${esc(part)}</span>`;
  }).join("");
}
const sheet = document.getElementById("sheet");
const sheetBody = document.getElementById("sheetBody");
function openSheet(ch, word, el) {
  const e = lookup(ch, word);
  if (!e) return;
  document.querySelectorAll(".w.sel").forEach((x) => x.classList.remove("sel"));
  el && el.classList.add("sel");
  const chw = e.key ? ch.words.find((w) => w.key === e.key) : null;
  const say = chw ? chw.es : word;
  sheetBody.innerHTML = `
    ${chw ? img(chw.img, "", chw.en) : ""}
    <div class="row"><span class="es" id="sheetWord">${esc(chw ? chw.es : word)}</span>${playBtn(say, chw ? chw.audio : null)}</div>
    ${e.lemma && norm(e.lemma) !== norm(word) && !chw ? `<div class="lemma">기본형: ${esc(e.lemma)}</div>` : ""}
    <div class="pron">[${pron(e.pron || "")}]</div>
    <div class="mean">${esc(e.ko || "")}</div>
    <div class="muted small">${esc(e.en || "")}</div>
    ${chw ? `<div class="muted small" style="margin-top:6px">이 장의 단어예요 · ${chw.core ? "핵심" : "보조"}</div>` : ""}`;
  sheet.hidden = false;
  sheet.querySelector(".sheet-x").focus();
}
function closeSheet() { sheet.hidden = true; document.querySelectorAll(".w.sel").forEach((x) => x.classList.remove("sel")); }
sheet.addEventListener("click", (e) => { if (e.target === sheet || e.target.closest(".sheet-x")) closeSheet(); });
document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !sheet.hidden) closeSheet(); });

/* global click delegation for play buttons + tappable words */
let currentChapter = null;
document.addEventListener("click", (e) => {
  const p = e.target.closest(".play");
  if (p) { e.preventDefault(); e.stopPropagation(); speak(p.dataset.say, p.dataset.file, p); return; }
  const w = e.target.closest(".w");
  if (w && currentChapter && !w.classList.contains("nogl")) openSheet(currentChapter, w.dataset.w, w);
});

/* ---------- router ---------- */
const TABS = [
  ["words", "단어"], ["flash", "플래시카드"], ["quiz", "퀴즈"], ["order", "어순"], ["talk", "대화"], ["read", "읽기"],
];
async function route() {
  stopAll(); closeSheet();
  const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  try {
    index = index || await getJSON("data/chapters.json");
    if (parts[0] === "ch" && parts[1]) {
      const ch = await getChapter(parseInt(parts[1], 10));
      currentChapter = ch;
      const tab = TABS.some(([k]) => k === parts[2]) ? parts[2] : "words";
      renderChapter(ch, tab);
    } else if (parts[0] === "review") { currentChapter = null; await renderReview(); }
    else if (parts[0] === "credits") { currentChapter = null; await renderCredits(); }
    else { currentChapter = null; renderHome(); }
  } catch (err) {
    $app.innerHTML = `<p class="empty">불러오지 못했어요: ${esc(err.message)}</p>`;
  }
  updateReviewBadge();
  $app.focus({ preventScroll: true });
  window.scrollTo(0, 0);
}
window.addEventListener("hashchange", route);

function updateReviewBadge() {
  const n = srs.dueIds().length;
  document.getElementById("reviewLink").textContent = n ? `복습 ${n}` : "복습";
}

/* ---------- home ---------- */
function renderHome() {
  const all = srs.all();
  const due = srs.dueIds().length;
  const cards = index.chapters.map((c) => {
    const known = Object.entries(all).filter(([id, v]) => id.startsWith(nn(c.num) + ":") && v.box >= 3).length;
    return `<a class="chcard" href="#/ch/${nn(c.num)}">
      <div class="pic">${c.cover ? img(c.cover, "", "") : `<span class="num">${nn(c.num)}</span>`}</div>
      <div class="meta">
        <div class="n">${nn(c.num)} · ${esc(c.city)} · ${esc(c.date)}</div>
        <div class="t">${esc(c.es)}</div>
        <div class="k">${esc(c.ko)}</div>
        <div class="bar" title="외운 단어 ${known}/20"><i style="width:${known * 5}%"></i></div>
      </div></a>`;
  }).join("");
  $app.innerHTML = `
    <section class="hero">
      <h1>사진으로 배우는 여행 스페인어</h1>
      <p>그라나다에서 마드리드까지, 장소마다 20단어. 단어 카드로 보고, 대화와 짧은 글로 써 보고, 어순 블록으로 문장을 만들어요.</p>
    </section>
    <div class="review-cta">
      <div><b>오늘 복습할 카드 ${due}장</b><div class="muted small">플래시카드·퀴즈에서 본 단어가 간격을 두고 다시 나와요.</div></div>
      <a class="btn${due ? "" : " ghost"}" href="#/review">${due ? "복습 시작" : "복습함 보기"}</a>
    </div>
    <div class="chgrid">${cards}</div>
    <p class="muted small" style="margin-top:20px">▶ 버튼은 스페인 표준 발음이에요. 테두리가 옅은 ▶는 기기에 내장된 음성으로 읽어 줘요. 진도는 이 브라우저에만 저장돼요.</p>`;
}

/* ---------- chapter shell ---------- */
function renderChapter(ch, tab) {
  const tabs = TABS.map(([k, label]) => `<a href="#/ch/${nn(ch.num)}/${k}"${k === tab ? ' aria-current="page"' : ""}>${label}</a>`).join("");
  $app.innerHTML = `
    <div class="chhead"><h1>${nn(ch.num)} · ${esc(ch.es)}</h1><span class="city">${esc(ch.ko)} · ${esc(ch.city)} · ${esc(ch.date)}</span></div>
    <nav class="tabs" aria-label="학습 메뉴">${tabs}</nav>
    <section id="pane"></section>`;
  const pane = document.getElementById("pane");
  ({ words: paneWords, flash: paneFlash, quiz: paneQuiz, order: paneOrder, talk: paneTalk, read: paneRead })[tab](ch, pane);
}

/* ---------- 단어 카드 ---------- */
function wordCard(ch, w) {
  return `<article class="wcard">
    ${w.core ? '<span class="core">핵심</span>' : ""}
    ${playBtn(w.es, w.audio)}
    ${w.img ? `<div class="im">${img(w.img, "", w.en)}</div>` : ""}
    <div class="es">${esc(w.es)}${w.gender && GENDER[w.gender] ? `<span class="g">${GENDER[w.gender]}</span>` : ""}</div>
    <div class="pron">[${pron(w.pron)}]</div>
    <div class="mean">${esc(w.en)} · ${esc(w.ko)}</div>
    ${w.note ? `<div class="note">${esc(w.note)}</div>` : ""}
    ${srs.isKnown(wid(ch.num, w)) ? '<div class="known">✓ 외웠어요</div>' : ""}
    ${w.example ? `<div class="ex">${playBtn(w.example.es, w.example.audio, true)}<div><div>${tappable(ch, w.example.es)}</div><div class="ko">${esc(w.example.ko)}</div></div></div>` : ""}
  </article>`;
}
function paneWords(ch, pane) {
  const filt = store.get("wordFilter", "all");
  const hide = store.get("hideKo", false);
  const list = ch.words.filter((w) => filt === "all" || (filt === "core" ? w.core : !srs.isKnown(wid(ch.num, w))));
  pane.innerHTML = `
    <div class="toolbar">
      <div class="seg" role="group" aria-label="보기">
        <button data-f="all" aria-pressed="${filt === "all"}">전체 20</button>
        <button data-f="core" aria-pressed="${filt === "core"}">핵심 8</button>
        <button data-f="todo" aria-pressed="${filt === "todo"}">아직 못 외운 것</button>
      </div>
      <label class="small"><input type="checkbox" id="hideKo" ${hide ? "checked" : ""}> 뜻 가리기</label>
      <button class="btn ghost" id="playAll" type="button">▶ 전체 듣기</button>
    </div>
    <div class="wgrid">${list.map((w) => wordCard(ch, w)).join("") || '<p class="empty">이 장 단어를 모두 외웠어요.</p>'}</div>
    ${extrasBlock(ch)}`;
  pane.querySelectorAll(".seg button").forEach((b) => b.onclick = () => { store.set("wordFilter", b.dataset.f); paneWords(ch, pane); });
  const applyHide = (on) => pane.querySelectorAll(".wcard").forEach((c) => c.classList.toggle("hide-ko", on));
  applyHide(hide);
  pane.querySelector("#hideKo").onchange = (e) => { store.set("hideKo", e.target.checked); applyHide(e.target.checked); };
  pane.querySelectorAll(".wcard").forEach((c) => c.addEventListener("click", (e) => {
    if (c.classList.contains("hide-ko") && e.target.closest(".mean,.ko")) c.classList.remove("hide-ko");
  }));
  let stop = false;
  pane.querySelector("#playAll").onclick = async (e) => {
    const b = e.currentTarget;
    if (b.dataset.on) { stop = true; stopAll(); return; }
    stop = false; b.dataset.on = "1"; b.textContent = "■ 멈춤";
    for (const w of list) { if (stop || !document.body.contains(b)) break; await speak(w.es, w.audio); await new Promise((r) => setTimeout(r, 500)); }
    delete b.dataset.on; b.textContent = "▶ 전체 듣기";
  };
}
function extrasBlock(ch) {
  const x = ch.extras || {};
  let h = "";
  if (ch.scenes.length) {
    h += `<h2>Escenas · 장면 문장</h2>` + ch.scenes.map((s) => `<div class="line">${playBtn(s.es, s.audio)}<div><div class="es2">${tappable(ch, s.es)}</div><div class="t">${esc(s.ko)}</div></div></div>`).join("");
  }
  if (ch.variants.length) {
    h += `<h3>스페인 vs 중남미</h3><div class="panel"><ul class="plain">${ch.variants.map((v) => `<li><b>${esc(v.es)}</b> → ${esc(v.alt)}</li>`).join("")}</ul></div>`;
  }
  if ((x.grammar_ko || []).length) h += `<h3>문법 메모</h3><div class="panel"><ul class="plain">${x.grammar_ko.map((g) => `<li>${esc(g)}</li>`).join("")}</ul></div>`;
  if ((x.cognates || []).length) h += `<h3>영어와 닮은 말</h3><div class="panel"><ul class="plain">${x.cognates.map((c) => `<li><b>${esc(c.es)}</b> ≈ ${esc(c.en)} — ${esc(c.note_ko)}</li>`).join("")}</ul></div>`;
  if (x.false_friend) h += `<h3>헷갈리는 말</h3><div class="panel"><b>${esc(x.false_friend.es)}</b> ≠ ${esc(x.false_friend.en)} — ${esc(x.false_friend.note_ko)}</div>`;
  if (x.fun_fact_ko) h += `<h3>알아 두면 좋은 것</h3><div class="panel">${esc(x.fun_fact_ko)}</div>`;
  return h;
}

/* ---------- 플래시카드 ---------- */
function buildDeck(entries, limitNew = 12) {
  // entries: [{ch, w}] ; due first, then unseen, then the rest
  const now = Date.now();
  const due = [], fresh = [], later = [];
  for (const e of entries) {
    const c = srs.get(wid(e.ch.num, e.w));
    if (!c) fresh.push(e); else if (c.due <= now) due.push(e); else later.push(e);
  }
  return [...shuffle(due), ...fresh.slice(0, limitNew)];
}
function flashSession(pane, entries, opts = {}) {
  const dir = store.get("flashDir", "es2ko");
  let deck = buildDeck(entries, opts.limitNew ?? 12);
  const total = deck.length;
  let done = 0, right = 0;
  const header = `
    <div class="toolbar" style="justify-content:center">
      <div class="seg" role="group" aria-label="방향">
        <button data-d="es2ko" aria-pressed="${dir === "es2ko"}">스페인어 → 뜻</button>
        <button data-d="ko2es" aria-pressed="${dir === "ko2es"}">뜻 → 스페인어</button>
      </div>
    </div>`;
  function show() {
    if (!deck.length) {
      pane.innerHTML = `<div class="flash-wrap">${header}<div class="panel" style="text-align:center">
        ${total ? `<div class="score">${right}/${done}</div><p>이번 판은 끝났어요. 틀린 카드는 바로 복습함에 들어가고, 맞힌 카드는 며칠 뒤에 다시 나와요.</p>`
          : `<p>지금 볼 카드가 없어요. 새 단어도 모두 한 번씩 봤어요.</p>`}
        <div class="row" style="justify-content:center">
          <button class="btn" id="again" type="button">모든 카드 한 번 더</button>
          ${opts.back || ""}
        </div></div></div>`;
      bindDir();
      pane.querySelector("#again").onclick = () => { deck = shuffle(entries); show(); };
      return;
    }
    const { ch, w } = deck[0];
    const front = dir === "es2ko"
      ? `${img(w.img, "", w.en)}<div class="big">${esc(w.es)}</div><div class="pron">[${pron(w.pron)}]</div>`
      : `${img(w.img, "", w.en)}<div class="big" style="font-size:26px">${esc(w.ko)}</div><div class="muted">${esc(w.en)}</div>`;
    const back = `<div class="big">${esc(w.es)}</div><div class="pron">[${pron(w.pron)}]</div><div>${esc(w.ko)} · <span class="muted">${esc(w.en)}</span></div>
      ${w.example ? `<div class="small" style="margin-top:8px">${esc(w.example.es)}<br><span class="muted">${esc(w.example.ko)}</span></div>` : ""}
      ${opts.showChapter ? `<div class="muted small">${nn(ch.num)} · ${esc(ch.es)}</div>` : ""}`;
    pane.innerHTML = `<div class="flash-wrap">${header}
      <div class="progress">${done + 1} / ${Math.max(total, done + deck.length)}</div>
      <div class="flash" id="card" role="button" tabindex="0" aria-label="카드 뒤집기">
        <div class="flash-inner">
          <div class="face front">${front}<span class="hint">눌러서 뒤집기</span></div>
          <div class="face back">${back}<div style="margin-top:8px">${playBtn(w.es, w.audio)}</div></div>
        </div>
      </div>
      <div class="flash-btns">
        <button class="btn bad" id="no" type="button">몰라요</button>
        <button class="btn good" id="yes" type="button">알아요</button>
      </div></div>`;
    bindDir();
    const card = pane.querySelector("#card");
    const flip = () => { card.classList.toggle("flipped"); if (card.classList.contains("flipped") && dir === "ko2es") speak(w.es, w.audio); };
    card.onclick = (e) => { if (!e.target.closest(".play")) flip(); };
    card.onkeydown = (e) => { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(); } };
    if (dir === "es2ko") speak(w.es, w.audio);
    const answer = (ok) => {
      srs.grade(wid(ch.num, w), ok);
      done++; if (ok) right++;
      deck.shift();
      if (!ok) deck.splice(Math.min(deck.length, 3), 0, { ch, w }); // see it again soon
      updateReviewBadge();
      show();
    };
    pane.querySelector("#no").onclick = () => answer(false);
    pane.querySelector("#yes").onclick = () => answer(true);
  }
  function bindDir() {
    pane.querySelectorAll("[data-d]").forEach((b) => b.onclick = () => { store.set("flashDir", b.dataset.d); flashSession(pane, entries, opts); });
  }
  show();
}
function paneFlash(ch, pane) {
  flashSession(pane, ch.words.map((w) => ({ ch, w })), { limitNew: 20 });
}

/* ---------- 퀴즈 ---------- */
function paneQuiz(ch, pane) {
  const hasImg = ch.words.some((w) => w.img);
  const kinds = ["es2ko", "ko2es", "listen", ...(hasImg ? ["img"] : [])];
  const qs = pick(ch.words, 10).map((w, i) => {
    const kind = kinds[i % kinds.length] === "img" && !w.img ? "es2ko" : kinds[i % kinds.length];
    const others = pick(ch.words.filter((x) => x !== w), 3);
    return { w, kind, choices: shuffle([w, ...others]) };
  });
  let i = 0, score = 0;
  const wrong = [];
  const LABEL = { es2ko: "뜻을 고르세요", ko2es: "스페인어를 고르세요", listen: "듣고 고르세요", img: "사진에 맞는 단어는?" };
  function show() {
    if (i >= qs.length) {
      pane.innerHTML = `<div class="quiz"><div class="panel" style="text-align:center">
        <div class="score">${score} / ${qs.length}</div>
        ${wrong.length ? `<p>틀린 단어는 복습함에 넣었어요.</p><div class="wgrid" style="text-align:left">${wrong.map((w) => wordCard(ch, w)).join("")}</div>` : "<p>모두 맞혔어요!</p>"}
        <div class="row" style="justify-content:center;margin-top:12px"><button class="btn" id="re" type="button">다시 풀기</button></div>
      </div></div>`;
      pane.querySelector("#re").onclick = () => paneQuiz(ch, pane);
      return;
    }
    const q = qs[i];
    let prompt = "";
    if (q.kind === "es2ko") prompt = `<div class="prompt">${esc(q.w.es)}</div>${playBtn(q.w.es, q.w.audio)}`;
    if (q.kind === "ko2es") prompt = `<div class="prompt">${esc(q.w.ko)}</div><div class="muted">${esc(q.w.en)}</div>`;
    if (q.kind === "listen") prompt = `<div style="margin:16px 0">${playBtn(q.w.es, q.w.audio).replace('class="play', 'style="width:64px;height:64px;font-size:22px" class="play')}</div>`;
    if (q.kind === "img") prompt = img(q.w.img, "", "");
    const label = (w) => (q.kind === "es2ko" ? `${esc(w.ko)} <span class="muted small">${esc(w.en)}</span>` : esc(w.es));
    pane.innerHTML = `<div class="quiz">
      <div class="progress">${i + 1} / ${qs.length} · 맞힌 개수 ${score}</div>
      <div class="q"><div class="kind">${LABEL[q.kind]}</div>${prompt}</div>
      <div class="choices">${q.choices.map((c, k) => `<button class="choice" data-k="${k}" type="button">${label(c)}</button>`).join("")}</div>
      <div id="after" style="margin-top:12px"></div></div>`;
    if (q.kind === "listen") setTimeout(() => speak(q.w.es, q.w.audio), 250);
    pane.querySelectorAll(".choice").forEach((b) => b.onclick = () => {
      const ok = q.choices[+b.dataset.k] === q.w;
      pane.querySelectorAll(".choice").forEach((x) => { x.disabled = true; if (q.choices[+x.dataset.k] === q.w) x.classList.add("right"); });
      if (!ok) { b.classList.add("wrong"); wrong.push(q.w); } else score++;
      srs.grade(wid(ch.num, q.w), ok);
      const after = pane.querySelector("#after");
      after.innerHTML = `<div class="panel row" style="justify-content:space-between">
        <div><b>${esc(q.w.es)}</b> <span class="pron">[${pron(q.w.pron)}]</span> · ${esc(q.w.ko)}</div>
        <div class="row">${playBtn(q.w.es, q.w.audio)}<button class="btn" id="next" type="button">다음</button></div></div>`;
      if (q.kind !== "listen") speak(q.w.es, q.w.audio);
      after.querySelector("#next").onclick = () => { i++; show(); };
      after.querySelector("#next").focus();
    });
  }
  show();
}

/* ---------- 어순 ---------- */
function paneOrder(ch, pane) {
  const wo = ch.word_order;
  const tok = (s) => `<div class="tokens">${(s.tokens || []).map((t, k) => `<span class="tok${(s.highlight || []).includes(k) ? " hl" : ""}"><span class="a">${esc(t.es)}</span><span class="b">${esc(t.gloss_ko)}</span></span>`).join("")}</div>`;
  const patterns = (wo.patterns || []).map((p) => `<div class="panel"><h3 style="margin-top:0">${esc(p.title_ko)}</h3><table>${p.items.map((it) =>
    `<tr><td>${esc(it.es)}</td><td>${esc(it.ko)}${it.lit ? `<div class="muted small">${esc(it.lit)}</div>` : ""}${it.tag ? ` <span class="g">${esc(it.tag)}</span>` : ""}</td></tr>`).join("")}</table></div>`).join("");
  const list = (o) => o ? `<h3>${esc(o.title_ko)}</h3>${o.items.map((it) => `<div class="line">${playBtn(it.es, null, true)}<div><div class="es2">${esc(it.es)}</div><div class="t">${esc(it.label_ko ? it.label_ko + " · " : "")}${esc(it.ko)}</div></div></div>`).join("")}` : "";
  // exercises: book practice tiles + block sentences reshuffled
  const ex = [
    ...ch.practice.map((p) => ({ tiles: p.tiles, answer: p.answer, ko: p.ko, audio: p.audio })),
    ...wo.sentences.filter((s) => (s.tokens || []).length >= 3).map((s) => ({ tiles: s.tokens.map((t) => t.es), answer: s.es, ko: s.ko, audio: s.audio })),
  ];
  pane.innerHTML = `
    <h2 style="margin-top:8px">${esc(wo.tema)}</h2>
    <p class="sub">${esc(wo.tema_sub_ko)}</p>
    ${wo.lead_ko ? `<div class="panel">${esc(wo.lead_ko)}</div>` : ""}
    <h3>블록으로 보는 문장</h3>
    ${wo.sentences.map((s) => `<div class="panel"><div class="row">${playBtn(s.es, s.audio)}<span class="es2" style="font-family:var(--serif);font-size:18px">${esc(s.es)}</span></div>
      ${tok(s)}<div class="small">${esc(s.ko)} <span class="muted">· ${esc(s.en)}</span></div>${s.note_ko ? `<div class="small" style="color:var(--accent)">${esc(s.note_ko)}</div>` : ""}</div>`).join("")}
    <h2>직접 만들어 보기</h2>
    <p class="sub">블록을 순서대로 눌러 문장을 완성하세요. 잘못 넣은 블록은 다시 누르면 빠져요.</p>
    <div id="builder"></div>
    ${patterns ? `<h2>패턴</h2><div class="patterns">${patterns}</div>` : ""}
    ${list(wo.contrast)}${list(wo.subject)}
    ${(wo.extra_notes_ko || []).length ? `<h3>더 알아보기</h3>${wo.extra_notes_ko.map((n) => `<div class="panel small">${esc(n)}</div>`).join("")}` : ""}`;
  builder(pane.querySelector("#builder"), ex);
}
function builder(root, exercises) {
  let i = 0;
  function show() {
    const e = exercises[i];
    const pool = shuffle(e.tiles.map((t, k) => ({ t, k })));
    const chosen = [];
    root.innerHTML = `<div class="panel">
      <div class="progress" style="text-align:left">${i + 1} / ${exercises.length}</div>
      <div style="font-size:17px;margin:4px 0 10px"><b>${esc(e.ko)}</b></div>
      <div class="builder" id="bd" aria-live="polite"></div>
      <div class="pool" id="pool">${pool.map((p) => `<button class="tile" type="button" data-k="${p.k}">${esc(p.t)}</button>`).join("")}</div>
      <div class="row"><button class="btn" id="chk" type="button">확인</button><button class="btn ghost" id="clr" type="button">지우기</button>
        <button class="btn ghost" id="nx" type="button">${i < exercises.length - 1 ? "다음 문제" : "처음으로"}</button><span id="msg"></span></div></div>`;
    const bd = root.querySelector("#bd");
    const paint = () => {
      bd.className = "builder";
      bd.innerHTML = chosen.map((k) => `<button class="tile" type="button" data-k="${k}">${esc(e.tiles[k])}</button>`).join("");
      root.querySelectorAll("#pool .tile").forEach((b) => b.classList.toggle("used", chosen.includes(+b.dataset.k)));
    };
    root.querySelector("#pool").onclick = (ev) => { const b = ev.target.closest(".tile"); if (b && !chosen.includes(+b.dataset.k)) { chosen.push(+b.dataset.k); paint(); } };
    bd.onclick = (ev) => { const b = ev.target.closest(".tile"); if (b) { chosen.splice(chosen.indexOf(+b.dataset.k), 1); paint(); } };
    root.querySelector("#clr").onclick = () => { chosen.length = 0; paint(); root.querySelector("#msg").textContent = ""; };
    root.querySelector("#nx").onclick = () => { i = (i + 1) % exercises.length; show(); };
    root.querySelector("#chk").onclick = () => {
      const got = norm(chosen.map((k) => e.tiles[k]).join(" "));
      const ok = got === norm(e.answer);
      bd.className = "builder " + (ok ? "ok" : "no");
      root.querySelector("#msg").innerHTML = ok ? `<b style="color:var(--good)">정답!</b>` : `<span style="color:var(--bad)">다시 해 보세요</span> <button class="btn ghost" id="show" type="button" style="padding:4px 10px">정답 보기</button>`;
      if (ok) speak(e.answer, e.audio);
      const sh = root.querySelector("#show");
      if (sh) sh.onclick = () => { root.querySelector("#msg").innerHTML = `<span class="es2" style="font-family:var(--serif)">${esc(e.answer)}</span>`; speak(e.answer, e.audio); };
    };
    paint();
  }
  if (exercises.length) show(); else root.innerHTML = '<p class="empty">연습 문제가 없어요.</p>';
}

/* ---------- 대화 ---------- */
function paneTalk(ch, pane) {
  if (!ch.dialogues.length) { pane.innerHTML = '<p class="empty">이 장의 대화는 준비 중이에요.</p>'; return; }
  const di = Math.min(store.get("dlg" + ch.num, 0), ch.dialogues.length - 1);
  const mode = store.get("dlgMode", "both");
  const showKo = store.get("dlgKo", true);
  const d = ch.dialogues[di];
  const ver = (ln, v) => {
    const x = ln[v];
    return `<div class="ver"><div>${playBtn(x.es, x.audio, true)}</div><div>
      <div class="lab ${v}">${v === "native" ? "원어민은 이렇게" : "교재 표현"}</div>
      <div class="txt">${tappable(ch, x.es)}</div>
      <div class="ko">${esc(x.ko)}</div>
      ${v === "native" && x.note_ko && mode !== "textbook" ? `<div class="why">${esc(x.note_ko)}</div>` : ""}</div></div>`;
  };
  const vers = mode === "both" ? ["textbook", "native"] : [mode];
  pane.innerHTML = `
    <div class="dlg-pick">${ch.dialogues.map((x, k) => `<button class="btn${k === di ? "" : " ghost"}" data-di="${k}" type="button">${esc(x.title_ko)}</button>`).join("")}</div>
    <h2 style="margin-top:6px">${esc(d.title_es)}</h2>
    <p class="setting">${esc(d.setting_ko)}</p>
    <div class="toolbar">
      <div class="seg" role="group" aria-label="표현">
        <button data-m="textbook" aria-pressed="${mode === "textbook"}">교재</button>
        <button data-m="native" aria-pressed="${mode === "native"}">원어민</button>
        <button data-m="both" aria-pressed="${mode === "both"}">비교</button>
      </div>
      <label class="small"><input type="checkbox" id="ko" ${showKo ? "checked" : ""}> 한국어 뜻</label>
      <button class="btn ghost" id="playDlg" type="button">▶ 대화 듣기</button>
    </div>
    <p class="muted small">밑줄 친 단어를 누르면 뜻과 발음이 나와요.</p>
    <div id="dlg" class="${showKo ? "" : "hide-ko"}">${d.lines.map((ln, k) => `<div class="bubble-row ${ln.who === "A" ? "A" : "B"}" data-line="${k}">
      <div class="who" title="${esc(d.roles[ln.who]?.ko)}">${esc((d.roles[ln.who]?.ko || ln.who).slice(0, 4))}</div>
      <div class="bubble">${vers.map((v) => ver(ln, v)).join("")}</div></div>`).join("")}</div>`;
  pane.querySelectorAll("[data-di]").forEach((b) => b.onclick = () => { store.set("dlg" + ch.num, +b.dataset.di); paneTalk(ch, pane); });
  pane.querySelectorAll("[data-m]").forEach((b) => b.onclick = () => { store.set("dlgMode", b.dataset.m); paneTalk(ch, pane); });
  pane.querySelector("#ko").onchange = (e) => { store.set("dlgKo", e.target.checked); pane.querySelector("#dlg").classList.toggle("hide-ko", !e.target.checked); };
  let stop = false;
  pane.querySelector("#playDlg").onclick = async (e) => {
    const b = e.currentTarget;
    if (b.dataset.on) { stop = true; stopAll(); return; }
    stop = false; b.dataset.on = "1"; b.textContent = "■ 멈춤";
    const v = mode === "textbook" ? "textbook" : "native";
    for (const [k, ln] of d.lines.entries()) {
      if (stop || !document.body.contains(b)) break;
      const row = pane.querySelector(`[data-line="${k}"]`);
      row.scrollIntoView({ block: "nearest", behavior: "smooth" });
      await speak(ln[v].es, ln[v].audio, row.querySelector(`.lab.${v}`)?.closest(".ver")?.querySelector(".play"));
      await new Promise((r) => setTimeout(r, 450));
    }
    delete b.dataset.on; b.textContent = "▶ 대화 듣기";
  };
}

/* ---------- 읽기 ---------- */
function paneRead(ch, pane) {
  if (!ch.readings.length) { pane.innerHTML = '<p class="empty">이 장의 읽기 글은 준비 중이에요.</p>'; return; }
  const ri = Math.min(store.get("rd" + ch.num, 0), ch.readings.length - 1);
  const showKo = store.get("rdKo", false);
  const r = ch.readings[ri];
  pane.innerHTML = `
    <div class="dlg-pick">${ch.readings.map((x, k) => `<button class="btn${k === ri ? "" : " ghost"}" data-ri="${k}" type="button">${esc(x.title_ko)}</button>`).join("")}</div>
    <h2 style="margin-top:6px">${esc(r.title_es)} <span class="level">${esc(r.level)}</span></h2>
    <div class="toolbar">
      <label class="small"><input type="checkbox" id="ko" ${showKo ? "checked" : ""}> 번역 보기</label>
      <button class="btn ghost" id="playAll" type="button">▶ 전체 듣기</button>
    </div>
    <p class="muted small">모르는 단어를 누르면 뜻·발음·기본형이 나와요. 문단 왼쪽 ▶는 그 문단만 읽어 줘요.</p>
    <div class="reading ${showKo ? "" : "hide-ko"}" id="rd">${r.paragraphs.map((p) => `<div class="para row" style="align-items:flex-start;flex-wrap:nowrap">
      ${playBtn(p.es, p.audio, true)}<div><div class="txt">${tappable(ch, p.es)}</div><div class="ko">${esc(p.ko)}</div></div></div>`).join("")}</div>
    ${(r.questions || []).length ? `<h3>내용 확인</h3>${r.questions.map((q, qi) => `<div class="panel" data-q="${qi}"><div style="margin-bottom:8px"><b>${qi + 1}.</b> ${esc(q.q_ko)}</div>
      <div class="choices" style="margin-top:0">${q.choices_ko.map((c, ci) => `<button class="choice" type="button" data-c="${ci}">${esc(c)}</button>`).join("")}</div></div>`).join("")}` : ""}`;
  pane.querySelectorAll("[data-ri]").forEach((b) => b.onclick = () => { store.set("rd" + ch.num, +b.dataset.ri); paneRead(ch, pane); });
  pane.querySelector("#ko").onchange = (e) => { store.set("rdKo", e.target.checked); pane.querySelector("#rd").classList.toggle("hide-ko", !e.target.checked); };
  pane.querySelectorAll("[data-q]").forEach((box) => {
    const q = r.questions[+box.dataset.q];
    box.querySelectorAll(".choice").forEach((b) => b.onclick = () => {
      box.querySelectorAll(".choice").forEach((x) => { x.disabled = true; if (+x.dataset.c === q.answer) x.classList.add("right"); });
      if (+b.dataset.c !== q.answer) b.classList.add("wrong");
    });
  });
  let stop = false;
  pane.querySelector("#playAll").onclick = async (e) => {
    const b = e.currentTarget;
    if (b.dataset.on) { stop = true; stopAll(); return; }
    stop = false; b.dataset.on = "1"; b.textContent = "■ 멈춤";
    const btns = pane.querySelectorAll("#rd .play");
    for (const [k, p] of r.paragraphs.entries()) { if (stop || !document.body.contains(b)) break; await speak(p.es, p.audio, btns[k]); }
    delete b.dataset.on; b.textContent = "▶ 전체 듣기";
  };
}

/* ---------- 전체 복습 ---------- */
async function renderReview() {
  const chs = await Promise.all(index.chapters.map((c) => getChapter(c.num)));
  const all = srs.all();
  const entries = [];
  for (const ch of chs) for (const w of ch.words) if (all[wid(ch.num, w)]) entries.push({ ch, w });
  const due = entries.filter((e) => all[wid(e.ch.num, e.w)].due <= Date.now());
  $app.innerHTML = `<h1>복습</h1><p class="sub">여러 장에서 공부한 단어 중 다시 볼 때가 된 카드예요. 지금 ${due.length}장 · 전체 ${entries.length}장.</p><section id="pane"></section>`;
  const pane = document.getElementById("pane");
  if (!entries.length) { pane.innerHTML = `<div class="panel">아직 복습함이 비어 있어요. 장을 골라 플래시카드나 퀴즈를 먼저 해 보세요. <a href="#/">장 고르기</a></div>`; return; }
  flashSession(pane, due.length ? due : entries, { limitNew: 0, showChapter: true, back: '<a class="btn ghost" href="#/">처음으로</a>' });
}

/* ---------- 출처 ---------- */
function mdToHtml(md) {
  const lines = md.split("\n");
  let out = "", inList = false, table = [];
  const inline = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>").replace(/(https?:\/\/[^\s)|]+)/g, '<a href="$1" target="_blank" rel="noopener">링크</a>');
  const flushTable = () => {
    if (!table.length) return;
    const rows = table.filter((r) => !/^\|[\s:|-]+\|$/.test(r)).map((r) => r.replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
    out += `<table><thead><tr>${rows[0].map((c) => `<th>${inline(c)}</th>`).join("")}</tr></thead><tbody>${rows.slice(1).map((r) => `<tr>${r.map((c) => `<td>${inline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
    table = [];
  };
  for (const ln of lines) {
    if (ln.startsWith("|")) { table.push(ln.trim()); continue; }
    flushTable();
    if (/^\s*- /.test(ln)) { if (!inList) { out += "<ul>"; inList = true; } out += `<li>${inline(ln.replace(/^\s*- /, ""))}</li>`; continue; }
    if (inList) { out += "</ul>"; inList = false; }
    const h = ln.match(/^(#{1,3}) (.*)/);
    if (h) out += `<h${h[1].length + 1}>${inline(h[2])}</h${h[1].length + 1}>`;
    else if (ln.trim()) out += `<p class="small">${inline(ln)}</p>`;
  }
  flushTable(); if (inList) out += "</ul>";
  return out;
}
async function renderCredits() {
  const docs = await Promise.all(index.credits.map((f) => fetch("media/credits/" + f).then((r) => r.text())));
  $app.innerHTML = `<h1>사진 출처</h1>
    <p class="sub">사진은 모두 Wikimedia Commons의 실제 사진이고, 각 라이선스(CC0, CC BY, CC BY-SA 등)에 따라 표기했어요. 음성은 스페인 표준 발음 음성 합성이에요.</p>
    <div class="md">${docs.map((d) => `<div class="panel">${mdToHtml(d)}</div>`).join("")}</div>`;
}

route();
