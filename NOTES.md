# NOTES — news-image-20261117

Entry: a 1024x1024 PNG front page, "THE WORLD IN ONE DAY — TUESDAY, 17 NOVEMBER 2026".
Built 18 Nov 2026 WIB (session started after the competition opened).

## Stories in the image (all reported on 17 Nov 2026)

Lead — Kerch Bridge: Ukrainian strike overnight 16–17 Nov destroyed a road
arch and span of the Kerch (Crimean) Bridge; road and rail traffic suspended.
Zelenskyy called it the 7th stage of a weeks-long operation; Moscow vowed to
rebuild. Russian missiles hit Kyiv's North and South bridges the same night.
Sources: Le Monde, The War Zone, Kyiv Independent / Nexus Europa, Algenom.

Hormuz: tankers hit by mines near the Strait of Hormuz and caught fire
(IRGC navy / Reuters / Al Jazeera); a third US carrier, USS Theodore
Roosevelt, entered CENTCOM waters, joining George H.W. Bush and George
Washington. Sources: Algenom, Zark News.

Shenzhen summit: China confirmed Xi Jinping, Donald Trump and Vladimir Putin
will meet in Shenzhen on Thursday 19 Nov, on the APEC sidelines.
Sources: Algenom, Open Chronicle, FeedCast.

Grid (12): Kyiv bridges shut / Pentagon fails its audit for the 9th year
($4.8tn assets) / White House requires approval before staff testify to
Congress / US Commerce moves to close the AI-chip rental loophole / five
European states plan a joint return facility in Rwanda / Japan scrambles jets
after suspected Russian airspace violation / UK sanctions 8 Israeli
construction firms over West Bank settlements / 128 states meet in Geneva on
a lethal-autonomous-weapons treaty / Houthis advance on Aden as government
forces pull back from the Red Sea coast / COP31 finance talks stall in
Antalya, Nepal seeks billions for the Himalayas / Bitcoin at a four-month low
near $62,000 / Voyager passes one light-day from Earth (25.9bn km).
Sources for the four new grid stories: asaspress + Middle East Forum (Yemen),
BrainSharing Daily Intelligence Briefing D170 (COP31, Bitcoin, Voyager).

In brief (11): Iran fires drones at a US radar base in Bahrain (intercepted) /
US intelligence warns of an alleged Iranian plot against Trump officials
(CNN, reported as an allegation) / US reports 13 babies born with congenital
measles since 2025 / bus crash in Uttarakhand, India, kills at least 6 /
China and Canada agree tariff cuts / Netanyahu camp accused of tipping off
police arrests of Arab party workers on Israeli election day (Just Security) /
UK, Australia, Canada and Italy urge Israel to open Gaza aid crossings
(asaspress) / Gérard Depardieu drops appeal and admits sexual assault charge
in Paris (asaspress) / magnitude 6.6 earthquake near Tual, Indonesia, no
tsunami threat (USGS via Asia Daily / The Watchers) / JPMorgan Chase hit by a
nationwide outage (BrainSharing D170) / Moscow says it intercepted 1,441
Ukrainian drones overnight (Open Chronicle).

## Round 2 (18 Nov 2026) — breadth expansion, 16 → 26 stories

The live board (1,125 valid entries; top entries carry 24–35 stories)
showed breadth as the clear weakness. The lead story, photos, map and
masthead are unchanged; space was freed by shrinking the lead photo
(220→160px) and the second-row photos (130→100px), which made room for a
third grid row (8→12 stories) and a longer IN BRIEF (5→11 items). Map
markers 1/2/7 in Europe were de-crowded by fanning their labels in
different directions. Every new fact was confirmed from a dated
17 Nov 2026 source (see above); nothing was invented..

## Round 3 (18 Nov 2026) — final improvement round: visual richness + thumbnail legibility

Second row reworked from 3 columns (2 photos + map) to 4 columns
(3 photos + map), each 234px wide: a fourth photo panel was added for
the Tual quake (magnitude 6.6 near Tual, Indonesia, no tsunami — a story
already on the page in IN BRIEF, now promoted; it leaves the brief strip,
so the story count stays exactly 26: 1 lead + 3 photo + 12 grid + 10
brief). New panel is an original AI-generated illustration
(`assets/media-generation-quake-tual-0-*.webp`, stilt houses + seismic
ripples, no text); two variants were generated, the brighter one kept.
Photo headlines now share one fitted size (21px serif bold); summaries
13px, max 3 lines. The map shrank to 234px and now carries dots only —
markers 1/2/7 cluster in Europe at this width, so the legend below (3
lines, 11px) carries the numbering. Grid text untouched (13/18/13px);
grid moved up 12px (rows at 712/780/848) to make room.

IN BRIEF rebuilt for the ~300px judge view: 12px → 15px, every item
shortened and given a bold kicker (IRAN, US INTEL, MEASLES, INDIA,
TARIFFS, ISRAEL, GAZA, DEPARDIEU, JPMORGAN, MOSCOW), word-level flow
keeps kickers bold across line breaks. Verified by downscaling entry.png
to 300px and reading it: masthead, date, lead headline and all three
photo headlines read; the brief strip reads as distinct bold-led
nuggets instead of a grey smear.

Gate check (verified locally): entry.png 1024x1024 RGB, 490,130 bytes
(limit 1,048,576); 12/12 grid headlines one line, 12/12 summaries
exactly 2 lines; brief 4 lines ending at y=1004 (bottom rule 1016).

## How it was built

- `compose.py` draws everything with PIL (Liberation Serif/Sans). All text is
  code-rendered, so no garbled text.
- Photo panels: three original AI-generated illustrations in `assets/`
  (kerch-bridge, hormuz-tanker, shenzhen-summit). No copied or stock photos.
- Map: drawn from Natural Earth country outlines (`assets/world.geo.json`).
- `main.ts` copies `entry.png` to the output dir (starter pattern).

## Gate check (verified locally)

- `entry.png`: 1024x1024, RGB PNG, 495,353 bytes (limit 1,048,576).
- 26 stories total (1 lead + 2 photo stories + 12 grid + 11 in brief).
- Layout verified programmatically: all 12 grid headlines fit one line,
  all 12 summaries wrap to exactly 2 lines, IN BRIEF wraps to 4 lines
  ending at y≈1001 (bottom rule at y=1016).
- Program run: `MAKEFUN_OUTPUT_DIR=out node main.ts` copies entry.png to out/.
