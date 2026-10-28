"""NFL matchup-context data from nflverse (works in the cloud; GitHub releases). Run after fetch_nfl.py.
    python engine/nfl/fetch_context.py [season]
Writes engine/data/nfl/context/<season>/:
  snaps.csv          offense/defense snap share per player-game (PFR via nflverse)
  ngs_rec.csv        Next Gen Stats receiving per week: separation, cushion, aDOT, share of team air yards, YAC over expected
  ngs_rush.csv       NGS rushing: rush yards over expected, % of carries vs 8+ man boxes, time to LOS
  ngs_pass.csv       NGS passing: time to throw, aggressiveness, CPOE, air yards
  pfr_def.csv        PFR advanced defense per player-week: targets/yards allowed, pressures, blitzes, missed tackles
  pfr_rec.csv / pfr_rush.csv / pfr_pass.csv   PFR advanced offense (drops, broken tackles, yards after contact, pressure faced)
  ftn.csv            FTN charting per play: box count, blitzers, pass rushers, play action, motion, screen, RPO, contested
"""
import os, sys, time, urllib.request
import pandas as pd

SEASON = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
OUT = f"engine/data/nfl/context/{SEASON}"
B = "https://github.com/nflverse/nflverse-data/releases/download/"
FILES = {
    "snaps.csv": f"snap_counts/snap_counts_{SEASON}.csv",
    "pfr_def.csv": f"pfr_advstats/advstats_week_def_{SEASON}.csv",
    "pfr_rec.csv": f"pfr_advstats/advstats_week_rec_{SEASON}.csv",
    "pfr_rush.csv": f"pfr_advstats/advstats_week_rush_{SEASON}.csv",
    "pfr_pass.csv": f"pfr_advstats/advstats_week_pass_{SEASON}.csv",
    "ftn.csv": f"ftn_charting/ftn_charting_{SEASON}.csv",
}
NGS = {"ngs_rec.csv": "nextgen_stats/ngs_receiving.csv.gz", "ngs_rush.csv": "nextgen_stats/ngs_rushing.csv.gz",
       "ngs_pass.csv": "nextgen_stats/ngs_passing.csv.gz"}

def fetch(url, path):
    for a in range(3):
        try:
            urllib.request.urlretrieve(url, path); return True
        except Exception as e:
            print(f"retry {a+1} {url}: {e}"); time.sleep(3 * (a + 1))
    return False

def main():
    os.makedirs(OUT, exist_ok=True); ok = 0
    for name, rel in FILES.items():
        p = os.path.join(OUT, name)
        if fetch(B + rel, p):
            if name == "ftn.csv":   # keep the columns the matchup layer uses (file is ~3 MB a season)
                d = pd.read_csv(p, low_memory=False)
                keep = ["nflverse_game_id", "season", "week", "nflverse_play_id", "n_offense_backfield", "n_defense_box", "is_motion",
                        "is_play_action", "is_screen_pass", "is_rpo", "is_qb_out_of_pocket", "is_catchable_ball", "is_contested_ball",
                        "is_drop", "n_blitzers", "n_pass_rushers"]
                d[[c for c in keep if c in d.columns]].to_csv(p, index=False)
            print(f"ok   {name}: {len(pd.read_csv(p, low_memory=False))} rows"); ok += 1
        else:
            print(f"FAIL {name}")
    for name, rel in NGS.items():
        tmp = os.path.join(OUT, "_tmp.csv.gz")
        if fetch(B + rel, tmp):
            d = pd.read_csv(tmp, low_memory=False); d = d[d.season >= SEASON - 1]
            d.to_csv(os.path.join(OUT, name), index=False); os.remove(tmp)
            print(f"ok   {name}: {len(d)} rows ({SEASON-1}-{SEASON})"); ok += 1
        else:
            print(f"FAIL {name}")
    print(f"{ok} files -> {OUT}")

if __name__ == "__main__":
    main()
