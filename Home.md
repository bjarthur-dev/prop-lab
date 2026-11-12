---
tags: [moc, home]
---

# Prop Lab — Home

The player-prop projection system: **AI does the research, code does the math, the record decides what's real.**

## The three rules
1. **A projection above the line is not a good over** — only +EV bets count, and the default output is [[Daily Workflow#Pass|PASS]].
2. **Log every decision** — bets, paper bets, and passes — in the [[Bet Log]]. The record is the product.
3. **Never trust a number you can't source** — every probability comes from the [[Math Engine]] or is marked UNKNOWN.

## Scoreboard (updated every morning, 11-09 rebuild)
- [[Audit]] — real-money results: profit with and without the biggest win, by bet type, stated chances vs what happened, closing-line value
- [[Hypotheses]] — every betting idea graded against every NBA line we have; the "Forward test" table is the one to trust
- [[Market Backtest]] — how accurate each book's price is, and whether "this book is off the others" pays
- [[Promos]] — every promo taken and what it was worth (the main source of profit)
- [[Ideas Today]] — today's lines that match the lead ideas (paper only)
- Tools: `engine/fair.py` (price any slip), `engine/consensus_scan.py` (price edges, 6%+ only). Rules: [[Lessons]] "11-09 System audit"

## Start here
- [[Rules]] — **the single source of every number** (sizing, caps, pass rule, books, graduation). Wins any conflict.
- [[Slate Playbook]] — how 1 game vs 10+ games, start times and day types change bet count, slips and exposure
- [[Daily Workflow]] — the checklist for every slate
- [[Roles & Automation]] — who does what: Perplexity = Scout (sourced facts → `Inbox/`), Claude = Engine + Auditor, Python = data layer, you = Decider; the daily ET clock
- [[Perplexity Prompt]] — standing instructions for Perplexity (Jobs A–E)
- [[NFL Engine]] — v1: line → plays → script-aware pass rate → shares → simulated yards/TDs (PAPER/WATCH only)
- [[NBA Engine]] — v1 projection engine (minutes → rates → market-anchored sim), how it decides, how to run it on Windows
- [[Mechanism Tracker]] — v2: zero-stake theory tests with matched controls, H1a–H8 + DvP placebo, grader `engine/tracker.py`
- [[MLB Module]] — MLB chains (pitcher Ks, batter H/TB/HRR), World Series micro-slate plan, Scout MLB fields
- [[Cloud Pipeline]] — **what runs with the laptop off**: GitHub Actions (results, Scout ingest, watchdog, tests), Claude cloud morning settlement 08:17, Perplexity delivery by GitHub issue
- [[Afternoon Card Task]] — the daily 14:52 bet card (live pilot, [[Rules]] §9) — create it in the Claude app
- [[Bankroll Growth Plan]] — the ranked, research-backed plan: tokens/boosts first, price-edge singles, what to avoid
- [[Bankroll]] — live-pilot bankroll and limits
- [[Laptop Refresh Task]] — keep NBA data current from the laptop (Windows startup/daily, or a Claude task)
- [[Morning Settlement Task]] — the morning settlement prompt (now a cloud scheduled task)
- [[Researcher Prompt]] — reusable facts-only researcher + separate falsifying reviewer
- [[Upgrade Roadmap]] — what to build next, in order
- [[Research - Advanced NFL and MLB mechanisms]] — NFL engine v1 design (volume → shares → simulated tails), K model v1 (PA-by-PA, hook, park), N1–N10 + M1–M8 theories
- [[Research - Advanced NBA mechanisms]] — shot zones, schemes, rotations, reb/ast tracking, market patterns; engine v1.5 plan + tracker v2 (H4–H8)
- [[Research - Upgrade Report]] — the full audit + research behind all of this
- [[The Guide]] — the full methodology (17 chapters: math, per-sport modeling, parlays, pick'em, form/streaks)
- [[Math Engine]] — the prop-engine code: devig, distributions, EV, Kelly
- [[Master Prompt - NFL]] / [[Master Prompt - NBA]] — archived one-game dossiers (superseded by [[Researcher Prompt]])

## Tonight / recent slates
- [[2026-10-23 NBA + WS G1]] — 12 NBA + World Series G1: 124 NBA props scanned → all PASS; 1 paper bet (Misiorowski u6.5 K)
- [[2026-10-22 TNF + NBA]] — Patriots-Bears + Nuggets-Thunder: the first full two-sport slate

## The record
- [[2026-11-11 Review]]: **LIVE 1–3, +$1.75** on $9.05 cash (Pick6 Giddey/Mobley ast unders ✓ +$7.80; DK 30% boost parlay ✗ F. Wagner 3PM; CBB 11-leg ✗; Betr Crosby/Allen ✗ Bucks only). Paper/watch/dropped 7–6 + 1 void (MPJ 3 ast sank every slip; dropped Barrett u2.5 would have won). Mean CLV +1.2% on 5 (18:18 stand-in, no close; favorites −1.1%, Randle price edge +10.4%). Tracker H3 hyp 1/3 vs control 7/15 (H3 net +0.9, SE 10.2). Shadow NBA 4,873, model −2.7%, blend +0.0%; NFL −5.8% on 1,039. NBA logs complete through 11-11 (3 teams filled). 4 flags. Bankroll **$52.80**
- [[2026-11-10 Review]]: **LIVE 3–1, +$10.05** on $14 (KOTC Giannis u5.5 ast ✓ +$5.25; Pick6 Brunson/Sabonis ✓ +$5.80 and Wagner/LeBron ✓ +$4.00, payouts assumed; Duke −7.5 boost ✗ −$5; Betr entries not placed). Paper/watch/dropped 3–4 settled, 5 unsettled (OKC@POR + Bane single-source). Mean CLV +1.9% on 9 (price-edge watches +6.5%, favorite legs −3.9%; true closes +0.6% on 2). Tracker H3 hyp 2/4 vs control 2/3 (H3 net +3.0, SE 10.6). Shadow NBA 4,599, model −3.1%, blend −0.0%; NFL −5.8% on 1,039. NBA logs complete through 11-10 (5 teams filled). 6 flags. Bankroll **$51.65** (confirm Pick6 payouts)
- [[2026-11-09 Review]]: **LIVE 5–22, −$3.44** on $45.04 cash + $5 bonus (Pick6 1–11 −$10.08; Betr promo 2-picks 2–2 +$9; MNF unders SGP ✓ +$5.32; Maluach/Harper SGP ✓ +$3.36). Paper/watch 6–4 (Draymond u5.5 price edge ✓; long shot ✗ Siakam 5 threes; Yurosek unsettled, −10.9% CLV). Mean CLV −1.1% on 9 (true closes −3.1% on 6). Tracker 7/12 (N1 hyp 2/4 vs control 3/4; N1 net −1.9, SE 4.6, n=91). Shadow NBA 4,400, model −3.3%, blend −0.1%; NFL −5.8% on 1,039. NBA logs complete through 11-09 (4 teams filled). 4 flags. Bankroll **$41.60**
- [[2026-11-08 Review]]: **LIVE 3–8–1, −$14.45** on $85 (Moonshot $68 incl. a $40 = 67%-of-roll round; NE ML live ✗ GB 45–27; SGPx ✗ only on the added Murphy u2.5 3PM). Paper/watch 6–2 + 1 void (Portis u8.5 price edge ✓ +3.5% CLV; Herro/Murphy/Jaquez/Egbuka ✓; Reaves ✗; NFL Slip A ✗ Jacobs injury / Taylor 46). Mean CLV +1.1% on 5 (true closes −0.8% on 2). Tracker 62 rows, 45.2% vs 50.0% p (N1 net −0.7, SE 4.8, n=87). Shadow NBA 4,077, model −3.5%, blend +0.3%; NFL −5.8% on 1,039. NBA logs complete through 11-08. 4 flags. Bankroll file **$44.04** (P&L implies $45.04, please check)
- [[2026-11-07 Review]]: **LIVE 3–9, −$9.18** on $58.67 (CFB 4-leg 30% ✓ +$25.72, Georgia ML 50% ✓, Rossi/Toffoli Pick6 ✓; NBA Pick6 ✗ Durant 1 three, SGPx ✗ Draymond 13 ast / Mitchell 5 threes, DEN SGP ✗ Zubac 12 reb; 6 CFB/NHL ✗). Paper legs 3–3; mean CLV −0.4% on 5 (2 true closes +1.8%). Holiday drop would have won (+5.4%). Tracker H1 ✗ vs control ✓, H3 ✓/✓. Shadow NBA 3,785, model −3.8%, blend +0.4%; NFL −8.3% on 590. **NBA logs incomplete: CLE.** 2 unsettled (Shamet, Proctor). Bankroll **$59.49**
- [[2026-11-06 Review]]: **LIVE 0–3, −$25.00** on $25 (SGPx 50% boost ✗ Williams 6 / McCain 5 reb; SGA most points ✗ Mitchell 35; Pick6 2-pick ✗). That was 27% of the roll. Paper legs 1–2, mean CLV −0.4% on 6 (with the dropped ones); drops right 2 of 3. Price-edge 75 legs, CLV +2.7%. Tracker H3 0/2 vs control 1/2 (net +4.7). Shadow NBA 3,516, model −3.5%, blend +0.5%; NFL −8.3% on 590. **NBA logs incomplete: MIL.** 3 single-source rows unsettled. Bankroll **$68.67**
- [[2026-11-05 Review]]: **LIVE 2–3, +$53.67** on $25 (Pick6 3-pick ✓ +$41.41 and 2-pick ✓ +$27.26, both winnings-boosted; JAX SGP ✗ Meyers 4 rec; Pick6 4-pick ✗ Henry 57; SGPx ✗ Bane 6 reb / Giannis 18 R+A). That was 36% of the roll vs the 2% cap. Paper legs 4–2, mean CLV −1.2% on 6 (NFL = pregame proxy). Tracker B2B ✓ vs control ✗ (Wagner 15 ast); H4 ✓/✓. Shadow NBA 3,160, model −3.5%, blend +0.7%; NFL −8.3% on 590. NBA logs complete through 11-05. Bankroll **$123.67**
- [[2026-11-04 Review]]: **LIVE 0–2, −$16.81** on $16.81 (Pick6 ✗ Quickley 1 reb; 25%-boost parlay ✗ Giannis 14 reb in OT). That was **19% of the roll vs the 2% day cap**. Paper: SAFE singles 2–1 (Reid ✓, Edey ✗, Buzelis ✓), and the card SGPx ✗ on Vassell 7 reb. CLV only for DAL@SAS (Vassell +0.5%, Champagnie −0.5%). Price-edge 72 legs, CLV +3.1%. Tracker U1 1/1 vs control 0/1. Shadow NBA 3,070, model −3.2%, blend +0.7%; NFL −8.3% on 590. NBA logs complete through 11-04 (SAS 11-02 closed). Bankroll **$70.00**
- [[2026-11-03 Review]]: **No slate** (Election Day), nothing settled. Shadow unchanged (NBA 2,766, model −3.3%, blend +0.5%; NFL −8.3% on 590). **NBA logs incomplete: SAS (11-02).** Bankroll **$86.81**
- [[2026-11-02 Review]]: **LIVE 0–2, −$4.00** on $4 (Brown u1.5 3PM ✗ 4 threes; SGPx ✗ on the added Giddey 10 ast / Brown legs). The card SGPx (Anunoby/Brunson/Vassell reb unders) would have won 3/3; the Carter Jr. PASS would have won (6 pts). Close only for OKC@CLE (credit guard), so CLV is a T−124 proxy. Price-edge scan 6–4 on the day; 69 legs, CLV +3.1%. Tracker 3/4 (H3 ✓/✓, H4* ✓/✗; H4 ID clash). Shadow NBA 2,766 graded, model −3.3%, blend +0.5%; NFL −8.3% on 590. **NBA logs incomplete: SAS.** Bankroll **$86.81**
- [[2026-11-01 Review]]: **LIVE 2–3, +$94.67** on $32.52 (NBA SGPx 50% boost ✓ +$105.67; NFL alt parlay ✗ on Coleman 1–4; SNF SGP ✗ on Goedert 4 rec; SGPx ✓ +$13.38; Garland hedge ✗ −$16.38). Paper 2 legs ✓ / 2 ✗, Pick6 paper ✗ (Walker 4 rec), Melton PASS would have lost. No new true-close CLV (NFL close coverage gap). Tracker N1 10/25 vs control 10/18 (N1 net −2.6, SE 5.1, n=63); H2 confirmed start ✓. Shadow 2,791 graded (NBA model −3.9%, blend +1.1%; **NFL −8.3%** on 590). NBA logs complete through 11-01; 0 open flags. Bankroll **$90.81** (after the $30 tools withdrawal)
- [[2026-10-31 Review]]: **LIVE 4–2, +$0.14** on $16 (5 off-card boosts 4–1 +$7.14: Canelo UD, Wemby 43, IND–MINN and UF–UGA unders ✓, WNBA G7 SGP ✗ on Dream +1.5; $7 boosted reb parlay ✗ on Acuff 5 reb, +17.6% EV vs close). Wemby boost +20% vs close. Running CLV 31 entries, **+1.9%** (bet/paper/live 15, +4.7%). Tracker H1a 1/3 vs control 0/2 (net +26.5, SE 10.3, n=27); H2 0/2 (1/7). Shadow 1,996 graded (NBA model −3.9%, blend +1.2%). NBA logs incomplete: HOU/OKC/MEM/SAC. 3 single-source flags. Bankroll **$28.14**. **Off-card bets → kill-switch question**
- [[2026-10-30 Review]]: **LIVE none confirmed, $0** (Durant u3.5 ast ✓ at +123; +$6.15 if you placed the $5). First true close: Durant **+3.1% CLV**; price-edge 11/11 positive. Running CLV 25 entries, **+1.3%** (bet/paper rows only: 14, +3.6%). Morant flag cleared ✓. Tracker H1a 2/2 vs control 0/2 (net +25.9, SE 11.4, n=24); H2 0/2. Shadow 1,853 graded (NBA model −4.1%, blend +0.9%). NBA logs through 10-30 (12 bench players filled). Bankroll $34.00
- [[2026-10-29 Review]]: **LIVE none logged, $0** (7:15 list unconfirmed; at $5 each it nets +$4.50: Pick6 Hubbard TD + Jacobs/Love ✓, Harden 4 ast ✗ single and parlay). Paper: Wiggins o3.5 reb ✓ (+3.3% CLV), Murphy 16.5 ✓, Harden −2.9% CLV. Running CLV 22 entries, **+0.8%**; price-edge 10/10 positive. Tracker H1a 3/3 vs control 0/3 (net +18.2, SE 12.1). Shadow 1,632 graded (NBA model −4.0%, blend +1.0%). 2 single-source flags. Bankroll $34.00
- [[2026-10-28 Review]]: **LIVE none placed, $0.** Paper 1–3 legs, both slips lost (Trae 8 ast, 2 short). CLV: price_edge 4/4 positive (+2.8 / +3.8 / +2.9 / +7.4%); segment 8/8, mean +5.7%; running 19 entries, **+0.7%**. Tracker H1a hyp 0/3 vs control 1/2. Shadow 1,506 graded (NBA model −4.0%, blend +1.0%; matchup v1 −6.2% on 795). **NBA gate review due (1,346 props), under-lean unexplained.** Bankroll $39.00
- [[2026-10-27 Review]]: **LIVE 0–1, −$5.00** (off-card Pick6 Tatum < 25.5 ✗ 40 in OT / Harper > 16.5 ✗ 13). Paper 0–1 (Thybulle 3PM). PASSed Cade 8+/Reaves 7+ slip would have won. CLV: price_edge 4/4 positive, mean +7.2% (none placed); running 15 entries, −0.2%. Shadow 1,069 graded (NBA model −4.9%, blend +2.0%; matchup v1 −1.1% on 201). **Bankroll $39.00** (DK 27 + Betr 12). Kill-switch question for the user
- [[2026-10-26 Review]]: **LIVE 0–1, −$5.00** (Pick6 Miller 20+ ✓ / JJJ 15+ ✗, he left hurt; a discounted line). Paper 3–5. CLV: price_edge legs **+6.8% / +4.9%**, model WATCH legs −4.2% / −3.7%; running 13 entries, −1.5%. Shadow 942 graded (NBA model −4.1%, blend +2.6%; NFL model −2.8%). 10-25 NFL flags settled from pbp (20–15 final). **Bankroll $25.00**
- [[2026-10-25 Review]]: 0 staked bets; paper-track **18–13, 4 open** (NFL WATCH 16–12, NBA 2–1; +3.35 notional u). CLV only on SNF: 5 entries, all negative, mean **−4.0%**; running CLV 9 entries, −2.6%. Tracker N1 hyp 20/36 vs controls 16/35 (noise). 11 NFL players flagged single-source. Bankroll $30.00
- [[2026-10-24 Review]]: 0 staked bets; paper-track 1–3 (Mitchell u AST and Harden u REB lost at **+2.5% / +2.0% CLV**, Rasmussen o5.5 K lost at −3.7%; Pick6 HRR slip won, $0). Tracker hyp 4/6 vs controls 4/7. Running CLV 4 entries, −0.95%. Bankroll $30.00
- [[2026-10-23 Review]] — 0 staked bets; WATCH Misiorowski u6.5 K won (3 K) at **−4.6% CLV**; tracker 4/15 vs market p 0.50 (H1 0/7, H2 1/3, H3-legacy 3/5; noise). Live pilot bankroll $30.00
- [[Bet Log]] — 2026-10-22 settled **4–5, −$14.17** at $10 stakes (−$1.42 at 1%), 0/9 closes captured — see [[2026-10-22 Review]] and [[2026-10-22 Audit]]
- `Record/Bets.base` — Bases views: open bets, exposure by game, CLV by market, reason-code ledger, calibration bins (one note per bet from [[_Bet Template]])
- [[Review Template]] — run after every slate settles

## Libraries
- [[Market Intel]] — line moves, RLM, books vs pick'em apps, CLV lessons
- [[_Player Template]] — one note per player you track (form/streak protocol)
- [[_Slate Template]] — copy for each new slate

## Where things live
- **Source of truth: GitHub** https://github.com/bjarthur-dev/prop-lab — Claude commits here; Perplexity reads it; Obsidian (PC + phone) pulls it via the Obsidian Git plugin.

## Older cloud-side notes
- Guide: `player-prop-projection-guide.md` · Engine: `prop-engine/` · Log: `prop-engine/bets.csv`
- Target state ([[Upgrade Roadmap]] #4, #11): a local DuckDB is the source of truth, and the vault mirrors it. Until then, treat `bets.csv` as canonical and note any changes made on the cloud side here.
