# AUDIT v6 — vocabulario_visual_v6 (Índice · ch01 · ch02 · ch11 · Créditos)
Checked 2026-11-02 05:35 KST · 11 pages A4 · 18M

## 1. Fonts (pdffonts)
- Type 3: **0**. All fonts are embedded subsets (CID TrueType). No system fallback (NanumGothic/DejaVu/Tinos) left.
- AAAAAA+Jost-Regular — CID TrueType (emb yes)
- BAAAAA+BodoniModa-Italic — CID TrueType (emb yes)
- CAAAAA+GowunBatang-Regular — CID TrueType (emb yes)
- DAAAAA+GowunBatang-Bold — CID TrueType (emb yes)
- EAAAAA+SpecialElite-Regular — CID TrueType (emb yes)
- FAAAAA+Jost-Regular — CID TrueType (emb yes)
- GAAAAA+Caveat-Regular — CID TrueType (emb yes)
- HAAAAA+BodoniModa-Regular — CID TrueType (emb yes)
- IAAAAA+Caveat-Regular — CID TrueType (emb yes)
- JAAAAA+NanumPen-Regular — CID TrueType (emb yes)
- Fixed in v6: Korean text inside Jost / Special Elite (FALSO AMIGO label, answer key, billete "승차권") had fallen back to NanumGothic → Gowun fallback added (outside @font-face). An earlier attempt broke @font-face and turned Jost into Type 3; that was caught and fixed.

## 2. Images (pdfimages -list, x-ppi, smask excluded)
- Photos and cutouts: 78 placed images, **min 312 ppi** (ch01 opener 2579×3648 at 210×297 mm). ch02 knife (re-cropped) 328 ppi; everything else ≥342 ppi (cards 450 ppi).
- Paper texture: 300 ppi (8 pages).
- All real photos from Wikimedia Commons, no generated images.

## 3. Font size
- HTML text minimum: **7.0 pt** (chips, credits body, legends).
- SVG stamp text (CTM-scaled): minimum **7.03 pt** (postmarks enlarged from 32 to 40 mm; poster from 34 to 36 mm).

## 4. Korean pronunciation rules (scripted, 60/60 items, _build/audit_v6.py)
- p/t/k → ㅃ/ㄸ/ㄲ (no ㅌ or ㅋ anywhere): pass.
- ㅍ appears only for f; every f has ㅍ: pass.
- ll/y + vowel → 야/요 series: pass.
- c(e,i)/z → ㅅ: pass.
- Bold stressed syllable present in every item: pass.
- **Flagged: 0**.

## 5. Gloss accuracy (manual)
- §4 o1: dientes "이들" → "이(치아)들".
- §4 o3: Necesito → "(나는) 필요하다" (subject drop shown).
- §3 secador: "말리개" → "말리는 것 · ~의 · 머리 = 드라이어".
- ch02 cafetera: 커피포트 → 커피 메이커 (moka; card note "cafetera italiana").
- §7 variants note cleaned up.
- Rest checked: ch01 20, ch02 20, ch11 20.

## 6. Layout (Playwright DOM check + visual check of every shot)
- No horizontal overflow. No card/section past the page margin. Credits flow over 2 pages (38 + 32 blocks), and page 2 fits.
- Remaining reported "overlaps" are intentional: the §3 header box sits over its own cards by 2 mm, and the tilted ch01 card 06 is 1.9 mm over tag 11's tape.
- Índice: rows re-spaced (7.8 mm) so that title, KO, grammar and example no longer collide; ends at 272 mm.
- ch11 props: the red/blue rect stamps clipped their text and covered the legend → removed. The billete moved to the empty band under the legend, and the dashed perforation removed.

## 7. Brands and signs
- Removed: ch02 opener stall sign (new opener); EMT bus logos/ads/plate; Airoh helmet; Metro sign (new photo); Renfe/AVE nose; stop ad panel; airline livery (new plane); backpack logo (new photo); Hisense fridge logo.
- Removed (found during the v6 audit): Zwilling knife engraving and handle badge (blade retouched, then re-cropped); Bajaj microwave logo, model and door label.
- Still visible (tiny or not a brand): SEAT badge on the car (very small), Madrid taxi livery, signage text on the Mercado Central facade (a place name), tiny fridge display text, possible faint marks on the toaster.

## 8. Web
- web/index.html: 60 word cards, ch01 sentences (§4 blocks, §5 clitic, §6 subject drop, §8 answers, scenes), 85 mp3 files (edge-tts es-ES-ElviraNeural), 0.75× toggle, 0 broken images.
