# AGENT_SUMMARY — bounty #100

**Commit:** `dca76fd` — `fix: Card: 2026-11-22 card | 0 live | Place today`
**Files changed:** 1 (`engine/steam_scan.py`, one line)

## Root cause

The card reports the same defect twice:

- Data gaps: *"The NFL part of `steam_scan` crashed (the NFL board file has no over/under columns). The NBA part ran."*
- Late update 18:22: *"`steam_scan` NFL part still crashes (same missing over/under columns); NBA part ran."*

`scan()` in `engine/steam_scan.py` globs **every** CSV in `data/odds/<sport>/<date>/`, skipping
only files named `games*` or containing `alt`, then unconditionally reads `o.over` / `o.under`:

```python
if o.empty or "snap_et" not in o: continue
o = o[o.market.isin(MK[sport]) & o.over.notna() & o.under.notna()].copy()
```

Two snapshot writers in `engine/cloud/odds_snapshot.py:177` emit a **different, long-format schema** —
`snap_et,game,start_et,book,market,player,side,line,price` (one row per side) instead of the wide
`...,line,over,under,...` the board/pregame/open/close files use:

- `nflx_*.csv` — on-demand NFL market pulls (`data/odds/nfl/2026-11-22/nflx_1112.csv`)
- `live_*.csv` — in-game props (14 files across `data/odds/nba/2026-11-16 … 2026-11-21`)

Neither name is filtered, so pandas raises `AttributeError: 'DataFrame' object has no attribute
'over'` and the whole sport's scan dies. Reproduced before the fix:

```
$ python engine/steam_scan.py 2026-11-22 nfl
AttributeError: 'DataFrame' object has no attribute 'over'   # steam_scan.py:20
```

The issue only blames the NFL side, but **the same bug silently broke NBA** on every date that has a
`live_*.csv` (11-16, 11-17, 11-18, 11-19, 11-20, 11-21) and therefore broke
`python engine/steam_scan.py grade`, which loops over all NBA dates. 11-22 NBA happened to have no
`live_` file, which is why "the NBA part ran" that day.

## Fix

Guard on the schema rather than on one column, so any snapshot that is not in the wide over/under
format is skipped the same way `games*`/`alt` files already are:

```diff
-        if o.empty or "snap_et" not in o: continue
+        if o.empty or not {"snap_et", "over", "under"} <= set(o.columns): continue   # long-format snapshots (side/price columns: nflx_, live_) are a different schema -> skip, not crash
```

Reasoning:

- **Schema check, not a filename check.** Matches the existing `"snap_et" not in o` guard one token
  over, and covers future long-format writers (`nbalive:`, `nflweek:` tags) without another edit.
- **Skip rather than pivot.** `engine/nfl/prop_calibration.py:23` shows the repo's pivot idiom for
  this schema, so converting `nflx_` was the alternative. I did not, for two reasons: the long-format
  set also contains `live_*` **in-game** prices, and feeding post-tip prices into a scan whose whole
  premise is *"Pre-tip moves are information"* (module docstring) would corrupt the first→last move
  computation, not fix it; and the repo's own note in `Slates/2026-11-22 NFL card.md:103` scopes
  `nflx` schema support as a separate piece of work across `fair.py`, `matchup.py` and `pick6_scan`.
  Exclusion is also what the card author already did by hand ("I excluded it with a wrapper and did
  not change any code", line 70).

## Verification

Reported crash is gone — NFL now produces its steam list:

```
$ python engine/steam_scan.py 2026-11-22 nfl
== NFL 2026-11-22: sharp moves >= 2 pts
  Kirk Cousins    rush_yds   1.5 under 4.7  0.541 -113.0  2.0  7.7  11:08->18:43
  Jordan Watkins  receptions 0.5 under 3.0  0.467  103.0 -5.2  0.9  11:08->18:43
```

That `Cousins U1.5 rush yds` row independently corroborates the card's own WATCH line
("Cousins U1.5 rush yds −106 (+4.2%, only 2 books)"), i.e. the restored NFL output is sane.

- `python engine/steam_scan.py 2026-11-22` (default both sports, how the pipeline calls it) → exit 0,
  both `== NBA` and `== NFL` sections printed.
- `python engine/steam_scan.py 2026-11-16 nba` / `11-19` / `11-21` → previously `AttributeError`, now
  produce output.
- `python engine/steam_scan.py grade` → previously crashed on 11-16, now completes and writes
  `Record/Shadow/Steam Report.md`: *855 steam legs, win 53.6% vs last fair 51.3%*; *DK lagging: 105,
  win 54.3%, ROI +3.5%* — in line with the docstring's documented 55.6% edge.
- **No regression.** On 2026-11-22 NBA (a date with no long-format file) the full output CSV is
  byte-identical pre- and post-fix (23 rows), checked by stashing the fix, regenerating, and diffing.
- CI suite from `.github/workflows/tests.yml`, all green before and after:
  `engine/nba/tests/test_synthetic.py`, `engine/nba/tests/test_minutes.py`,
  `engine/nfl/tests/test_nfl.py`, `engine/mlb/k_model_v1.py`. No test covers `steam_scan`; there is
  no `package.json`/TypeScript in this repo, so no `npm test`/`tsc` step applies.

## Concerns for a reviewer

1. **The card's `nflx` request is only partly addressed.** This fixes the crash; it does not make
   `steam_scan` *use* `nflx_` data. `Slates/2026-11-22 NFL card.md:103` asks for that schema to be
   supported in `fair.py`, `matchup.py` and `pick6_scan` — out of scope here (>5 files, and it needs
   a pregame/live split decision first). If you do want it in the steam scan, the right shape is a
   pivot like `prop_calibration.py:23` **plus** a `snap_et < start_et` pregame filter so `live_` rows
   can't leak in.
2. **No regression test added.** The repo has no test harness for `steam_scan` (tests live under
   `engine/nba/tests`, `engine/nfl/tests` and are model-level, synthetic-fixture tests), and adding
   one would mean new fixture files beyond the one-line fix. The one-line guard is covered by the
   manual reproduction above.
3. **Nothing else in the dirty tree was touched.** The working tree already had ~30 modified files at
   session start (`engine/out/*.csv`, `status/*.json`, and several `engine/*.py` that differ from HEAD
   by line endings only — equal insert/delete counts on every line). I deliberately did **not**
   `git add -A`; the commit is the single code file. My verification runs did rewrite
   `data/edges/*_steam_*.csv` and `Record/Shadow/Steam Report.md`; I restored those to HEAD and
   deleted the newly created `data/edges/2026-11-22_steam_nfl.csv` so no generated artifact is in the
   commit. Worth knowing: the committed `data/edges/2026-11-22_steam_nba.csv` is **stale** — it was
   written when the latest snapshot was 18:19, while the repo now holds 18:43 and 19:03 snapshots, so
   a fresh run legitimately yields 23 rows with a `...->19:03` window instead of 44 with `...->18:19`.
   That drift predates this fix (confirmed: identical output with the fix reverted).
4. **The betting content of the issue needed no action.** The card itself is a decision log; the only
   code defect it reports is the `steam_scan` crash. The two boost-only slips, stakes and the `#433`
   settlement are operational notes, not software behavior.
