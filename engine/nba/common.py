import re, unicodedata
import numpy as np

TEAMS = {"Atlanta Hawks":"ATL","Boston Celtics":"BOS","Brooklyn Nets":"BKN","Charlotte Hornets":"CHA","Chicago Bulls":"CHI",
"Cleveland Cavaliers":"CLE","Dallas Mavericks":"DAL","Denver Nuggets":"DEN","Detroit Pistons":"DET","Golden State Warriors":"GSW",
"Houston Rockets":"HOU","Indiana Pacers":"IND","LA Clippers":"LAC","Los Angeles Clippers":"LAC","Los Angeles Lakers":"LAL",
"Memphis Grizzlies":"MEM","Miami Heat":"MIA","Milwaukee Bucks":"MIL","Minnesota Timberwolves":"MIN","New Orleans Pelicans":"NOP",
"New York Knicks":"NYK","Oklahoma City Thunder":"OKC","Orlando Magic":"ORL","Philadelphia 76ers":"PHI","Phoenix Suns":"PHX",
"Portland Trail Blazers":"POR","Sacramento Kings":"SAC","San Antonio Spurs":"SAS","Toronto Raptors":"TOR","Utah Jazz":"UTA",
"Washington Wizards":"WAS"}

def norm_name(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    s = s.lower().replace(".", "").replace("'", "")
    s = re.sub(r"\b(jr|sr|ii|iii|iv)\b", "", s)
    return re.sub(r"\s+", " ", s).strip()

def american_to_dec(a):
    a = float(a); return 1 + a / 100 if a > 0 else 1 + 100 / -a

def implied(a): return 1 / american_to_dec(a)

def devig(over, under):
    po, pu = implied(over), implied(under); return po / (po + pu)

def nb_draw(rng, mean, vmr):
    """Negative binomial with given mean array and variance/mean ratio; Poisson if vmr<=1.05."""
    mean = np.maximum(mean, 1e-6)
    if vmr <= 1.05:
        return rng.poisson(mean)
    p = 1.0 / vmr
    r = mean * p / (1 - p)
    return rng.negative_binomial(r, p)
