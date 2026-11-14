# Combo Correlations (NBA, 2025-26 + 2026-27)
Anchor = each team's top scorer. Pairs need 20+ shared games. Spearman correlation per pair, then the median across pairs.

## Teammates
| anchor stat | other player stat | role | pairs | median corr | 25-75% |
|---|---|---|---|---|---|
| star pts | pts | 2nd scorer | 24 | -0.02 | -0.13 to +0.15 |
| star pts | pts | big (7+ rpg) | 28 | -0.00 | -0.12 to +0.13 |
| star pts | pts | other rotation | 219 | -0.06 | -0.17 to +0.05 |
| star pts | pts | playmaker (5+ apg) | 19 | -0.03 | -0.09 to +0.06 |
| star ast | pts | 2nd scorer | 24 | +0.13 | -0.09 to +0.22 |
| star ast | pts | big (7+ rpg) | 28 | +0.04 | -0.07 to +0.24 |
| star ast | pts | other rotation | 219 | +0.07 | -0.05 to +0.19 |
| star ast | pts | playmaker (5+ apg) | 19 | +0.14 | +0.05 to +0.21 |
| star pts | reb | 2nd scorer | 24 | +0.03 | -0.11 to +0.13 |
| star pts | reb | big (7+ rpg) | 28 | +0.04 | -0.01 to +0.20 |
| star pts | reb | other rotation | 219 | +0.00 | -0.09 to +0.12 |
| star pts | reb | playmaker (5+ apg) | 19 | +0.06 | -0.02 to +0.10 |
| star pts | ast | 2nd scorer | 24 | +0.08 | +0.01 to +0.15 |
| star pts | ast | big (7+ rpg) | 28 | +0.05 | -0.06 to +0.10 |
| star pts | ast | other rotation | 219 | +0.02 | -0.10 to +0.14 |
| star pts | ast | playmaker (5+ apg) | 19 | +0.06 | -0.07 to +0.11 |
| star reb | reb | 2nd scorer | 24 | -0.04 | -0.14 to +0.08 |
| star reb | reb | big (7+ rpg) | 28 | +0.01 | -0.06 to +0.13 |
| star reb | reb | other rotation | 219 | +0.01 | -0.09 to +0.12 |
| star reb | reb | playmaker (5+ apg) | 19 | +0.09 | -0.05 to +0.18 |
| star ast | ast | 2nd scorer | 24 | -0.02 | -0.10 to +0.07 |
| star ast | ast | big (7+ rpg) | 28 | -0.04 | -0.15 to -0.00 |
| star ast | ast | other rotation | 219 | +0.00 | -0.12 to +0.10 |
| star ast | ast | playmaker (5+ apg) | 19 | +0.02 | -0.08 to +0.06 |

## Pooled (z-scores, all rotation players vs the top scorer)
| anchor | other | teammates corr (n) | opponents corr (n) |
|---|---|---|---|
| star pts | pts | -0.036 (8243) | +0.063 (9352) |
| star pts | reb | +0.037 (8243) | +0.013 (9352) |
| star pts | ast | +0.039 (8243) | +0.026 (9352) |
| star ast | pts | +0.099 (8243) | +0.010 (9352) |
| star reb | reb | -0.001 (8243) | +0.030 (9352) |

Read: positive = they go up together (stack overs, or unders); negative = one up, the other down (pair over with under). DK's SGP prices bake in its own guesses; edges come where its guess differs.