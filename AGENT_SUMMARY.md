# Fix: `steam_scan` crashes on long-format odds snapshots

Issue: [#100](https://github.com/bjarthur-dev/prop-lab/issues/100) — "Card: 2026-11-22 card | 0 live | Place today"

The card note flags the same defect twice under **Data gaps**:

> The NFL part of `steam_scan` crashed (the NFL board file has no over/under columns). The NBA part ran.

and again in the 18:22 late update ("`steam_scan` NFL part still crashes (same missing over/under columns)").

## Root cause

`engine/steam_scan.py:scan()` globs **every** CSV in `data/odds/<sport>/<date>/`, skipping only
`games*` and `*alt*` files, then unconditionally reads `o.over` / `o.under`:

```python
o = o[o.market.isin(MK[sport]) & o.over.notna() & o.under.notna()].copy()
```

Most snapshots (`board_`, `pregame_`, `open_`, `close_`, `pick6_`) are **wide** — one row per
player/market/line with separate `over` and `under` price columns. But
`engine/cloud/odds_snapshot.py:177` writes a second, **long** format for the on-demand
`nflx:` / `nbalive:` / `nfllive:` tags (and `cbbprops_`): `…,player,side,line,price` — one row
per side, with no `over`/`under` columns at all.

Those files pass both existing filters, so `o.over` raises
`AttributeError: 'DataFrame' object has no attribute 'over'` and the whole scan dies.

On 2026-11-22 the NFL directory contains `nflx_1112.csv`, which is exactly what killed the NFL
leg of the scan — matching the note's diagnosis.

**The bug was wider than the issue reports.** The NBA leg "ran" on 11-22 only because it was
invoked at 14:53 and 18:22, before the in-game `live_*.csv` pulls landed at 20:53+. Replaying
the scan over the stored data today, the NBA leg crashes on **every date from 2026-11-16
onward** (13 sport-days total), and `steam_scan.py grade` — which loops every NBA date to
rebuild `Record/Shadow/Steam Report.md` — had been dead since 11-16 for the same reason.

## Fix

One line, in `engine/steam_scan.py`, alongside the existing per-file guards:

```python
if "over" not in o or "under" not in o: continue   # long-format snapshots (live_/nflx_/cbbprops_: one row per side) carry no two-way price
```

Skipping (rather than pivoting `side`→`over`/`under`) is the correct behaviour, not just the
cheap one:

- A steam scan compares a sharp book's **first vs. latest pregame** devigged price. The `live_`
  files are in-game lines pulled after tip-off; folding them in would overwrite the `last`
  sharp price with a live number and manufacture fake "steam". The skip keeps the method honest.
- It is schema-based, not filename-based, so it also covers `cbbprops_` and any future tag that
  reuses the long writer in `odds_snapshot.py`.
- It matches the file's existing idiom (`if o.empty or "snap_et" not in o: continue`).

## Verification

`python` 3.14 / pandas 2.3.3. Ran from the repo root.

**1. Reproduced the crash, confirmed it clears.** Before the change, `python engine/steam_scan.py
2026-11-22 nfl` ends in the `AttributeError` above. After:

```
== NFL 2026-11-22: sharp moves >= 2 pts (ev_steam adds the +3 pt steam premium seen in the data)
        player     market  line  side  move_pts  fair_last     dk  ev_last  ev_steam       window
  Kirk Cousins   rush_yds   1.5 under       4.7      0.541 -113.0      2.0       7.7 11:08->18:43
Jordan Watkins receptions   0.5 under       3.0      0.467  103.0     -5.2       0.9 11:08->18:43
```

Cousins U1.5 rush yds is the same NFL price edge the card lists under **WATCH**, so the restored
output agrees with what the card recorded by hand.

**2. No regression on anything that already worked.** Imported the pre-fix and post-fix modules
side by side and compared `scan()` over all 56 stored sport-days:

- 43 sport-days ran before → output is **byte-identical** (`DataFrame.equals` is `True` for every one).
- 13 sport-days raised `AttributeError` before → all now return results
  (nba 11-16…11-22, nfl 11-15…11-19, 11-22, 11-23).

**3. Grade mode restored.** `python engine/steam_scan.py grade` now completes and rebuilds the
report: `All steam legs: 876, win 54.2% vs last fair 51.3%, ROI +0.6% as DK singles.`

**4. Repo test suites pass** (the three commands in `.github/workflows/tests.yml`):

```
engine/nba/tests/test_synthetic.py  ALL SYNTHETIC TESTS PASSED
engine/nba/tests/test_minutes.py    ALL MINUTES TESTS PASSED
engine/nfl/tests/test_nfl.py        ALL NFL TESTS PASSED
```

No TypeScript, lint, or package manifest in this repo; nothing else to run.

The regenerated `Record/Shadow/Steam Report.md` and `data/edges/*_steam_*.csv` from those
verification runs were reverted, so the commit is the one-line code change only.

## Concerns for a reviewer

- **The same latent crash exists in `engine/edge_grade.py:close_fair()`** (line 29), which reads
  each odds file individually and calls `o.over.notna()` with only the `games_` prefix filtered
  out. It will fail on `live_`/`nflx_` files exactly as `steam_scan` did. I left it alone to keep
  this to one logical change, but it is worth a follow-up. `engine/fair.py:load()` is safe by
  luck — it `pd.concat`s all frames first, so the union of columns gives the long-format rows
  `NaN` in `over`/`under` and the `notna()` filter drops them.
- **Silent skip.** Like the neighbouring `games`/`alt` guards, the new line drops files without
  logging. Consistent with the file's style, but it does mean a future wide-format file with a
  renamed price column would vanish from the scan instead of erroring.
- **The restored NBA rows are new output, not just a restored crash.** Dates 11-16 onward now
  produce steam lists that previously produced nothing, which shifts the aggregate in
  `Steam Report.md` (the numbers in §3 above are post-fix). That is the intended behaviour, but
  anyone comparing against a stale copy of the report will see it move.
- I did not add a test. The repo's suites are self-contained synthetic scripts for the NBA/NFL
  models with no harness for the top-level `engine/*.py` scanners, so a `steam_scan` test would
  have meant introducing new test scaffolding — beyond the minimal-change scope. The 56-day
  before/after comparison in §2 is the evidence in its place.
