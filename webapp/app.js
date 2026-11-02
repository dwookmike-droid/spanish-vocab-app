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
  ? `<img class="${cls}" src="media/img/${name}.webp" alt="${esc(alt)}" loading="lazy" decoding="async">`
  : "";

async function getJSON(url) {
  const bundled = window.VV_DATA && window.VV_DATA[url.split("/").pop()];
  if (bundled) return bundled;
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
    activity.add(1);
  },
  isKnown(id) { const c = this.get(id); return !!c && c.box >= 3; },
  dueIds() { const now = Date.now(); return Object.entries(this.all()).filter(([, c]) => c.due <= now).map(([id]) => id); },
};
const wid = (ch, w) => `${nn(ch)}:${w.key}`;

/* ---------- daily activity: count of answers per local date, streak ---------- */
const today = (d = new Date()) => `${d.getFullYear()}-${nn(d.getMonth() + 1)}-${nn(d.getDate())}`;
const activity = {
  log() { return store.get("log", {}); },
  add(n) { const l = this.log(); const k = today(); l[k] = (l[k] || 0) + n; store.set("log", l); },
  todayCount() { return this.log()[today()] || 0; },
  streak() {
    const l = this.log(); let s = 0; const d = new Date();
    if (!l[today(d)]) d.setDate(d.getDate() - 1); // today not started yet: count up to yesterday
    while (l[today(d)]) { s++; d.setDate(d.getDate() - 1); }
    return s;
  },
  last7() {
    const l = this.log(); const out = []; const d = new Date();
    for (let i = 6; i >= 0; i--) { const x = new Date(d); x.setDate(d.getDate() - i); out.push({ day: "일월화수목금토"[x.getDay()], n: l[today(x)] || 0, isToday: i === 0 }); }
    return out;
  },
};
const settings = {
  get() { return { goal: 20, hidePron: false, theme: "auto", ...store.get("settings", {}) }; },
  set(patch) { store.set("settings", { ...this.get(), ...patch }); applySettings(); },
};
function applySettings() {
  const s = settings.get();
  document.body.classList.toggle("no-pron", !!s.hidePron);
  if (s.theme === "auto") document.documentElement.removeAttribute("data-theme");
  else document.documentElement.setAttribute("data-theme", s.theme);
}

/* ---------- my words (saved from tapped words) ---------- */
const mine = {
  all() { return store.get("mine", []); },
  has(id) { return this.all().some((m) => m.id === id); },
  toggle(entry) {
    const all = this.all(); const i = all.findIndex((m) => m.id === entry.id);
    if (i >= 0) all.splice(i, 1); else all.unshift({ ...entry, added: Date.now() });
    store.set("mine", all); return i < 0;
  },
};

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
/* preview builds pack audio into a few data/audiopack_NN.js files (the page host limits file counts) */
const packs = {};
function ensurePack(n) {
  if (!window.VV_PACKED) return Promise.resolve();
  const k = nn(n);
  packs[k] = packs[k] || new Promise((res) => {
    const sc = document.createElement("script"); sc.src = `data/audiopack_${k}.js`; sc.onload = res; sc.onerror = res; document.head.appendChild(sc);
  });
  return packs[k];
}
const audioSrc = (file) => { const b = (window.VV_AUDIO || {})[file]; return b ? "data:audio/mpeg;base64," + b : "media/audio/" + file; };
let speakSeq = 0;
function speak(text, file, btn) {
  const my = ++speakSeq;
  return new Promise((resolve) => {
    stopAll();
    if (btn) { btn.classList.add("on"); playingBtn = btn; }
    const done = () => { if (btn) btn.classList.remove("on"); resolve(); };
    if (file && window.VV_PACKED && !(window.VV_AUDIO || {})[file]) {
      // preview build: audio lives in per-chapter packs; load the one holding this file, then play
      const ch = (window.VV_PACK_INDEX || {})[file];
      if (ch) { ensurePack(ch).then(() => { if (my === speakSeq) speak(text, file, btn).then(resolve); else resolve(); }); return; }
    }
    if (file) {
      player.src = audioSrc(file);
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

/* ---------- answer checking: accent-tolerant word diff ---------- */
const fold = (s) => norm(s).normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ñ/g, "n");
const words = (s) => norm(s).split(" ").filter(Boolean);
/* compare typed/recognized text with the target; per target word: ok | accent | miss */
function diffWords(target, got) {
  const t = words(target), g = words(got);
  const gFold = g.map(fold);
  const used = new Set();
  const marks = t.map((w) => {
    const exact = g.findIndex((x, i) => !used.has(i) && x === w);
    if (exact >= 0) { used.add(exact); return "ok"; }
    const loose = gFold.findIndex((x, i) => !used.has(i) && x === fold(w));
    if (loose >= 0) { used.add(loose); return "accent"; }
    return "miss";
  });
  const score = t.length ? marks.reduce((a, m) => a + (m === "ok" ? 1 : m === "accent" ? 0.8 : 0), 0) / t.length : 0;
  const extra = g.filter((_, i) => !used.has(i));
  return { marks, score, extra, t };
}
function diffHtml(target, d) {
  // keep the original punctuation/case of the target, colour each word
  let k = 0;
  return target.split(/(\s+)/).map((part) => {
    if (!part.trim() || !norm(part)) return esc(part);
    const m = d.marks[k++] || "miss";
    return `<span class="dw ${m}">${esc(part)}</span>`;
  }).join("") + (d.extra.length ? ` <span class="dw extra" title="정답에 없는 단어">+ ${esc(d.extra.join(" "))}</span>` : "");
}
const ACCENTS = ["á", "é", "í", "ó", "ú", "ñ", "ü", "¿", "¡"];
const accentBar = (target) => `<div class="accents">${ACCENTS.map((a) => `<button type="button" class="acc" data-ins="${a}" data-target="${target}">${a}</button>`).join("")}</div>`;
document.addEventListener("click", (e) => {
  const b = e.target.closest(".acc");
  if (!b) return;
  const inp = document.getElementById(b.dataset.target);
  if (!inp) return;
  const s = inp.selectionStart ?? inp.value.length, en = inp.selectionEnd ?? s;
  inp.value = inp.value.slice(0, s) + b.dataset.ins + inp.value.slice(en);
  inp.focus(); inp.setSelectionRange(s + 1, s + 1);
});

/* ---------- speech recognition (Chrome, Edge, Safari) + recording ---------- */
const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
function listenOnce() {
  return new Promise((resolve, reject) => {
    if (!SR) { reject(new Error("이 브라우저는 음성 인식을 지원하지 않아요. Chrome이나 Safari에서 열어 주세요.")); return; }
    stopAll();
    const r = new SR();
    r.lang = "es-ES"; r.interimResults = false; r.maxAlternatives = 3;
    let best = "";
    r.onresult = (ev) => {
      const alts = [...ev.results[0]].map((a) => a.transcript);
      best = alts[0] || "";
      resolve({ text: best, alts });
    };
    r.onerror = (ev) => reject(new Error(ev.error === "not-allowed" ? "마이크 권한을 허용해 주세요." : ev.error === "no-speech" ? "소리가 들리지 않았어요. 다시 해 보세요." : "음성 인식 오류: " + ev.error));
    r.onend = () => { if (!best) reject(new Error("소리가 들리지 않았어요. 다시 해 보세요.")); };
    r.start();
  });
}
const recorder = {
  rec: null, chunks: [], url: null,
  async start() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    this.chunks = []; this.rec = new MediaRecorder(stream);
    this.rec.ondataavailable = (e) => this.chunks.push(e.data);
    this.rec.start();
  },
  stop() {
    return new Promise((resolve) => {
      if (!this.rec) { resolve(null); return; }
      this.rec.onstop = () => {
        this.rec.stream.getTracks().forEach((t) => t.stop());
        if (this.url) URL.revokeObjectURL(this.url);
        this.url = URL.createObjectURL(new Blob(this.chunks, { type: this.rec.mimeType }));
        this.rec = null; resolve(this.url);
      };
      this.rec.stop();
    });
  },
};
const canRecord = () => !!(navigator.mediaDevices && window.MediaRecorder);

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
    <div class="row"><span class="es" id="sheetWord">${esc(chw ? chw.es : word)}</span>${playBtn(say, chw ? chw.audio : e.audio)}</div>
    ${e.lemma && norm(e.lemma) !== norm(word) && !chw ? `<div class="lemma">기본형: ${esc(e.lemma)}</div>` : ""}
    <div class="pron">[${pron(e.pron || "")}]</div>
    <div class="mean">${esc(e.ko || "")}</div>
    <div class="muted small">${esc(e.en || "")}</div>
    ${chw ? `<div class="muted small" style="margin-top:6px">이 장의 단어예요 · ${chw.core ? "핵심" : "보조"}</div>` : ""}
    ${chw ? "" : `<button class="btn ghost" id="saveWord" type="button" style="margin-top:10px"></button>`}`;
  const sv = sheetBody.querySelector("#saveWord");
  if (sv) {
    const entry = { id: `${nn(ch.num)}:${norm(word)}`, ch: ch.num, es: word.toLowerCase(), lemma: e.lemma, ko: e.ko, en: e.en, pron: e.pron, audio: e.audio || null };
    const paint = () => { sv.textContent = mine.has(entry.id) ? "★ 내 단어장에 있어요 (빼기)" : "☆ 내 단어장에 저장"; };
    paint();
    sv.onclick = () => { mine.toggle(entry); paint(); };
  }
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
  ["words", "단어"], ["flash", "플래시카드"], ["quiz", "퀴즈"], ["listen", "받아쓰기"], ["speak", "말하기"],
  ["order", "어순"], ["talk", "대화"], ["read", "읽기"],
];
async function route() {
  stopAll(); closeSheet();
  const parts = location.hash.replace(/^#\/?/, "").split("/").filter(Boolean);
  try {
    index = index || await getJSON("data/chapters.json");
    if (parts[0] === "ch" && parts[1]) {
      const ch = await getChapter(parseInt(parts[1], 10));
      currentChapter = ch;
      ensurePack(ch.num);
      const tab = TABS.some(([k]) => k === parts[2]) ? parts[2] : "words";
      renderChapter(ch, tab);
    } else if (parts[0] === "review") { if (window.VV_PACKED) index.chapters.forEach((c) => ensurePack(c.num)); currentChapter = null; await renderReview(); }
    else if (parts[0] === "credits") { currentChapter = null; await renderCredits(); }
    else if (parts[0] === "mine") { currentChapter = null; renderMine(); }
    else if (parts[0] === "search") { currentChapter = null; await renderSearch(decodeURIComponent(parts[1] || "")); }
    else if (parts[0] === "settings") { currentChapter = null; renderSettings(); }
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
  const s = settings.get();
  const tc = activity.todayCount();
  const learned = Object.values(all).filter((v) => v.box >= 3).length;
  const seen = Object.keys(all).length;
  const week = activity.last7();
  const max = Math.max(s.goal, ...week.map((w) => w.n));
  const lastCh = store.get("lastCh", null);
  const firstNew = index.chapters.find((c) => !Object.keys(all).some((id) => id.startsWith(nn(c.num) + ":")));
  const next = lastCh ? index.chapters.find((c) => c.num === lastCh.num) : firstNew || index.chapters[0];
  $app.innerHTML = `
    <section class="hero">
      <h1>사진으로 배우는 여행 스페인어</h1>
      <p>그라나다에서 마드리드까지, 장소마다 20단어. 듣고, 말하고, 쓰고, 읽으면서 익혀요.</p>
    </section>
    <section class="dash">
      <div class="stat"><b>${activity.streak()}</b><span>연속 학습일</span></div>
      <div class="stat"><b>${tc}<small>/${s.goal}</small></b><span>오늘 푼 문제</span><div class="bar"><i style="width:${Math.min(100, (tc / s.goal) * 100)}%"></i></div></div>
      <div class="stat"><b>${learned}</b><span>외운 단어 <small>(본 단어 ${seen})</small></span></div>
      <div class="week" aria-label="최근 7일 학습량">${week.map((w) => `<div class="day${w.isToday ? " today" : ""}" title="${w.n}문제"><i style="height:${max ? Math.max(4, (w.n / max) * 44) : 4}px${w.n ? "" : ";opacity:.35"}"></i><span>${w.day}</span></div>`).join("")}</div>
    </section>
    <div class="review-cta">
      <div><b>오늘 복습할 카드 ${due}장</b><div class="muted small">틀린 단어는 바로, 맞힌 단어는 1·2·4·8·16일 뒤에 다시 나와요.</div></div>
      <div class="row">
        ${next ? `<a class="btn ghost" href="#/ch/${nn(next.num)}/${lastCh?.tab || "words"}">${lastCh ? "이어서" : "시작"}: ${nn(next.num)} ${esc(next.es)}</a>` : ""}
        <a class="btn${due ? "" : " ghost"}" href="#/review">${due ? "복습 시작" : "복습함"}</a>
      </div>
    </div>
    <form class="search" id="searchForm" role="search">
      <input id="q" type="search" placeholder="단어 찾기 (스·한·영)" autocomplete="off" aria-label="단어 찾기">
      <button class="btn" type="submit">찾기</button>
    </form>
    <div class="chgrid">${cards}</div>
    <p class="muted small" style="margin-top:20px">▶ 버튼은 스페인 표준 발음이에요. 테두리가 옅은 ▶는 기기에 내장된 음성으로 읽어 줘요. 진도는 이 브라우저에만 저장돼요. <a href="#/settings">설정</a>에서 백업할 수 있어요.</p>`;
  document.getElementById("searchForm").onsubmit = (e) => { e.preventDefault(); const q = document.getElementById("q").value.trim(); if (q) location.hash = "#/search/" + encodeURIComponent(q); };
}

/* ---------- chapter shell ---------- */
function renderChapter(ch, tab) {
  const tabs = TABS.map(([k, label]) => `<a href="#/ch/${nn(ch.num)}/${k}"${k === tab ? ' aria-current="page"' : ""}>${label}</a>`).join("");
  $app.innerHTML = `
    <div class="chhead"><h1>${nn(ch.num)} · ${esc(ch.es)}</h1><span class="city">${esc(ch.ko)} · ${esc(ch.city)} · ${esc(ch.date)}</span></div>
    <nav class="tabs" aria-label="학습 메뉴">${tabs}</nav>
    <section id="pane"></section>`;
  const pane = document.getElementById("pane");
  store.set("lastCh", { num: ch.num, tab });
  const cur = $app.querySelector('.tabs [aria-current="page"]');
  if (cur) cur.scrollIntoView({ block: "nearest", inline: "center" });
  ({ words: paneWords, flash: paneFlash, quiz: paneQuiz, listen: paneListen, speak: paneSpeak, order: paneOrder, talk: paneTalk, read: paneRead })[tab](ch, pane);
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
const ARTICLE = { m: "el", f: "la", mpl: "los", fpl: "las" };
function paneQuiz(ch, pane) {
  const mode = store.get("quizMode", "mix");
  const hasImg = ch.words.some((w) => w.img);
  const nouns = ch.words.filter((w) => ARTICLE[w.gender]);
  const kindsFor = { mix: ["es2ko", "ko2es", "listen", "type", ...(hasImg ? ["img"] : []), ...(nouns.length >= 4 ? ["gender"] : [])],
    choice: ["es2ko", "ko2es", "listen", ...(hasImg ? ["img"] : [])], type: ["type"], gender: ["gender"] };
  const kinds = kindsFor[mode].length ? kindsFor[mode] : kindsFor.mix;
  const pool = mode === "gender" ? nouns : ch.words;
  const qs = pick(pool, 10).map((w, i) => {
    let kind = kinds[i % kinds.length];
    if (kind === "img" && !w.img) kind = "es2ko";
    if (kind === "gender" && !ARTICLE[w.gender]) kind = "ko2es";
    const others = pick(ch.words.filter((x) => x !== w), 3);
    return { w, kind, choices: shuffle([w, ...others]) };
  });
  let i = 0, score = 0;
  const wrong = [];
  const LABEL = { es2ko: "뜻을 고르세요", ko2es: "스페인어를 고르세요", listen: "듣고 고르세요", img: "사진에 맞는 단어는?",
    type: "스페인어로 써 보세요 (관사 포함)", gender: "알맞은 관사를 고르세요" };
  const head = `<div class="toolbar" style="justify-content:center"><div class="seg" role="group" aria-label="퀴즈 종류">
    ${[["mix", "섞어서"], ["choice", "객관식"], ["type", "쓰기"], ["gender", "el/la"]].map(([k, l]) => `<button data-qm="${k}" aria-pressed="${mode === k}">${l}</button>`).join("")}</div></div>`;
  const bindHead = () => pane.querySelectorAll("[data-qm]").forEach((b) => b.onclick = () => { store.set("quizMode", b.dataset.qm); paneQuiz(ch, pane); });
  function finish(ok, extraHtml = "") {
    const q = qs[i];
    if (!ok) wrong.push(q.w); else score++;
    srs.grade(wid(ch.num, q.w), ok);
    const after = pane.querySelector("#after");
    after.innerHTML = `<div class="panel row" style="justify-content:space-between">
      <div>${extraHtml}<b>${esc(q.w.es)}</b> <span class="pron">[${pron(q.w.pron)}]</span> · ${esc(q.w.ko)}</div>
      <div class="row">${playBtn(q.w.es, q.w.audio)}<button class="btn" id="next" type="button">다음</button></div></div>`;
    if (q.kind !== "listen") speak(q.w.es, q.w.audio);
    after.querySelector("#next").onclick = () => { i++; show(); };
    after.querySelector("#next").focus();
  }
  function show() {
    if (i >= qs.length) {
      pane.innerHTML = `${head}<div class="quiz"><div class="panel" style="text-align:center">
        <div class="score">${score} / ${qs.length}</div>
        ${wrong.length ? `<p>틀린 단어는 복습함에 넣었어요.</p><div class="wgrid" style="text-align:left">${wrong.map((w) => wordCard(ch, w)).join("")}</div>` : "<p>모두 맞혔어요!</p>"}
        <div class="row" style="justify-content:center;margin-top:12px"><button class="btn" id="re" type="button">다시 풀기</button></div>
      </div></div>`;
      bindHead();
      pane.querySelector("#re").onclick = () => paneQuiz(ch, pane);
      return;
    }
    const q = qs[i];
    let prompt = "", body = "";
    if (q.kind === "es2ko") prompt = `<div class="prompt">${esc(q.w.es)}</div>${playBtn(q.w.es, q.w.audio)}`;
    if (q.kind === "ko2es" || q.kind === "type") prompt = `${q.kind === "type" ? img(q.w.img, "", "") : ""}<div class="prompt">${esc(q.w.ko)}</div><div class="muted">${esc(q.w.en)}</div>`;
    if (q.kind === "listen") prompt = `<div style="margin:16px 0">${playBtn(q.w.es, q.w.audio).replace('class="play', 'style="width:64px;height:64px;font-size:22px" class="play')}</div>`;
    if (q.kind === "img") prompt = img(q.w.img, "", "");
    if (q.kind === "gender") prompt = `${img(q.w.img, "", "")}<div class="prompt">___ ${esc(q.w.base)}</div><div class="muted">${esc(q.w.ko)}</div>`;
    if (q.kind === "type") {
      body = `<form id="typeForm" class="typeform"><input id="ans" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="예: la toalla" aria-label="답">
        <button class="btn" type="submit">확인</button></form>${accentBar("ans")}
        <button class="btn ghost small" id="hint" type="button" style="margin-top:6px">힌트</button>`;
    } else if (q.kind === "gender") {
      body = `<div class="choices g4">${["el", "la", "los", "las"].map((a) => `<button class="choice" data-a="${a}" type="button" style="text-align:center">${a}</button>`).join("")}</div>`;
    } else {
      const label = (w) => (q.kind === "es2ko" ? `${esc(w.ko)} <span class="muted small">${esc(w.en)}</span>` : esc(w.es));
      body = `<div class="choices">${q.choices.map((c, k) => `<button class="choice" data-k="${k}" type="button">${label(c)}</button>`).join("")}</div>`;
    }
    pane.innerHTML = `${head}<div class="quiz">
      <div class="progress">${i + 1} / ${qs.length} · 맞힌 개수 ${score}</div>
      <div class="q"><div class="kind">${LABEL[q.kind]}</div>${prompt}</div>
      ${body}
      <div id="after" style="margin-top:12px"></div></div>`;
    bindHead();
    if (q.kind === "listen") setTimeout(() => speak(q.w.es, q.w.audio), 250);
    if (q.kind === "type") {
      const inp = pane.querySelector("#ans"); inp.focus();
      let hints = 0;
      pane.querySelector("#hint").onclick = () => { hints++; inp.placeholder = q.w.es.slice(0, Math.min(q.w.es.length, 2 + hints * 2)) + "…"; };
      pane.querySelector("#typeForm").onsubmit = (e) => {
        e.preventDefault();
        if (pane.querySelector("#next")) return;
        const got = inp.value.trim();
        if (!got) return;
        const exact = norm(got) === norm(q.w.es) || (q.w.base && norm(got) === norm(q.w.base) && !ARTICLE[q.w.gender]);
        const loose = fold(got) === fold(q.w.es);
        const noArt = q.w.base && fold(got) === fold(q.w.base) && ARTICLE[q.w.gender];
        inp.disabled = true;
        inp.classList.add(exact ? "ok" : loose || noArt ? "near" : "no");
        const msg = exact ? '<span class="tag good">정답</span> ' : loose ? '<span class="tag near">거의 맞았어요 · 강세 표시를 확인하세요</span><br>'
          : noArt ? '<span class="tag near">관사까지 써야 해요</span><br>' : `<span class="tag bad">정답은</span> `;
        finish(exact || (loose && hints === 0), msg);
      };
    } else if (q.kind === "gender") {
      pane.querySelectorAll("[data-a]").forEach((b) => b.onclick = () => {
        const right = ARTICLE[q.w.gender];
        pane.querySelectorAll("[data-a]").forEach((x) => { x.disabled = true; if (x.dataset.a === right) x.classList.add("right"); });
        if (b.dataset.a !== right) b.classList.add("wrong");
        const tip = q.w.base && /a$/.test(q.w.base) && right.startsWith("e") ? '<span class="muted small">-a로 끝나도 남성인 예외예요.</span><br>'
          : q.w.base && /o$/.test(q.w.base) && right.startsWith("la") ? '<span class="muted small">-o로 끝나도 여성인 예외예요.</span><br>' : "";
        finish(b.dataset.a === right, tip);
      });
    } else {
      pane.querySelectorAll(".choice").forEach((b) => b.onclick = () => {
        const ok = q.choices[+b.dataset.k] === q.w;
        pane.querySelectorAll(".choice").forEach((x) => { x.disabled = true; if (q.choices[+x.dataset.k] === q.w) x.classList.add("right"); });
        if (!ok) b.classList.add("wrong");
        finish(ok);
      });
    }
  }
  show();
}

/* ---------- 받아쓰기 ---------- */
function sentencePool(ch) {
  // every voiced sentence of the chapter, examples first (shortest = easiest)
  const out = [];
  const add = (s, src) => { if (s && s.es && !out.some((x) => x.es === s.es)) out.push({ es: s.es, ko: s.ko, audio: s.audio, src }); };
  ch.words.forEach((w) => add(w.example, "예문"));
  ch.scenes.forEach((s) => add(s, "장면"));
  ch.word_order.sentences.forEach((s) => add(s, "어순"));
  ch.dialogues.forEach((d) => d.lines.forEach((l) => add(l.textbook, "대화")));
  return out;
}
function paneListen(ch, pane) {
  const level = store.get("dictLevel", "easy");
  const all = sentencePool(ch);
  const pool = all.filter((s) => (level === "easy" ? words(s.es).length <= 6 : words(s.es).length > 4));
  const list = shuffle(pool.length ? pool : all).slice(0, 10);
  let i = 0, total = 0;
  function show() {
    if (i >= list.length) {
      pane.innerHTML = `<div class="quiz"><div class="panel" style="text-align:center"><div class="score">${Math.round((total / list.length) * 100)}점</div>
        <p>받아쓰기 ${list.length}문장을 마쳤어요.</p><button class="btn" id="re" type="button">다시 하기</button></div></div>`;
      pane.querySelector("#re").onclick = () => paneListen(ch, pane);
      return;
    }
    const s = list[i];
    pane.innerHTML = `<div class="quiz">
      <div class="toolbar" style="justify-content:center"><div class="seg" role="group" aria-label="난이도">
        <button data-lv="easy" aria-pressed="${level === "easy"}">짧은 문장</button><button data-lv="hard" aria-pressed="${level === "hard"}">긴 문장</button></div></div>
      <div class="progress">${i + 1} / ${list.length} · ${esc(s.src)}</div>
      <div class="q"><div class="kind">듣고 그대로 써 보세요</div>
        <div class="row" style="justify-content:center;margin:12px 0">
          ${playBtn(s.es, s.audio).replace('class="play', 'id="big" style="width:64px;height:64px;font-size:22px" class="play')}
          <button class="btn ghost" id="slow" type="button">🐢 천천히</button>
        </div>
        <div class="muted small" id="koHint" hidden>${esc(s.ko)}</div>
      </div>
      <form id="dForm" class="typeform"><textarea id="ans" rows="2" autocomplete="off" autocapitalize="sentences" spellcheck="false" placeholder="들리는 대로 쓰세요" aria-label="받아쓰기"></textarea>
        <button class="btn" type="submit">확인</button></form>
      ${accentBar("ans")}
      <div class="row" style="margin-top:6px"><button class="btn ghost" id="kh" type="button">뜻 보기</button><button class="btn ghost" id="skip" type="button">모르겠어요</button></div>
      <div id="after" style="margin-top:12px"></div></div>`;
    pane.querySelectorAll("[data-lv]").forEach((b) => b.onclick = () => { store.set("dictLevel", b.dataset.lv); paneListen(ch, pane); });
    setTimeout(() => speak(s.es, s.audio, pane.querySelector("#big")), 250);
    pane.querySelector("#slow").onclick = () => { const r0 = rate; rate = 0.75; speak(s.es, s.audio).then(() => { rate = r0; }); };
    pane.querySelector("#kh").onclick = () => { pane.querySelector("#koHint").hidden = false; };
    const check = (got) => {
      const d = diffWords(s.es, got);
      total += d.score;
      activity.add(1);
      const after = pane.querySelector("#after");
      after.innerHTML = `<div class="panel">
        <div class="es2 diff">${diffHtml(s.es, d)}</div>
        <div class="muted small" style="margin-top:4px">${esc(s.ko)}</div>
        <div class="row" style="justify-content:space-between;margin-top:10px">
          <span class="tag ${d.score >= 0.95 ? "good" : d.score >= 0.6 ? "near" : "bad"}">${Math.round(d.score * 100)}점</span>
          <span class="legend small"><span class="dw ok">맞음</span> <span class="dw accent">강세</span> <span class="dw miss">빠짐·틀림</span></span>
          <div class="row">${playBtn(s.es, s.audio)}<button class="btn" id="next" type="button">다음</button></div>
        </div></div>`;
      pane.querySelector("#ans").disabled = true;
      after.querySelector("#next").onclick = () => { i++; show(); };
      after.querySelector("#next").focus();
    };
    pane.querySelector("#dForm").onsubmit = (e) => { e.preventDefault(); if (!pane.querySelector("#next")) check(pane.querySelector("#ans").value); };
    pane.querySelector("#ans").onkeydown = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); pane.querySelector("#dForm").requestSubmit(); } };
    pane.querySelector("#skip").onclick = () => { if (!pane.querySelector("#next")) check(""); };
    pane.querySelector("#ans").focus();
  }
  show();
}

/* ---------- 말하기 (따라 말하기 + 녹음 비교) ---------- */
function paneSpeak(ch, pane) {
  const src = store.get("speakSrc", "words");
  let items;
  if (src === "words") items = ch.words.map((w) => ({ es: w.es, ko: w.ko, audio: w.audio, pron: w.pron }));
  else if (src === "native") items = ch.dialogues.flatMap((d) => d.lines.map((l) => ({ es: l.native.es, ko: l.native.ko, audio: l.native.audio })));
  else items = sentencePool(ch);
  let i = 0;
  const best = store.get("speakBest", {});
  function show() {
    const it = items[i];
    const key = nn(ch.num) + ":" + norm(it.es);
    pane.innerHTML = `
      <div class="toolbar" style="justify-content:center"><div class="seg" role="group" aria-label="연습 범위">
        <button data-src="words" aria-pressed="${src === "words"}">단어</button><button data-src="sent" aria-pressed="${src === "sent"}">문장</button><button data-src="native" aria-pressed="${src === "native"}">원어민 표현</button></div></div>
      ${SR ? "" : `<div class="panel small">이 브라우저는 음성 인식이 안 돼요. 녹음해서 원어민 발음과 비교하는 연습은 할 수 있어요. 채점까지 하려면 Chrome이나 Safari에서 열어 주세요.</div>`}
      <div class="quiz">
        <div class="progress">${i + 1} / ${items.length}${best[key] ? ` · 최고 ${best[key]}점` : ""}</div>
        <div class="q">
          <div class="kind">듣고 따라 말해 보세요</div>
          <div class="prompt" style="font-size:24px">${esc(it.es)}</div>
          ${it.pron ? `<div class="pron">[${pron(it.pron)}]</div>` : ""}
          <div class="muted small">${esc(it.ko)}</div>
          <div class="row" style="justify-content:center;margin-top:14px;gap:12px">
            ${playBtn(it.es, it.audio).replace('class="play', 'style="width:56px;height:56px;font-size:18px" class="play')}
            ${SR ? `<button class="mic" id="mic" type="button" aria-label="말하기">🎤</button>` : ""}
            ${canRecord() ? `<button class="btn ghost" id="rec" type="button">● 녹음</button>` : ""}
          </div>
          <div id="res" aria-live="polite" style="margin-top:12px"></div>
          <div id="mine" style="margin-top:8px"></div>
        </div>
        <div class="row" style="justify-content:space-between;margin-top:12px">
          <button class="btn ghost" id="prev" type="button" ${i ? "" : "disabled"}>이전</button>
          <button class="btn" id="next" type="button">${i < items.length - 1 ? "다음" : "처음으로"}</button>
        </div>
      </div>`;
    pane.querySelectorAll("[data-src]").forEach((b) => b.onclick = () => { store.set("speakSrc", b.dataset.src); paneSpeak(ch, pane); });
    pane.querySelector("#prev").onclick = () => { i = Math.max(0, i - 1); show(); };
    pane.querySelector("#next").onclick = () => { i = (i + 1) % items.length; show(); };
    const res = pane.querySelector("#res");
    const mic = pane.querySelector("#mic");
    if (mic) mic.onclick = async () => {
      mic.classList.add("on"); res.innerHTML = '<span class="muted">듣고 있어요… 말해 보세요</span>';
      try {
        const { text, alts } = await listenOnce();
        // take the recognition alternative closest to the target
        const scored = alts.map((a) => ({ a, d: diffWords(it.es, a) })).sort((x, y) => y.d.score - x.d.score)[0];
        const pct = Math.round(scored.d.score * 100);
        if (pct > (best[key] || 0)) { best[key] = pct; store.set("speakBest", best); }
        activity.add(1);
        res.innerHTML = `<div class="es2 diff">${diffHtml(it.es, scored.d)}</div>
          <div class="muted small">들린 말: “${esc(scored.a || text)}”</div>
          <span class="tag ${pct >= 90 ? "good" : pct >= 60 ? "near" : "bad"}">${pct}점</span>
          ${pct >= 90 ? " 좋아요!" : pct >= 60 ? " 거의 됐어요. 빨간 단어를 다시 들어 보세요." : " ▶로 다시 듣고 천천히 말해 보세요."}`;
      } catch (err) { res.innerHTML = `<span class="tag bad">${esc(err.message)}</span>`; }
      mic.classList.remove("on");
    };
    const rec = pane.querySelector("#rec");
    if (rec) rec.onclick = async () => {
      if (rec.dataset.on) {
        delete rec.dataset.on; rec.textContent = "● 녹음";
        const url = await recorder.stop();
        if (url) pane.querySelector("#mine").innerHTML = `<div class="row" style="justify-content:center"><span class="small muted">내 발음</span><audio controls src="${url}"></audio></div>`;
        return;
      }
      try { stopAll(); await recorder.start(); rec.dataset.on = "1"; rec.textContent = "■ 멈춤"; }
      catch { res.innerHTML = '<span class="tag bad">마이크 권한을 허용해 주세요.</span>'; }
    };
  }
  if (items.length) show(); else pane.innerHTML = '<p class="empty">연습할 문장이 없어요.</p>';
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
    <div class="panel roleplay">
      <b>역할극</b> <span class="muted small">내 역할의 대사가 가려지고 한국어만 보여요. 상대 대사를 들은 뒤 직접 말해 보세요.</span>
      <div class="row" style="margin-top:8px">${Object.entries(d.roles).map(([k, r]) => `<button class="btn ghost" data-role="${k}" type="button">${esc(r.ko)} 역할</button>`).join("")}</div>
    </div>
    <p class="muted small">밑줄 친 단어를 누르면 뜻과 발음이 나와요.</p>
    <div id="dlg" class="${showKo ? "" : "hide-ko"}">${d.lines.map((ln, k) => `<div class="bubble-row ${ln.who === "A" ? "A" : "B"}" data-line="${k}">
      <div class="who" title="${esc(d.roles[ln.who]?.ko)}">${esc((d.roles[ln.who]?.ko || ln.who).slice(0, 4))}</div>
      <div class="bubble">${vers.map((v) => ver(ln, v)).join("")}</div></div>`).join("")}</div>`;
  pane.querySelectorAll("[data-di]").forEach((b) => b.onclick = () => { store.set("dlg" + ch.num, +b.dataset.di); paneTalk(ch, pane); });
  pane.querySelectorAll("[data-m]").forEach((b) => b.onclick = () => { store.set("dlgMode", b.dataset.m); paneTalk(ch, pane); });
  pane.querySelector("#ko").onchange = (e) => { store.set("dlgKo", e.target.checked); pane.querySelector("#dlg").classList.toggle("hide-ko", !e.target.checked); };
  pane.querySelectorAll("[data-role]").forEach((b) => b.onclick = () => rolePlay(ch, pane, d, b.dataset.role, mode === "textbook" ? "textbook" : "native"));
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

function rolePlay(ch, pane, d, me, v) {
  let k = 0;
  const scores = [];
  const lines = d.lines;
  pane.innerHTML = `<h2 style="margin-top:6px">${esc(d.title_es)} · 역할극</h2>
    <p class="setting">나는 <b>${esc(d.roles[me].ko)}</b> · ${v === "native" ? "원어민 표현" : "교재 표현"}으로 말해요.</p>
    <div id="rp"></div>
    <div class="row" style="margin-top:12px"><button class="btn ghost" id="quit" type="button">대화 화면으로</button></div>`;
  pane.querySelector("#quit").onclick = () => { stopAll(); paneTalk(ch, pane); };
  const box = pane.querySelector("#rp");
  async function step() {
    if (!document.body.contains(box)) return;
    if (k >= lines.length) {
      const avg = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
      box.insertAdjacentHTML("beforeend", `<div class="panel" style="text-align:center">대화를 끝까지 했어요.${avg !== null ? ` 평균 <b>${avg}점</b>` : ""}
        <div class="row" style="justify-content:center;margin-top:8px"><button class="btn" id="again" type="button">다시 하기</button></div></div>`);
      box.querySelector("#again").onclick = () => rolePlay(ch, pane, d, me, v);
      return;
    }
    const ln = lines[k], x = ln[v], mineTurn = ln.who === me;
    const row = document.createElement("div");
    row.className = `bubble-row ${ln.who === "A" ? "A" : "B"}`;
    row.innerHTML = `<div class="who">${esc((d.roles[ln.who]?.ko || ln.who).slice(0, 4))}</div><div class="bubble">${mineTurn
      ? `<div class="lab">내 차례 · 이렇게 말해 보세요</div><div class="ko" style="display:block;font-size:15px;color:var(--ink)">${esc(x.ko)}</div>
         <div class="row" style="margin-top:8px">${SR ? '<button class="mic small-mic" type="button" aria-label="말하기">🎤</button>' : ""}<button class="btn ghost reveal" type="button">정답 보기</button></div>
         <div class="out" aria-live="polite"></div>`
      : `<div class="ver"><div>${playBtn(x.es, x.audio, true)}</div><div><div class="txt">${tappable(ch, x.es)}</div><div class="ko">${esc(x.ko)}</div></div></div>`}</div>`;
    box.appendChild(row);
    row.scrollIntoView({ block: "nearest", behavior: "smooth" });
    k++;
    if (!mineTurn) { await speak(x.es, x.audio, row.querySelector(".play")); setTimeout(step, 350); return; }
    const out = row.querySelector(".out");
    const reveal = (extra = "") => {
      row.querySelectorAll(".mic,.reveal").forEach((b) => b.remove());
      out.innerHTML = `${extra}<div class="ver" style="margin-top:6px"><div>${playBtn(x.es, x.audio, true)}</div><div class="txt">${tappable(ch, x.es)}</div></div>
        <button class="btn small" type="button" style="margin-top:8px">계속</button>`;
      out.querySelector(".btn").onclick = (e) => { e.currentTarget.remove(); step(); };
    };
    row.querySelector(".reveal").onclick = () => reveal();
    const mic = row.querySelector(".mic");
    if (mic) mic.onclick = async () => {
      mic.classList.add("on"); out.innerHTML = '<span class="muted small">듣고 있어요…</span>';
      try {
        const { alts } = await listenOnce();
        const best = alts.map((a) => ({ a, d: diffWords(x.es, a) })).sort((p, q) => q.d.score - p.d.score)[0];
        const pct = Math.round(best.d.score * 100);
        scores.push(pct); activity.add(1);
        reveal(`<div class="es2 diff">${diffHtml(x.es, best.d)}</div><span class="tag ${pct >= 90 ? "good" : pct >= 60 ? "near" : "bad"}">${pct}점</span> <span class="muted small">“${esc(best.a)}”</span>`);
      } catch (err) { out.innerHTML = `<span class="tag bad">${esc(err.message)}</span>`; mic.classList.remove("on"); }
    };
  }
  step();
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
  for (const e of mineEntries()) if (all[wid(e.ch.num, e.w)]) entries.push(e);
  const due = entries.filter((e) => all[wid(e.ch.num, e.w)].due <= Date.now());
  $app.innerHTML = `<h1>복습</h1><p class="sub">여러 장에서 공부한 단어 중 다시 볼 때가 된 카드예요. 지금 ${due.length}장 · 전체 ${entries.length}장.</p><section id="pane"></section>`;
  const pane = document.getElementById("pane");
  if (!entries.length) { pane.innerHTML = `<div class="panel">아직 복습함이 비어 있어요. 장을 골라 플래시카드나 퀴즈를 먼저 해 보세요. <a href="#/">장 고르기</a></div>`; return; }
  flashSession(pane, due.length ? due : entries, { limitNew: 0, showChapter: true, back: '<a class="btn ghost" href="#/">처음으로</a>' });
}

/* ---------- 내 단어장 ---------- */
function mineEntries() {
  return mine.all().map((m) => ({ ch: { num: m.ch, es: index.chapters.find((c) => c.num === m.ch)?.es || "" },
    w: { key: "g_" + norm(m.es).replace(/\s+/g, "_"), es: m.es, ko: m.ko, en: m.en, pron: m.pron, img: null, audio: m.audio || null } }));
}
function renderMine() {
  const list = mine.all();
  $app.innerHTML = `<h1>내 단어장</h1>
    <p class="sub">대화·읽기에서 단어를 누르고 ☆를 누르면 여기에 모여요. ${list.length}개.</p>
    ${list.length ? `<div class="row" style="margin-bottom:12px"><button class="btn" id="mf" type="button">플래시카드로 외우기</button></div>
      <section id="pane"></section>
      <div id="mlist">${list.map((m) => `<div class="line">${playBtn(m.es, m.audio)}<div style="flex:1"><div class="es2"><b>${esc(m.es)}</b>${m.lemma && norm(m.lemma) !== norm(m.es) ? ` <span class="muted small">← ${esc(m.lemma)}</span>` : ""}</div>
        <div class="pron small">[${pron(m.pron || "")}]</div><div class="t">${esc(m.ko)} · ${esc(m.en)} · <a href="#/ch/${nn(m.ch)}/read">${nn(m.ch)}장</a></div></div>
        <button class="btn ghost small" data-rm="${esc(m.id)}" type="button" aria-label="빼기">빼기</button></div>`).join("")}</div>`
      : `<div class="panel">아직 저장한 단어가 없어요. 장의 <b>대화</b>나 <b>읽기</b>에서 모르는 단어를 눌러 보세요.</div>`}`;
  $app.querySelectorAll("[data-rm]").forEach((b) => b.onclick = () => { const m = mine.all().find((x) => x.id === b.dataset.rm); if (m) mine.toggle(m); renderMine(); });
  const mf = $app.querySelector("#mf");
  if (mf) mf.onclick = () => { $app.querySelector("#mlist").hidden = true; mf.hidden = true; flashSession($app.querySelector("#pane"), mineEntries(), { limitNew: 50, showChapter: true, back: '<a class="btn ghost" href="#/mine">목록으로</a>' }); };
}

/* ---------- 검색 ---------- */
async function renderSearch(q) {
  const chs = await Promise.all(index.chapters.map((c) => getChapter(c.num)));
  const qq = fold(q);
  const hits = [], seen = new Set();
  for (const ch of chs) {
    for (const w of ch.words) {
      if ([w.es, w.base, w.ko, w.en].some((x) => x && fold(x).includes(qq))) hits.push({ ch, w, kind: "word" });
    }
    for (const [form, e] of Object.entries(ch.glossary)) {
      if (e.key || seen.has(form)) continue;
      if (fold(form).includes(qq) || fold(e.lemma || "").includes(qq) || (e.ko || "").includes(q) || fold(e.en || "").includes(qq)) {
        seen.add(form); hits.push({ ch, form, e, kind: "gl" });
      }
    }
  }
  hits.sort((a, b) => (a.kind === b.kind ? 0 : a.kind === "word" ? -1 : 1));
  $app.innerHTML = `<h1>찾기</h1>
    <form class="search" id="searchForm" role="search"><input id="q" type="search" value="${esc(q)}" autocomplete="off" aria-label="단어 찾기"><button class="btn" type="submit">찾기</button></form>
    <p class="sub">“${esc(q)}” ${hits.length}개${hits.length > 60 ? " · 앞의 60개만 보여요" : ""}</p>
    <div class="wgrid">${hits.filter((h) => h.kind === "word").slice(0, 40).map((h) => wordCard(h.ch, h.w).replace("<article class=\"wcard\">", `<article class="wcard"><a class="chlink small" href="#/ch/${nn(h.ch.num)}">${nn(h.ch.num)} ${esc(h.ch.es)}</a>`)).join("")}</div>
    ${hits.some((h) => h.kind === "gl") ? `<h3>대화·읽기에 나온 말</h3>${hits.filter((h) => h.kind === "gl").slice(0, 30).map((h) => `<div class="line">${playBtn(h.form, h.e.audio, true)}<div><div class="es2"><b>${esc(h.form)}</b> <span class="muted small">${esc(h.e.lemma !== h.form ? "← " + h.e.lemma : "")}</span></div>
      <div class="t">${esc(h.e.ko)} · ${esc(h.e.en)} · <a href="#/ch/${nn(h.ch.num)}/read">${nn(h.ch.num)}장</a></div></div></div>`).join("")}` : ""}`;
  document.getElementById("searchForm").onsubmit = (e) => { e.preventDefault(); const v = document.getElementById("q").value.trim(); if (v) location.hash = "#/search/" + encodeURIComponent(v); };
}

/* ---------- 설정 ---------- */
function renderSettings() {
  const s = settings.get();
  $app.innerHTML = `<h1>설정</h1>
    <div class="panel"><h3 style="margin-top:0">하루 목표</h3>
      <div class="seg" role="group">${[10, 20, 40, 60].map((g) => `<button data-goal="${g}" aria-pressed="${s.goal === g}">${g}문제</button>`).join("")}</div></div>
    <div class="panel"><h3 style="margin-top:0">듣기 속도</h3>
      <div class="seg" role="group"><button data-rate="1" aria-pressed="${rate === 1}">보통</button><button data-rate="0.75" aria-pressed="${rate !== 1}">천천히</button></div></div>
    <div class="panel"><h3 style="margin-top:0">한글 발음 표기</h3>
      <label><input type="checkbox" id="hp" ${s.hidePron ? "checked" : ""}> 숨기기</label>
      <p class="muted small">익숙해지면 숨기고 소리로만 익혀 보세요. 한글로는 정확히 적을 수 없는 소리(r·rr·j 등)가 있어요.</p></div>
    <div class="panel"><h3 style="margin-top:0">화면</h3>
      <div class="seg" role="group">${[["auto", "기기 설정"], ["light", "밝게"], ["dark", "어둡게"]].map(([k, l]) => `<button data-theme="${k}" aria-pressed="${s.theme === k}">${l}</button>`).join("")}</div></div>
    <div class="panel"><h3 style="margin-top:0">진도 백업</h3>
      <p class="muted small">진도는 이 브라우저에만 저장돼요. 다른 기기로 옮기거나 브라우저 기록을 지우기 전에 파일로 받아 두세요.</p>
      <div class="row"><button class="btn" id="exp" type="button">백업 파일 받기</button>
        <label class="btn ghost" style="cursor:pointer">백업 불러오기<input type="file" id="imp" accept="application/json,.json" hidden></label>
        <button class="btn ghost" id="reset" type="button" style="color:var(--bad)">진도 모두 지우기</button></div>
      <div id="msg" class="small" style="margin-top:8px"></div></div>
    <div class="panel"><h3 style="margin-top:0">음성</h3>
      <p class="small">${esVoice ? `기기 스페인어 음성: <b>${esc(esVoice.name)}</b>` : "이 기기에서 스페인어 음성을 찾지 못했어요. 테두리가 옅은 ▶는 소리가 안 날 수 있어요. 기기 설정에서 스페인어(스페인) 음성을 내려받아 주세요."}</p>
      <p class="small">음성 인식(말하기 채점): ${SR ? "사용할 수 있어요" : "이 브라우저에서는 안 돼요 (Chrome·Safari 권장)"}</p></div>
    <p class="small"><a href="#/credits">사진 출처</a></p>`;
  $app.querySelectorAll("[data-goal]").forEach((b) => b.onclick = () => { settings.set({ goal: +b.dataset.goal }); renderSettings(); });
  $app.querySelectorAll("[data-rate]").forEach((b) => b.onclick = () => { rate = +b.dataset.rate; store.set("rate", rate); paintSpeed(); renderSettings(); });
  $app.querySelectorAll("[data-theme]").forEach((b) => b.onclick = () => { settings.set({ theme: b.dataset.theme }); renderSettings(); });
  $app.querySelector("#hp").onchange = (e) => settings.set({ hidePron: e.target.checked });
  const msg = $app.querySelector("#msg");
  $app.querySelector("#exp").onclick = () => {
    const data = {};
    try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k.startsWith("vv.")) data[k] = localStorage.getItem(k); } } catch { /* blocked */ }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify({ app: "vocabulario-visual", v: 1, saved: new Date().toISOString(), data }, null, 1)], { type: "application/json" }));
    a.download = `vocabulario-visual-backup-${today()}.json`; a.click();
    msg.textContent = "백업 파일을 받았어요.";
  };
  $app.querySelector("#imp").onchange = async (e) => {
    const f = e.target.files[0]; if (!f) return;
    try {
      const j = JSON.parse(await f.text());
      if (j.app !== "vocabulario-visual" || !j.data) throw new Error("이 앱의 백업 파일이 아니에요.");
      Object.entries(j.data).forEach(([k, v]) => { if (k.startsWith("vv.")) localStorage.setItem(k, v); });
      msg.textContent = "불러왔어요."; applySettings(); rate = store.get("rate", 1); paintSpeed();
    } catch (err) { msg.textContent = "불러오지 못했어요: " + err.message; }
  };
  $app.querySelector("#reset").onclick = () => {
    if (!confirm("모든 진도(복습 카드, 학습 기록, 내 단어장, 설정)를 지울까요? 되돌릴 수 없어요.")) return;
    try { Object.keys(localStorage).filter((k) => k.startsWith("vv.")).forEach((k) => localStorage.removeItem(k)); } catch { /* blocked */ }
    msg.textContent = "지웠어요."; applySettings();
  };
}

/* ---------- keyboard shortcuts (desktop) ---------- */
document.addEventListener("keydown", (e) => {
  if (e.target.closest("input,textarea,select,button,a") || e.metaKey || e.ctrlKey || e.altKey) return;
  const card = document.getElementById("card");
  if (card && (e.key === "ArrowLeft" || e.key === "1")) { document.getElementById("no")?.click(); }
  else if (card && (e.key === "ArrowRight" || e.key === "2")) { document.getElementById("yes")?.click(); }
  else if (/^[1-4]$/.test(e.key)) { const c = document.querySelectorAll(".choice:not(:disabled)")[+e.key - 1]; if (c) c.click(); }
  else if (e.key === "Enter" && document.getElementById("next")) { document.getElementById("next").click(); }
});

/* ---------- offline / install (service worker, only over http/https) ---------- */
if ("serviceWorker" in navigator && location.protocol.startsWith("http")) {
  window.addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));
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
  const bundled = (window.VV_DATA && window.VV_DATA.credits) || {};
  const docs = await Promise.all(index.credits.map((f) => bundled[f] ?? fetch("media/credits/" + f).then((r) => r.text())));
  $app.innerHTML = `<h1>사진 출처</h1>
    <p class="sub">사진은 모두 Wikimedia Commons의 실제 사진이고, 각 라이선스(CC0, CC BY, CC BY-SA 등)에 따라 표기했어요. 음성은 스페인 표준 발음 음성 합성이에요.</p>
    <div class="md">${docs.map((d) => `<div class="panel">${mdToHtml(d)}</div>`).join("")}</div>`;
}

applySettings();
route();
