---
tags: [record, tracker]
date: 2026-10-23
stake: 0
purpose: test whether each mechanism beats the market's own probability over many nights
---

# Mechanism tracker — 2026-10-23 (zero stake, pre-registered 15:50 ET)

Locked in **before tip-off** at the time-stamped price. No money, paper or real. We grade each one against the market's own devigged probability: if a mechanism has an edge, its hit rate will run **above** the average `p_market` over many nights. One night tells us nothing; ~150+ entries per mechanism starts to tell us something.

| Hypothesis | Player | Game | Prop | Price o/u | Book | p_market (side) | Context |
|---|---|---|---|---|---|---:|---|
| H1 vacated usage → over | Brandon Miller | ATL@CHA | pts over 24.5 | -114/-114 | FanDuel | 0.5 | White, Knueppel, G. Williams OUT |
| H1 vacated usage → over | Naz Reid | ATL@CHA | pts over 18.5 | -108/-122 | FanDuel | 0.486 | same |
| H1 vacated usage → over | Anthony Davis | TOR@WAS | pts over 22.5 | -112/-118 | FanDuel | 0.494 | Dybantsa OUT |
| H1 vacated usage → over | Kyshawn George | TOR@WAS | pts over 14.5 | -118/-112 | FanDuel | 0.506 | Dybantsa OUT |
| H1 vacated usage → over | Stephen Curry | MEM@GSW | pts over 24.5 | -128/-104 | FanDuel | 0.524 | Butler, Porzingis, Moody OUT |
| H1 vacated usage → over | Paolo Banchero | MIN@ORL | pts over 22.5 | -104/-128 | FanDuel | 0.476 | A. Black, Isaac, Penda OUT |
| H1 vacated usage → over | Cooper Flagg | DAL@IND | pts over 24.5 | -118/-112 | FanDuel | 0.506 | Lively, C. Martin, Aldama OUT |
| H2 replacement C → reb over | Jalen Smith | CHI@MIL | reb over 7.5 | -113/-113 | FanDuel | 0.5 | starts for Claxton (aggregator) |
| H2 replacement C → reb over | Daniel Gafford | DAL@IND | reb over 7.5 | +110/-146 | FanDuel | 0.445 | replaces Lively |
| H2 replacement C → reb over | Jaxson Hayes | NOP@UTA | reb over 5.5 | -148/+112 | FanDuel | 0.559 | replaces Nurkic |
| H3 blowout fav star → under | Kawhi Leonard | TOR@WAS | pts under 24.5 | -120/-110 | FanDuel | 0.49 | TOR -8.5 |
| H3 blowout fav star → under | Deni Avdija | POR@SAC | pts under 21.5 | -118/-112 | FanDuel | 0.494 | POR -9.5 |
| H3 blowout fav star → under | Pascal Siakam | DAL@IND | pts under 23.5 | -110/-120 | FanDuel | 0.51 | IND -7.5 |
| H3 blowout fav star → under | Luka Doncic | LAC@LAL | pts under 32.5 | -108/-118 | DraftKings (reference) | 0.51 | LAL -9.5; no FD market |
| H3 blowout fav star → under | Austin Reaves | LAC@LAL | pts under 22.5 | -111/-115 | DraftKings (reference) | 0.504 | LAL -9.5; no FD market |

**Grading:** Job A tomorrow (R14) pulls these 15 stat lines; Claude fills `actual`/`hit` in `Record/mechanism_tracker.csv` and keeps a running table by hypothesis in [[Market Intel]].

**Why these and not bets:** FanDuel's prices matched the other books on all of them, and with no calibrated NBA model yet there was no edge to stake. The tracker is how we find out which of these stories is real before the engine starts acting on them.

**v2 relabel (16:55 ET, before the 7 pm tips; no entries changed):** Miller, Davis, Curry, Banchero, Flagg → H1a; Reid, K. George → H1b; Smith, Gafford, Hayes → H2 (confirmed-start rule unverified); Leonard, Avdija, Siakam, Doncic, Reaves → H3-legacy (spreads below the v2 ≥10 threshold). No controls tonight → graded vs the side-bias prior. See [[Mechanism Tracker]].
