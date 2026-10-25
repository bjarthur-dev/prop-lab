---
job: C
date: 2026-10-25
run_at: 2026-10-25T09:30:22-04:00
sport: [NFL]
status: new
incidents_self_check: 0
---

# NFL news and reference price board

NFL-only scope, Sunday Eastern date. All prices are reference feed observations, not executable offers. Retrieval began at 09:30 ET, at the Paris start; PIT@NO quotes are not certified pregame and may already be stale. All other prices can change before kickoff. No current-day Job B file was present, so changes since Job B are UNKNOWN; statuses below are a separately labeled current snapshot, not asserted changes.

Source quotes in arrays are exact short fragments from the response (player/selection, line and each available price), not a fabricated continuous sentence. odds_ts arrays preserve the feed's exact Unix seconds in over/under order; this is a timestamp representation, not a probability. Missing sides remain UNKNOWN. YAML merge anchors resolve every quote to its book, price_type, source_url, url and retrieved_at. Each fenced block is independently parseable.

```yaml
{request_responses: [{&b req_id: R13, &c status: &d OUT_OF_SCOPE, &e answer: 'Job A results, not today''s NFL Job C.'}, {
      *b: R14, *c: *d, *e: 'Job A NBA results, not today''s NFL Job C.'}, {*b: R15, *c: *d, *e: 'MLB results, not today''s
        NFL Job C.'}, {*b: R16, *c: *d, *e: 'Saturday MLB starter props, not today''s NFL Job C.'}, {*b: R17, *c: &f PARTIAL,
      *e: '12 Sunday games below, with FanDuel and DraftKings main spreads, totals and moneylines. DAL@PHI Monday and NE@CHI
        Thursday close excluded by today''s-only instruction.'}, {*b: R18, *c: *f, *e: 'Official current report and attributed
        Sunday news below. Friday-only timestamp, WR1/TE1 depth ranks and confirmed replacements UNKNOWN. Barkley and McKee
        Monday questions excluded.'}, {*b: R19, *c: *f, *e: 'Six Sunday outdoor locations below. Hourly forecast observations
        bracketing non-hour kickoffs are preserved separately, not interpolated. Monday Philadelphia excluded.'}, {*b: R20,
      *c: *f, *e: FanDuel main RB/TE receiving yards <=24.5 and WR receiving yards >=40; one available main RB rushing-attempt
        book per player. TD depth ranks UNKNOWN; TD prices and alternate lines not transcribed under the GitHub issue-body
        cap.}, {*b: R21, *c: UNKNOWN, *e: 'Every listed player''s 2026 target share, catch rate, YPR, carry share, YPC, inside-10
        carry share and red-zone/end-zone target share UNKNOWN. Every team''s 2025/2026 PROE UNKNOWN; attempted Sharp page
        unavailable. No season shares inferred from odds.'}], broad_board: {*c: NOT_APPLICABLE, reason: Standing points/rebounds/assists/threes
      and minutes-ranked top-four board is NBA-specific; user restricted this run to today's NFL games. No invented NFL equivalent.},
  read_audit: {instructions: Fresh raw fetch; updated 2026-10-24., rules: System/Rules.md v3; read., playbook: System/Slate
      Playbook.md; read., requests: 'Inbox/Requests/2026-10-24 requests.md; newest available, no 2026-10-25 file at retrieval.',
    bets: 'Read Record/Bets/ and its two files; only substantive note was settled MLB WATCH, no open NFL bet note.'}}
```

```yaml
{injury_snapshot: [{&b player: Lamar Jackson, team: BAL, &c status: OUT, &d reason: Ankle, &e source_type: &f official league
        injury report, &g source_url: &h 'https://www.nfl.com/injuries/', quote: [Lamar Jackson, QB, Ankle, &o Limited Participation
          in Practice, Out], &i retrieved_at: &j '2026-10-25T09:31:05-04:00', &k report_time: &l UNKNOWN}, {*b: Baker Mayfield,
      team: TB, *c: &m QUESTIONABLE, *d: Thumb, *e: *f, *g: *h, quote: [Baker Mayfield, QB, Thumb, &q Full Participation in
          Practice, &p Questionable], *i: *j, *k: *l}, {*b: David Montgomery, team: HOU, *c: OUT, *d: Groin, *e: *f, *g: *h,
      quote: [David Montgomery, RB, Groin, &r Did Not Participate In Practice, Out], *i: *j, *k: *l}, {*b: &n Breece Hall,
      team: NYJ, *c: *m, *d: Quadricep, *e: *f, *g: *h, quote: [*n, RB, Quadricep, *o, *p], *i: *j, *k: *l}, {*b: Jordan Mason,
      team: MIN, *c: *m, *d: Thumb, *e: *f, *g: *h, quote: [Jordan Mason, RB, Thumb, *q, *p], *i: *j, *k: *l}, {*b: Quinshon
        Judkins, team: CLE, *c: *l, *d: *l, *e: *f, *g: *h, quote: [Quinshon Judkins, RB, *q], *i: *j, *k: *l}, {*b: Mike
        Evans, team: SF, *c: OUT, *d: 'Ribs, Achilles', *e: *f, *g: *h, quote: [Mike Evans, WR, 'Ribs, Achilles', *r, Out],
      *i: *j, *k: *l}, {*b: Deebo Samuel Sr., team: SF, *c: OUT, *d: &s Hamstring, *e: *f, *g: *h, quote: [Deebo Samuel Sr.,
        WR, *s, *r, Out], *i: *j, *k: *l}, {*b: Emeka Egbuka, team: TB, *c: OUT, *d: 'Concussion, Foot', *e: *f, *g: *h, quote: [
        Emeka Egbuka, WR, 'Concussion, Foot', *o, Out], *i: *j, *k: *l}, {*b: Theo Johnson, team: NYG, *c: DOUBTFUL, *d: Neck,
      *e: *f, *g: *h, quote: [Theo Johnson, TE, Neck, *r, Doubtful], *i: *j, *k: *l}, {*b: Tyler Warren, team: IND, *c: OUT,
      *d: Groin, *e: *f, *g: *h, quote: [Tyler Warren, TE, Groin, *r, Out], *i: *j, *k: *l}, {*b: Rashee Rice, team: KC, *c: OUT,
      *d: 'Hamstring, Knee', *e: *f, *g: *h, quote: [Rashee Rice, WR, 'Hamstring, Knee', *r, Out], *i: *j, *k: *l}, {*b: Brian
        Robinson, team: ATL, *c: OUT, *d: *s, *e: *f, *g: *h, quote: [Brian Robinson, RB, *s, *r, Out], *i: *j, *k: *l}, {
      *b: Jeremiyah Love, team: ARI, *c: OUT, *d: Ankle, *e: *f, *g: *h, quote: [Jeremiyah Love, RB, Ankle, *r, Out], *i: *j,
      *k: *l}, {*b: Zach Charbonnet, team: SEA, *c: OUT, *d: Knee, *e: *f, *g: *h, quote: [Zach Charbonnet, RB, Knee, *q,
        Out], *i: *j, *k: *l}, {*b: &t Puka Nacua, team: LAR, *c: *m, *d: Calf, *e: *f, *g: *h, quote: [*t, WR, Calf, *r,
        *p], *i: *j, *k: *l}], news_updates: [{*b: *n, team: NYJ, *c: *m, *e: &u named beat reporter, &v reporter: Ian Rapoport,
      *g: &w 'https://amp.nfl.com/news/week-7-injuries-sunday-pregame-2026-nfl-season', quote: 'RB Breece Hall (quad; questionable)
        is unlikely to play Sunday against Miami, NFL Network''s Ian Rapoport reported.', *i: *j}, {*b: *t, team: LAR, *c: *m,
      *e: *u, *v: Adam Schefter, *g: *w, quote: 'WR Puka Nacua (calf; questionable): Los Angeles is optimistic that Nacua
        will play Sunday against the Raiders, ESPN''s Adam Schefter reported.', *i: *j}, {*b: Olamide Zaccheaus, team: ATL,
      *c: *m, *e: *u, *v: Ian Rapoport, *g: *w, quote: 'WR Olamide Zaccheaus (shoulder; questionable) is not expected to play
        against San Francisco, NFL Network''s Ian Rapoport reported.', *i: *j}, {*b: Mike Washington Jr., team: LV, *c: *m,
      *e: *u, *v: Jeremy Fowler, *g: *w, quote: 'RB Mike Washington Jr. (foot/back) is a game-time decision against the Rams,
        ESPN''s Jeremy Fowler reported.', *i: *j}], confirmed_starters: *l, role_changes_since_B: *l, staleness: Expectations
    are not official active/inactive determinations; recheck official inactives before each start.}
```

```yaml
{&A game_id: &B PIT@NO 2026-10-25, start_et: '2026-10-25T09:30:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&s Pittsburgh Steelers, &t New Orleans Saints, '2026-10-25T13:30:00Z'], &d retrieved_at: &e '2026-10-25T09:30:58-04:00'},
  quote_defaults: [{<<: &D {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &X {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &ba {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i New Orleans Saints +3, line: 3, odds: -110, &k odds_ts: 1792933026.174517, quote: [
            *i, '-110']}, {*j: &l Pittsburgh Steelers -3, line: -3, odds: -110, *k: 1792933026.174517, quote: [*l, '-110']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Over 43.5, line: 43.5, odds: -104, *k: 1792932936.0530508, quote: [*q,
            '-104']}, {*j: &r Under 43.5, line: 43.5, odds: -118, *k: 1792932936.0530508, quote: &x [*r, '-118']}]}, {<<: *m,
      *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: -166, *k: 1792933026.174517, quote: &y [*s, '-166']},
        {*j: *t, line: *u, odds: 140, *k: 1792933026.174517, quote: &z [*t, '140']}]}, {<<: &w {book: *v, *f: *g, *b: *c,
        *d: *e}, *n: R17, *o: point_spread, *p: [{*j: *i, line: 3, odds: -102, *k: 1792934202.3710458, quote: [*i, '-102']},
        {*j: *l, line: -3, odds: -118, *k: 1792934202.3710458, quote: [*l, '-118']}]}, {<<: *w, *n: R17, *o: total_points,
      *p: [{*j: *q, line: 43.5, odds: -102, *k: 1792934202.3710458, quote: [*q, '-102']}, {*j: *r, line: 43.5, odds: -118,
          *k: 1792934202.3710458, quote: *x}]}, {<<: *w, *n: R17, *o: moneyline, *p: [{*j: *s, line: *u, odds: -166, *k: 1792934202.3710458,
          quote: *y}, {*j: *t, line: *u, odds: 140, *k: 1792934202.3710458, quote: *z}]}], weather: {*n: R19, *b: 'https://api.open-meteo.com/v1/forecast?latitude=48.924&longitude=2.36&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&start_date=2026-10-25&end_date=2026-10-25',
    *d: '2026-10-25T09:31:51-04:00', exact_kickoff_forecast: *u, hourly_samples: [{time_et: '2026-10-25T09:00-04:00', temp_f: 59.7,
        wind_mph: 15.6, gust_mph: 31.3, precip_probability_pct: 0, quote: ['2026-10-25T09:00', '59.7', '15.6', '31.3', '0']},
      {time_et: '2026-10-25T10:00-04:00', temp_f: 59.7, wind_mph: 16.3, gust_mph: 33.3, precip_probability_pct: 0, quote: [
          '2026-10-25T10:00', '59.7', '16.3', '33.3', '0']}]}, props: [{*n: R20, &E player: &C Darnell Washington, *o: &F receiving_yards,
      *A: *B, &G identity: {&H position: TE, team: *s, *b: &I 'https://api.opticodds.com/api/v3/players', quote: [*C, TE,
          *s], *d: &K '2026-10-25T09:36:54-04:00'}, &L quotes: [{<<: *D, line: 24.5, over: -113, under: -113, quote: [*C,
            '24.5', '-113', '-113'], *k: &M [1792855650.4779956, 1792855650.4779956]}], &N exchange: &O []}, {*n: R20, *E: &J Kendre
        Miller, *o: *F, *A: *B, *G: &bb {*H: RB, team: *t, *b: *I, quote: [*J, RB, *t], *d: *K}, *L: [{<<: *D, line: 3.5,
          over: -113, under: -113, quote: [*J, '3.5', '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &P Alvin Kamara, *o: *F,
      *A: *B, *G: {*H: RB, team: *t, *b: *I, quote: [*P, RB, *t], *d: *K}, *L: [{<<: *D, line: 12.5, over: -113, under: -113,
          quote: [*P, '12.5', '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &Q Noah Fant, *o: *F, *A: *B, *G: {*H: TE,
        team: *t, *b: *I, quote: [*Q, TE, *t], *d: *K}, *L: [{<<: *D, line: 11.5, over: -113, under: -113, quote: [*Q, '11.5',
            '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &R Chris Olave, *o: *F, *A: *B, *G: {*H: WR, team: *t, *b: *I,
        quote: [*R, WR, *t], *d: *K}, *L: [{<<: *D, line: 74.5, over: -113, under: -113, quote: [*R, '74.5', '-113', '-113'],
          *k: [1792930415.9790742, 1792930415.9790742]}], *N: *O}, {*n: R20, *E: &S Devaughn Vele, *o: *F, *A: *B, *G: {*H: WR,
        team: *t, *b: *I, quote: [*S, WR, *t], *d: *K}, *L: [{<<: *D, line: 41.5, over: -113, under: -113, quote: [*S, '41.5',
            '-113', '-113'], *k: [1792933446.116215, 1792933446.116215]}], *N: *O}, {*n: R20, *E: &T Germie Bernard, *o: *F,
      *A: *B, *G: {*H: WR, team: *s, *b: *I, quote: [*T, WR, *s], *d: *K}, *L: [{<<: *D, line: 53.5, over: -113, under: -113,
          quote: [*T, '53.5', '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &U Rico Dowdle, *o: *F, *A: *B, *G: &W {*H: RB,
        team: *s, *b: *I, quote: [*U, RB, *s], *d: *K}, *L: [{<<: *D, line: 7.5, over: -113, under: -113, quote: [*U, '7.5',
            '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &V DK Metcalf, *o: *F, *A: *B, *G: {*H: WR, team: *s, *b: *I,
        quote: [*V, WR, *s], *d: *K}, *L: [{<<: *D, line: 58.5, over: -113, under: -113, quote: [*V, '58.5', '-113', '-113'],
          *k: *M}], *N: *O}, {*n: R20, *E: *U, *o: &Y rushing_attempts, *A: *B, *G: *W, *L: [{<<: *X, line: 7.5, over: 112,
          under: -142, quote: [*U, '7.5', '112', '-142'], *k: [1792934761.47671, 1792934761.4766972]}], *N: *O}, {*n: R20,
      *E: &Z Jaylen Warren, *o: *Y, *A: *B, *G: {*H: RB, team: *s, *b: *I, quote: [*Z, RB, *s], *d: *K}, *L: [{<<: *ba, line: 14.5,
          over: -118, under: -112, quote: [*Z, '14.5', '-118', '-112'], *k: [1792933868.976788, 1792933868.976788]}], *N: *O},
    {*n: R20, *E: *J, *o: *Y, *A: *B, *G: *bb, *L: [{<<: *X, line: 11.5, over: -104, under: -123, quote: [*J, '11.5', '-104',
            '-123'], *k: [1792934244.232103, 1792934244.232103]}], *N: *O}]}
```

```yaml
{&A game_id: &B IND@MIN 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&t Indianapolis Colts, &s Minnesota Vikings, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:30:58-04:00'},
  quote_defaults: [{<<: &D {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &U {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &X {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i Indianapolis Colts +6.5, line: 6.5, odds: -104, &k odds_ts: 1792905842.680253, quote: [
            *i, '-104']}, {*j: &l Minnesota Vikings -6.5, line: -6.5, odds: -115, *k: 1792905842.680253, quote: &w [*l, '-115']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Under 41.5, line: 41.5, odds: -110, *k: 1792855665.1066895, quote: &y [
            *q, '-110']}, {*j: &r Over 41.5, line: 41.5, odds: -110, *k: 1792855665.1066895, quote: &z [*r, '-110']}]}, {
      <<: *m, *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: -335, *k: 1792931132.7943106, quote: [*s, '-335']},
        {*j: *t, line: *u, odds: 270, *k: 1792931132.7943106, quote: [*t, '270']}]}, {<<: &x {book: *v, *f: *g, *b: *c, *d: *e},
      *n: R17, *o: point_spread, *p: [{*j: *l, line: -6.5, odds: -115, *k: 1792907482.181877, quote: *w}, {*j: *i, line: 6.5,
          odds: -105, *k: 1792907482.181877, quote: [*i, '-105']}]}, {<<: *x, *n: R17, *o: total_points, *p: [{*j: *q, line: 41.5,
          odds: -110, *k: 1792895594.1600578, quote: *y}, {*j: *r, line: 41.5, odds: -110, *k: 1792895594.1600578, quote: *z}]},
    {<<: *x, *n: R17, *o: moneyline, *p: [{*j: *t, line: *u, odds: 260, *k: 1792932091.5682993, quote: [*t, '260']}, {*j: *s,
          line: *u, odds: -325, *k: 1792932091.5682993, quote: [*s, '-325']}]}], props: [{*n: R20, &E player: &C Keenan Allen,
      *o: &F receiving_yards, *A: *B, &G identity: {&H position: WR, team: *t, *b: &I 'https://api.opticodds.com/api/v3/players',
        quote: [*C, WR, *t], *d: &K '2026-10-25T09:36:54-04:00'}, &L quotes: [{<<: *D, line: 40.5, over: -113, under: -113,
          quote: [*C, '40.5', '-113', '-113'], *k: &M [1792861293.2914512, 1792861293.2914512]}], &N exchange: &O []}, {*n: R20,
      *E: &J Jonathan Taylor, *o: *F, *A: *B, *G: &T {*H: RB, team: *t, *b: *I, quote: [*J, RB, *t], *d: *K}, *L: [{<<: *D,
          line: 17.5, over: -113, under: -113, quote: [*J, '17.5', '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &P Justin
        Jefferson, *o: *F, *A: *B, *G: {*H: WR, team: *s, *b: *I, quote: [*P, WR, *s], *d: *K}, *L: [{<<: *D, line: 72.5,
          over: -113, under: -113, quote: [*P, '72.5', '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &Q Will Mallory,
      *o: *F, *A: *B, *G: {*H: TE, team: *t, *b: *I, quote: [*Q, TE, *t], *d: *K}, *L: [{<<: *D, line: 20.5, over: -113, under: -113,
          quote: [*Q, '20.5', '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &R Aaron Jones, *o: *F, *A: *B, *G: &Y {*H: RB,
        team: *s, *b: *I, quote: [*R, RB, *s], *d: *K}, *L: [{<<: *D, line: 14.5, over: -113, under: -113, quote: [*R, '14.5',
            '-113', '-113'], *k: *M}], *N: *O}, {*n: R20, *E: &S Josh Downs, *o: *F, *A: *B, *G: {*H: WR, team: *t, *b: *I,
        quote: [*S, WR, *t], *d: *K}, *L: [{<<: *D, line: 49.5, over: -113, under: -113, quote: [*S, '49.5', '-113', '-113'],
          *k: *M}], *N: *O}, {*n: R20, *E: *J, *o: &V rushing_attempts, *A: *B, *G: *T, *L: [{<<: *U, line: 17.5, over: -105,
          under: -125, quote: [*J, '17.5', '-105', '-125'], *k: &Z [1792930738.659754, 1792930738.659754]}], *N: *O}, {*n: R20,
      *E: &W Jordan Mason, *o: *V, *A: *B, *G: {*H: RB, team: *s, *b: *I, quote: [*W, RB, *s], *d: *K}, *L: [{<<: *X, line: 12.5,
          over: 105, under: -137, quote: [*W, '12.5', '105', '-137'], *k: [1792905103.8969183, 1792905103.8969183]}], *N: *O},
    {*n: R20, *E: *R, *o: *V, *A: *B, *G: *Y, *L: [{<<: *U, line: 9.5, over: -135, under: 100, quote: [*R, '9.5', '-135',
            '100'], *k: *Z}], *N: *O}]}
```

```yaml
{&v game_id: &w CLE@TEN 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&r Cleveland Browns, &q Tennessee Titans, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:30:58-04:00'},
  quote_defaults: [{<<: &y {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &S {book: &t DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &Q {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i Cleveland Browns -1.5, line: -1.5, odds: -118, &k odds_ts: 1792852305.634581, quote: [
            *i, '-118']}, {*j: &l Tennessee Titans +1.5, line: 1.5, odds: -104, *k: 1792852305.634581, quote: [*l, '-104']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: Under 37.5, line: 37.5, odds: -115, *k: 1792852305.634581, quote: [Under
              37.5, '-115']}, {*j: Over 37.5, line: 37.5, odds: -105, *k: 1792852305.634581, quote: [Over 37.5, '-105']}]},
    {<<: *m, *n: R17, *o: moneyline, *p: [{*j: *q, line: &s UNKNOWN, odds: 114, *k: 1792930824.7214367, quote: [*q, '114']},
        {*j: *r, line: *s, odds: -134, *k: 1792930824.7214367, quote: [*r, '-134']}]}, {<<: &u {book: *t, *f: *g, *b: *c,
        *d: *e}, *n: R17, *o: point_spread, *p: [{*j: *i, line: -1.5, odds: -110, *k: 1792908488.6662385, quote: [*i, '-110']},
        {*j: *l, line: 1.5, odds: -110, *k: 1792908488.6662385, quote: [*l, '-110']}]}, {<<: *u, *n: R17, *o: total_points,
      *p: [{*j: Over 36.5, line: 36.5, odds: -118, *k: 1792895594.1600578, quote: [Over 36.5, '-118']}, {*j: Under 36.5, line: 36.5,
          odds: -102, *k: 1792895594.1600578, quote: [Under 36.5, '-102']}]}, {<<: *u, *n: R17, *o: moneyline, *p: [{*j: *q,
          line: *s, odds: 110, *k: 1792895594.1600578, quote: [*q, '110']}, {*j: *r, line: *s, odds: -130, *k: 1792895594.1600578,
          quote: [*r, '-130']}]}], weather: {*n: R19, *b: 'https://api.open-meteo.com/v1/forecast?latitude=36.1665&longitude=-86.7713&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&start_date=2026-10-25&end_date=2026-10-25',
    *d: '2026-10-25T09:31:51-04:00', exact_kickoff_forecast: hourly sample at kickoff, hourly_samples: [{time_et: '2026-10-25T13:00-04:00',
        temp_f: 70.9, wind_mph: 4, gust_mph: 5.1, precip_probability_pct: 0, quote: ['2026-10-25T13:00', '70.9', '4', '5.1',
          '0']}]}, props: [{*n: R20, &z player: &x Denzel Boston, *o: &A receiving_yards, *v: *w, &B identity: {&C position: WR,
        team: *r, *b: &D 'https://api.opticodds.com/api/v3/players', quote: [*x, WR, *r], *d: &F '2026-10-25T09:36:54-04:00'},
      &G quotes: [{<<: *y, line: 51.5, over: -113, under: -113, quote: [*x, '51.5', '-113', '-113'], *k: &H [1792861284.8607311,
            1792861284.8607311]}], &I exchange: &J []}, {*n: R20, *z: &E Carnell Tate, *o: *A, *v: *w, *B: {*C: WR, team: *q,
        *b: *D, quote: [*E, WR, *q], *d: *F}, *G: [{<<: *y, line: 52.5, over: -113, under: -113, quote: [*E, '52.5', '-113',
            '-113'], *k: *H}], *I: *J}, {*n: R20, *z: &K Tyjae Spears, *o: *A, *v: *w, *B: {*C: RB, team: *q, *b: *D, quote: [
          *K, RB, *q], *d: *F}, *G: [{<<: *y, line: 11.5, over: -113, under: -113, quote: [*K, '11.5', '-113', '-113'], *k: *H}],
      *I: *J}, {*n: R20, *z: &L Tony Pollard, *o: *A, *v: *w, *B: &P {*C: RB, team: *q, *b: *D, quote: [*L, RB, *q], *d: *F},
      *G: [{<<: *y, line: 6.5, over: -113, under: -113, quote: [*L, '6.5', '-113', '-113'], *k: *H}], *I: *J}, {*n: R20, *z: &M Quinshon
        Judkins, *o: *A, *v: *w, *B: &R {*C: RB, team: *r, *b: *D, quote: [*M, RB, *r], *d: *F}, *G: [{<<: *y, line: 10.5,
          over: -113, under: -113, quote: [*M, '10.5', '-113', '-113'], *k: [1792861644.852841, 1792861644.852841]}], *I: *J},
    {*n: R20, *z: &N Dylan Sampson, *o: *A, *v: *w, *B: {*C: RB, team: *r, *b: *D, quote: [*N, RB, *r], *d: *F}, *G: [{<<: *y,
          line: 10.5, over: -113, under: -113, quote: [*N, '10.5', '-113', '-113'], *k: [1792877274.2915215, 1792877274.2915215]}],
      *I: *J}, {*n: R20, *z: &O Gunnar Helm, *o: *A, *v: *w, *B: {*C: TE, team: *q, *b: *D, quote: [*O, TE, *q], *d: *F},
      *G: [{<<: *y, line: 13.5, over: -113, under: -113, quote: [*O, '13.5', '-113', '-113'], *k: *H}], *I: *J}, {*n: R20,
      *z: *L, *o: rushing_attempts, *v: *w, *B: *P, *G: [{<<: *Q, line: 17.5, over: 107, under: -141, quote: [*L, '17.5',
            '107', '-141'], *k: [1792930847.913627, 1792930847.913627]}], *I: *J}, {*n: R20, *z: *M, *o: rushing_attempts,
      *v: *w, *B: *R, *G: [{<<: *S, line: 14.5, over: -102, under: -126, quote: [*M, '14.5', '-102', '-126'], *k: [1792895594.1600578,
            1792895594.1600578]}], *I: *J}]}
```

```yaml
{&z game_id: &A MIA@NYJ 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&s Miami Dolphins, &t New York Jets, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:30:58-04:00'},
  quote_defaults: [{<<: &C {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &T {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: Caesars, *f: *g,
        *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i New York Jets -3.5, line: -3.5, odds: -115, &k odds_ts: 1792922403.1036687, quote: &w [
            *i, '-115']}, {*j: &l Miami Dolphins +3.5, line: 3.5, odds: -105, *k: 1792922403.1036687, quote: &x [*l, '-105']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Over 39.5, line: 39.5, odds: -105, *k: 1792855665.1066895, quote: [*q,
            '-105']}, {*j: &r Under 39.5, line: 39.5, odds: -115, *k: 1792855665.1066895, quote: [*r, '-115']}]}, {<<: *m,
      *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: 168, *k: 1792931465.0127232, quote: [*s, '168']}, {*j: *t,
          line: *u, odds: -200, *k: 1792931465.0127232, quote: [*t, '-200']}]}, {<<: &y {book: *v, *f: *g, *b: *c, *d: *e},
      *n: R17, *o: point_spread, *p: [{*j: *i, line: -3.5, odds: -115, *k: 1792931489.0291967, quote: *w}, {*j: *l, line: 3.5,
          odds: -105, *k: 1792931489.0291967, quote: *x}]}, {<<: *y, *n: R17, *o: total_points, *p: [{*j: *r, line: 39.5,
          odds: -118, *k: 1792929887.2948306, quote: [*r, '-118']}, {*j: *q, line: 39.5, odds: -102, *k: 1792929887.2948306,
          quote: [*q, '-102']}]}, {<<: *y, *n: R17, *o: moneyline, *p: [{*j: *t, line: *u, odds: -218, *k: 1792928473.4284406,
          quote: [*t, '-218']}, {*j: *s, line: *u, odds: 180, *k: 1792928473.4284406, quote: [*s, '180']}]}], weather: {*n: R19,
    *b: 'https://api.open-meteo.com/v1/forecast?latitude=40.8135&longitude=-74.0745&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&start_date=2026-10-25&end_date=2026-10-25',
    *d: '2026-10-25T09:31:51-04:00', exact_kickoff_forecast: hourly sample at kickoff, hourly_samples: [{time_et: '2026-10-25T13:00-04:00',
        temp_f: 64.2, wind_mph: 3, gust_mph: 5.8, precip_probability_pct: 0, quote: ['2026-10-25T13:00', '64.2', '3', '5.8',
          '0']}]}, props: [{*n: R20, &D player: &B Mason Taylor, *o: &E receiving_yards, *z: *A, &F identity: {&G position: TE,
        team: *t, *b: &H 'https://api.opticodds.com/api/v3/players', quote: [*B, TE, *t], *d: &J '2026-10-25T09:36:54-04:00'},
      &K quotes: [{<<: *C, line: 17.5, over: -113, under: -113, quote: [*B, '17.5', '-113', '-113'], *k: [1792865372.886057,
            1792865372.886057]}], &L exchange: &M []}, {*n: R20, *D: &I Malik Washington, *o: *E, *z: *A, *F: {*G: WR, team: *s,
        *b: *H, quote: [*I, WR, *s], *d: *J}, *K: [{<<: *C, line: 40.5, over: -113, under: -113, quote: [*I, '40.5', '-113',
            '-113'], *k: &O [1792861293.2914512, 1792861293.2914512]}], *L: *M}, {*n: R20, *D: &N Ollie Gordon II, *o: *E,
      *z: *A, *F: &S {*G: RB, team: *s, *b: *H, quote: [*N, RB, *s], *d: *J}, *K: [{<<: *C, line: 8.5, over: -113, under: -113,
          quote: [*N, '8.5', '-113', '-113'], *k: *O}], *L: *M}, {*n: R20, *D: &P Greg Dulcich, *o: *E, *z: *A, *F: {*G: TE,
        team: *s, *b: *H, quote: [*P, TE, *s], *d: *J}, *K: [{<<: *C, line: 21.5, over: -113, under: -113, quote: [*P, '21.5',
            '-113', '-113'], *k: *O}], *L: *M}, {*n: R20, *D: &Q Garrett Wilson, *o: *E, *z: *A, *F: {*G: WR, team: *t, *b: *H,
        quote: [*Q, WR, *t], *d: *J}, *K: [{<<: *C, line: 62.5, over: -113, under: -113, quote: [*Q, '62.5', '-113', '-113'],
          *k: *O}], *L: *M}, {*n: R20, *D: &R Kenyon Sadiq, *o: *E, *z: *A, *F: {*G: TE, team: *t, *b: *H, quote: [*R, TE,
          *t], *d: *J}, *K: [{<<: *C, line: 18.5, over: -113, under: -113, quote: [*R, '18.5', '-113', '-113'], *k: *O}],
      *L: *M}, {*n: R20, *D: *N, *o: rushing_attempts, *z: *A, *F: *S, *K: [{<<: *T, line: 13.5, over: -134, under: 105, quote: [
            *N, '13.5', '-134', '105'], *k: [1792933421.1350365, 1792933421.1350365]}], *L: *M}]}
```

```yaml
{&x game_id: &y TB@CAR 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&q Tampa Bay Buccaneers, &r Carolina Panthers, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:30:58-04:00'},
  quote_defaults: [{<<: &A {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: {book: &t DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &R {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &U {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &k {book: *h, *f: *g, *b: *c, *d: *e}, &l req_id: R17, &m market: point_spread,
      &n observations: [{&i selection: Tampa Bay Buccaneers +2.5, line: 2.5, odds: 104, &j odds_ts: 1792852305.634581, quote: [
            Tampa Bay Buccaneers +2.5, '104']}, {*i: Carolina Panthers -2.5, line: -2.5, odds: -122, *j: 1792852305.634581,
          quote: [Carolina Panthers -2.5, '-122']}]}, {<<: *k, *l: R17, *m: total_points, *n: [{*i: &o Under 44.5, line: 44.5,
          odds: -110, *j: 1792852305.634581, quote: &w [*o, '-110']}, {*i: &p Over 44.5, line: 44.5, odds: -110, *j: 1792852305.634581,
          quote: &v [*p, '-110']}]}, {<<: *k, *l: R17, *m: moneyline, *n: [{*i: *q, line: &s UNKNOWN, odds: 134, *j: 1792852305.634581,
          quote: [*q, '134']}, {*i: *r, line: *s, odds: -158, *j: 1792852305.634581, quote: [*r, '-158']}]}, {<<: &u {book: *t,
        *f: *g, *b: *c, *d: *e}, *l: R17, *m: point_spread, *n: [{*i: Carolina Panthers -3, line: -3, odds: -102, *j: 1792895577.4487615,
          quote: [Carolina Panthers -3, '-102']}, {*i: Tampa Bay Buccaneers +3, line: 3, odds: -118, *j: 1792895577.4487615,
          quote: [Tampa Bay Buccaneers +3, '-118']}]}, {<<: *u, *l: R17, *m: total_points, *n: [{*i: *p, line: 44.5, odds: -110,
          *j: 1792930028.5617445, quote: *v}, {*i: *o, line: 44.5, odds: -110, *j: 1792930028.5617445, quote: *w}]}, {<<: *u,
      *l: R17, *m: moneyline, *n: [{*i: *q, line: *s, odds: 136, *j: 1792931030.8968313, quote: [*q, '136']}, {*i: *r, line: *s,
          odds: -162, *j: 1792931030.8968313, quote: [*r, '-162']}]}], weather: {*l: R19, *b: 'https://api.open-meteo.com/v1/forecast?latitude=35.2258&longitude=-80.8528&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&start_date=2026-10-25&end_date=2026-10-25',
    *d: '2026-10-25T09:31:51-04:00', exact_kickoff_forecast: hourly sample at kickoff, hourly_samples: [{time_et: '2026-10-25T13:00-04:00',
        temp_f: 64.6, wind_mph: 11.2, gust_mph: 15.9, precip_probability_pct: 0, quote: ['2026-10-25T13:00', '64.6', '11.2',
          '15.9', '0']}]}, props: [{*l: R20, &B player: &z Jalen Coker, *m: &C receiving_yards, *x: *y, &D identity: {&E position: WR,
        team: *r, *b: &F 'https://api.opticodds.com/api/v3/players', quote: [*z, WR, *r], *d: &H '2026-10-25T09:36:54-04:00'},
      &I quotes: [{<<: *A, line: 66.5, over: -113, under: -113, quote: [*z, '66.5', '-113', '-113'], *j: &J [1792861284.8607311,
            1792861284.8607311]}], &K exchange: &L []}, {*l: R20, *B: &G Chris Godwin, *m: *C, *x: *y, *D: {*E: WR, team: *q,
        *b: *F, quote: [*G, WR, *q], *d: *H}, *I: [{<<: *A, line: 44.5, over: -113, under: -113, quote: [*G, '44.5', '-113',
            '-113'], *j: *J}], *K: *L}, {*l: R20, *B: &M Kenneth Gainwell, *m: *C, *x: *y, *D: {*E: RB, team: *q, *b: *F,
        quote: [*M, RB, *q], *d: *H}, *I: [{<<: *A, line: 11.5, over: -113, under: -113, quote: [*M, '11.5', '-113', '-113'],
          *j: *J}], *K: *L}, {*l: R20, *B: &N Darren Waller, *m: *C, *x: *y, *D: {*E: TE, team: *r, *b: *F, quote: [*N, TE,
          *r], *d: *H}, *I: [{<<: *A, line: 22.5, over: -113, under: -113, quote: [*N, '22.5', '-113', '-113'], *j: *J}],
      *K: *L}, {*l: R20, *B: &O Tetairoa McMillan, *m: *C, *x: *y, *D: {*E: WR, team: *r, *b: *F, quote: [*O, WR, *r], *d: *H},
      *I: [{<<: *A, line: 69.5, over: -113, under: -113, quote: [*O, '69.5', '-113', '-113'], *j: *J}], *K: *L}, {*l: R20,
      *B: &P Tommy Tremble, *m: *C, *x: *y, *D: {*E: TE, team: *r, *b: *F, quote: [*P, TE, *r], *d: *H}, *I: [{<<: *A, line: 16.5,
          over: -113, under: -113, quote: [*P, '16.5', '-113', '-113'], *j: *J}], *K: *L}, {*l: R20, *B: &Q Chuba Hubbard,
      *m: &S rushing_attempts, *x: *y, *D: {*E: RB, team: *r, *b: *F, quote: [*Q, RB, *r], *d: *H}, *I: [{<<: *R, line: 17.5,
          over: -120, under: -110, quote: [*Q, '17.5', '-120', '-110'], *j: [1792930745.4509525, 1792930745.4509525]}], *K: *L},
    {*l: R20, *B: &T AJ Dillon, *m: *S, *x: *y, *D: {*E: RB, team: *r, *b: *F, quote: [*T, RB, *r], *d: *H}, *I: [{<<: *U,
          line: 3.5, over: 100, under: -132, quote: [*T, '3.5', '100', '-132'], *j: [1792925807.885554, 1792925807.885554]}],
      *K: *L}, {*l: R20, *B: &V Bucky Irving, *m: *S, *x: *y, *D: {*E: RB, team: *q, *b: *F, quote: [*V, RB, *q], *d: *H},
      *I: [{<<: *U, line: 15.5, over: -106, under: -125, quote: [*V, '15.5', '-106', '-125'], *j: [1792859097.8663704, 1792859097.8663704]}],
      *K: *L}]}
```

```yaml
{&y game_id: &z SF@ATL 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&t San Francisco 49ers, &s Atlanta Falcons, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:31:16-04:00'},
  quote_defaults: [{<<: &B {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &N {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i San Francisco 49ers -2.5, line: -2.5, odds: -118, &k odds_ts: 1792852305.634581,
          quote: [*i, '-118']}, {*j: &l Atlanta Falcons +2.5, line: 2.5, odds: -104, *k: 1792852305.634581, quote: [*l, '-104']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Over 50.5, line: 50.5, odds: -110, *k: 1792886004.303302, quote: [*q,
            '-110']}, {*j: &r Under 50.5, line: 50.5, odds: -110, *k: 1792886004.303302, quote: [*r, '-110']}]}, {<<: *m,
      *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: 124, *k: 1792886004.303302, quote: &x [*s, '124']}, {
          *j: *t, line: *u, odds: -146, *k: 1792886004.303302, quote: [*t, '-146']}]}, {<<: &w {book: *v, *f: *g, *b: *c,
        *d: *e}, *n: R17, *o: point_spread, *p: [{*j: *l, line: 2.5, odds: -105, *k: 1792895586.066018, quote: [*l, '-105']},
        {*j: *i, line: -2.5, odds: -115, *k: 1792895586.066018, quote: [*i, '-115']}]}, {<<: *w, *n: R17, *o: total_points,
      *p: [{*j: *q, line: 50.5, odds: -105, *k: 1792930251.154262, quote: [*q, '-105']}, {*j: *r, line: 50.5, odds: -115,
          *k: 1792930251.154262, quote: [*r, '-115']}]}, {<<: *w, *n: R17, *o: moneyline, *p: [{*j: *t, line: *u, odds: -148,
          *k: 1792933225.4802923, quote: [*t, '-148']}, {*j: *s, line: *u, odds: 124, *k: 1792933225.4802923, quote: *x}]}],
  props: [{*n: R20, &C player: &A Drake London, *o: receiving_yards, *y: *z, &D identity: {&E position: WR, team: *s, *b: &F 'https://api.opticodds.com/api/v3/players',
        quote: [*A, WR, *s], *d: &H '2026-10-25T09:36:54-04:00'}, &I quotes: [{<<: *B, line: 83.5, over: -113, under: -113,
          quote: [*A, '83.5', '-113', '-113'], *k: &J [1792861284.8607311, 1792861284.8607311]}], &K exchange: &L []}, {*n: R20,
      *C: &G Austin Hooper, *o: receiving_yards, *y: *z, *D: {*E: TE, team: *s, *b: *F, quote: [*G, TE, *s], *d: *H}, *I: [
        {<<: *B, line: 3.5, over: -113, under: -113, quote: [*G, '3.5', '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *C: &M Bijan
        Robinson, *o: rushing_attempts, *y: *z, *D: {*E: RB, team: *s, *b: *F, quote: [*M, RB, *s], *d: *H}, *I: [{<<: *N,
          line: 19.5, over: -108, under: -122, quote: [*M, '19.5', '-108', '-122'], *k: [1792933608.065135, 1792933608.065135]}],
      *K: *L}, {*n: R20, *C: &O Christian McCaffrey, *o: rushing_attempts, *y: *z, *D: {*E: RB, team: *t, *b: *F, quote: [
          *O, RB, *t], *d: *H}, *I: [{<<: *N, line: 14.5, over: -102, under: -128, quote: [*O, '14.5', '-102', '-128'], *k: [
            1792881497.7167997, 1792881497.7167997]}], *K: *L}]}
```

```yaml
{&v game_id: &w CIN@BAL 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&r Cincinnati Bengals, &q Baltimore Ravens, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:31:16-04:00'},
  quote_defaults: [{<<: &y {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &X {book: &t DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &S {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &V {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &k {book: *h, *f: *g, *b: *c, *d: *e}, &l req_id: R17, &m market: point_spread,
      &n observations: [{&i selection: Baltimore Ravens +2.5, line: 2.5, odds: 100, &j odds_ts: 1792931315.4134054, quote: [
            Baltimore Ravens +2.5, '100']}, {*i: Cincinnati Bengals -2.5, line: -2.5, odds: -120, *j: 1792892852.9996023,
          quote: [Cincinnati Bengals -2.5, '-120']}]}, {<<: *k, *l: R17, *m: total_points, *n: [{*i: &o Over 46.5, line: 46.5,
          odds: -110, *j: 1792880403.0562692, quote: [*o, '-110']}, {*i: &p Under 46.5, line: 46.5, odds: -110, *j: 1792880403.0562692,
          quote: [*p, '-110']}]}, {<<: *k, *l: R17, *m: moneyline, *n: [{*i: *q, line: &s UNKNOWN, odds: 130, *j: 1792931073.1931906,
          quote: [*q, '130']}, {*i: *r, line: *s, odds: -154, *j: 1792931073.1931906, quote: [*r, '-154']}]}, {<<: &u {book: *t,
        *f: *g, *b: *c, *d: *e}, *l: R17, *m: point_spread, *n: [{*i: Cincinnati Bengals -3, line: -3, odds: -105, *j: 1792906341.6432176,
          quote: [Cincinnati Bengals -3, '-105']}, {*i: Baltimore Ravens +3, line: 3, odds: -115, *j: 1792906341.6432176,
          quote: [Baltimore Ravens +3, '-115']}]}, {<<: *u, *l: R17, *m: total_points, *n: [{*i: *o, line: 46.5, odds: -105,
          *j: 1792895586.066018, quote: [*o, '-105']}, {*i: *p, line: 46.5, odds: -115, *j: 1792895586.066018, quote: [*p,
            '-115']}]}, {<<: *u, *l: R17, *m: moneyline, *n: [{*i: *r, line: *s, odds: -148, *j: 1792906341.6432176, quote: [
            *r, '-148']}, {*i: *q, line: *s, odds: 124, *j: 1792906341.6432176, quote: [*q, '124']}]}], weather: {*l: R19,
    *b: 'https://api.open-meteo.com/v1/forecast?latitude=39.278&longitude=-76.6227&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&start_date=2026-10-25&end_date=2026-10-25',
    *d: '2026-10-25T09:31:51-04:00', exact_kickoff_forecast: hourly sample at kickoff, hourly_samples: [{time_et: '2026-10-25T13:00-04:00',
        temp_f: 62.3, wind_mph: 2.7, gust_mph: 6.9, precip_probability_pct: 0, quote: ['2026-10-25T13:00', '62.3', '2.7',
          '6.9', '0']}]}, props: [{*l: R20, &z player: &x Justice Hill, *m: &A receiving_yards, *v: *w, &B identity: {&C position: RB,
        team: *q, *b: &D 'https://api.opticodds.com/api/v3/players', quote: [*x, RB, *q], *d: &F '2026-10-25T09:36:54-04:00'},
      &G quotes: [{<<: *y, line: 9.5, over: -113, under: -113, quote: [*x, '9.5', '-113', '-113'], *j: [1792872542.8659425,
            1792872542.8659425]}], &H exchange: &I []}, {*l: R20, *z: &E Zay Flowers, *m: *A, *v: *w, *B: {*C: WR, team: *q,
        *b: *D, quote: [*E, WR, *q], *d: *F}, *G: [{<<: *y, line: 63.5, over: -113, under: -113, quote: [*E, '63.5', '-113',
            '-113'], *j: [1792873772.6829324, 1792873772.6829324]}], *H: *I}, {*l: R20, *z: &J Ja'Marr Chase, *m: *A, *v: *w,
      *B: {*C: WR, team: *r, *b: *D, quote: [*J, WR, *r], *d: *F}, *G: [{<<: *y, line: 80.5, over: -113, under: -113, quote: [
            *J, '80.5', '-113', '-113'], *j: &L [1792861293.2914512, 1792861293.2914512]}], *H: *I}, {*l: R20, *z: &K Tee
        Higgins, *m: *A, *v: *w, *B: {*C: WR, team: *r, *b: *D, quote: [*K, WR, *r], *d: *F}, *G: [{<<: *y, line: 65.5, over: -113,
          under: -113, quote: [*K, '65.5', '-113', '-113'], *j: *L}], *H: *I}, {*l: R20, *z: &M Chase Brown, *m: *A, *v: *w,
      *B: &U {*C: RB, team: *r, *b: *D, quote: [*M, RB, *r], *d: *F}, *G: [{<<: *y, line: 19.5, over: -113, under: -113, quote: [
            *M, '19.5', '-113', '-113'], *j: *L}], *H: *I}, {*l: R20, *z: &N Josh Cuevas, *m: *A, *v: *w, *B: {*C: TE, team: *q,
        *b: *D, quote: [*N, TE, *q], *d: *F}, *G: [{<<: *y, line: 5.5, over: -113, under: -113, quote: [*N, '5.5', '-113',
            '-113'], *j: [1792934464.8864892, 1792934464.8864892]}], *H: *I}, {*l: R20, *z: &O Mike Gesicki, *m: *A, *v: *w,
      *B: {*C: TE, team: *r, *b: *D, quote: [*O, TE, *r], *d: *F}, *G: [{<<: *y, line: 22.5, over: -113, under: -113, quote: [
            *O, '22.5', '-113', '-113'], *j: *L}], *H: *I}, {*l: R20, *z: &P Derrick Henry, *m: *A, *v: *w, *B: &R {*C: RB,
        team: *q, *b: *D, quote: [*P, RB, *q], *d: *F}, *G: [{<<: *y, line: 6.5, over: -113, under: -113, quote: [*P, '6.5',
            '-113', '-113'], *j: [1792871312.5944772, 1792871312.5944772]}], *H: *I}, {*l: R20, *z: &Q Samaje Perine, *m: *A,
      *v: *w, *B: &W {*C: RB, team: *r, *b: *D, quote: [*Q, RB, *r], *d: *F}, *G: [{<<: *y, line: 7.5, over: -113, under: -113,
          quote: [*Q, '7.5', '-113', '-113'], *j: *L}], *H: *I}, {*l: R20, *z: *P, *m: &T rushing_attempts, *v: *w, *B: *R,
      *G: [{<<: *S, line: 19.5, over: -105, under: -125, quote: [*P, '19.5', '-105', '-125'], *j: [1792930745.4509525, 1792930745.4509525]}],
      *H: *I}, {*l: R20, *z: *M, *m: *T, *v: *w, *B: *U, *G: [{<<: *V, line: 11.5, over: 108, under: -150, quote: [*M, '11.5',
            '108', '-150'], *j: [1792875073.8901284, 1792875073.8901284]}], *H: *I}, {*l: R20, *z: *Q, *m: *T, *v: *w, *B: *W,
      *G: [{<<: *X, line: 7.5, over: -132, under: 103, quote: [*Q, '7.5', '-132', '103'], *j: [1792895586.066018, 1792895586.066018]}],
      *H: *I}]}
```

```yaml
{&x game_id: &y NYG@HOU 2026-10-25, start_et: '2026-10-25T13:00:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&s New York Giants, &t Houston Texans, '2026-10-25T17:00:00Z'], &d retrieved_at: &e '2026-10-25T09:31:16-04:00'},
  quote_defaults: [{<<: &A {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &R {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: Caesars, *f: *g,
        *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i New York Giants +10.5, line: 10.5, odds: -118, &k odds_ts: 1792855665.1066895, quote: [
            *i, '-118']}, {*j: &l Houston Texans -10.5, line: -10.5, odds: -104, *k: 1792855665.1066895, quote: [*l, '-104']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Under 42.5, line: 42.5, odds: -104, *k: 1792855665.1066895, quote: [
            *q, '-104']}, {*j: &r Over 42.5, line: 42.5, odds: -118, *k: 1792855665.1066895, quote: [*r, '-118']}]}, {<<: *m,
      *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: 385, *k: 1792855665.1066895, quote: [*s, '385']}, {*j: *t,
          line: *u, odds: -500, *k: 1792855665.1066895, quote: [*t, '-500']}]}, {<<: &w {book: *v, *f: *g, *b: *c, *d: *e},
      *n: R17, *o: point_spread, *p: [{*j: *l, line: -10.5, odds: -108, *k: 1792934594.8070965, quote: [*l, '-108']}, {*j: *i,
          line: 10.5, odds: -112, *k: 1792934594.8070965, quote: [*i, '-112']}]}, {<<: *w, *n: R17, *o: total_points, *p: [
        {*j: *r, line: 42.5, odds: -112, *k: 1792895577.4487615, quote: [*r, '-112']}, {*j: *q, line: 42.5, odds: -108, *k: 1792895577.4487615,
          quote: [*q, '-108']}]}, {<<: *w, *n: R17, *o: moneyline, *p: [{*j: *s, line: *u, odds: 400, *k: 1792934594.8070965,
          quote: [*s, '400']}, {*j: *t, line: *u, odds: -535, *k: 1792934594.8070965, quote: [*t, '-535']}]}], props: [{*n: R20,
      &B player: &z Tyrone Tracy Jr., *o: &C receiving_yards, *x: *y, &D identity: {&E position: RB, team: *s, *b: &F 'https://api.opticodds.com/api/v3/players',
        quote: [*z, RB, *s], *d: &H '2026-10-25T09:36:54-04:00'}, &I quotes: [{<<: *A, line: 9.5, over: -113, under: -113,
          quote: [*z, '9.5', '-113', '-113'], *k: &J [1792861293.2914512, 1792861293.2914512]}], &K exchange: &L []}, {*n: R20,
      *B: &G Malik Nabers, *o: *C, *x: *y, *D: {*E: WR, team: *s, *b: *F, quote: [*G, WR, *s], *d: *H}, *I: [{<<: *A, line: 68.5,
          over: -113, under: -113, quote: [*G, '68.5', '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &M Nico Collins,
      *o: *C, *x: *y, *D: {*E: WR, team: *t, *b: *F, quote: [*M, WR, *t], *d: *H}, *I: [{<<: *A, line: 68.5, over: -113, under: -113,
          quote: [*M, '68.5', '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &N Woody Marks, *o: *C, *x: *y, *D: &Q {*E: RB,
        team: *t, *b: *F, quote: [*N, RB, *t], *d: *H}, *I: [{<<: *A, line: 14.5, over: -113, under: -113, quote: [*N, '14.5',
            '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &O Foster Moreau, *o: *C, *x: *y, *D: {*E: TE, team: *t, *b: *F,
        quote: [*O, TE, *t], *d: *H}, *I: [{<<: *A, line: 8.5, over: -113, under: -113, quote: [*O, '8.5', '-113', '-113'],
          *k: *J}], *K: *L}, {*n: R20, *B: &P Devin Singletary, *o: *C, *x: *y, *D: {*E: RB, team: *s, *b: *F, quote: [*P,
          RB, *s], *d: *H}, *I: [{<<: *A, line: 7.5, over: -113, under: -113, quote: [*P, '7.5', '-113', '-113'], *k: [1792912382.9643288,
            1792912382.9643288]}], *K: *L}, {*n: R20, *B: *N, *o: rushing_attempts, *x: *y, *D: *Q, *I: [{<<: *R, line: 16.5,
          over: -112, under: -112, quote: [*N, '16.5', '-112', '-112'], *k: [1792927083.5634818, 1792919854.961233]}], *K: *L}]}
```

```yaml
{&v game_id: &w DEN@ARI 2026-10-25, start_et: '2026-10-25T16:05:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&r Denver Broncos, &q Arizona Cardinals, '2026-10-25T20:05:00Z'], &d retrieved_at: &e '2026-10-25T09:31:16-04:00'},
  quote_defaults: [{<<: &y {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &R {book: &t DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &V {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i Arizona Cardinals +4.5, line: 4.5, odds: -112, &k odds_ts: 1792855665.1066895, quote: [
            *i, '-112']}, {*j: &l Denver Broncos -4.5, line: -4.5, odds: -108, *k: 1792855665.1066895, quote: [*l, '-108']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: Under 43.5, line: 43.5, odds: -110, *k: 1792855665.1066895, quote: [Under
              43.5, '-110']}, {*j: Over 43.5, line: 43.5, odds: -110, *k: 1792855665.1066895, quote: [Over 43.5, '-110']}]},
    {<<: *m, *n: R17, *o: moneyline, *p: [{*j: *q, line: &s UNKNOWN, odds: 188, *k: 1792857453.3932922, quote: [*q, '188']},
        {*j: *r, line: *s, odds: -225, *k: 1792857453.3932922, quote: [*r, '-225']}]}, {<<: &u {book: *t, *f: *g, *b: *c,
        *d: *e}, *n: R17, *o: point_spread, *p: [{*j: *i, line: 4.5, odds: -105, *k: 1792930779.0609717, quote: [*i, '-105']},
        {*j: *l, line: -4.5, odds: -115, *k: 1792930779.0609717, quote: [*l, '-115']}]}, {<<: *u, *n: R17, *o: total_points,
      *p: [{*j: Under 42.5, line: 42.5, odds: 100, *k: 1792929816.9842997, quote: [Under 42.5, '100']}, {*j: Over 42.5, line: 42.5,
          odds: -120, *k: 1792929816.9842997, quote: [Over 42.5, '-120']}]}, {<<: *u, *n: R17, *o: moneyline, *p: [{*j: *q,
          line: *s, odds: 195, *k: 1792930793.0182624, quote: [*q, '195']}, {*j: *r, line: *s, odds: -238, *k: 1792930793.0182624,
          quote: [*r, '-238']}]}], props: [{*n: R20, &z player: &x Michael Wilson, *o: &A receiving_yards, *v: *w, &B identity: {
        &C position: WR, team: *q, *b: &D 'https://api.opticodds.com/api/v3/players', quote: [*x, WR, *q], *d: &F '2026-10-25T09:36:54-04:00'},
      &G quotes: [{<<: *y, line: 49.5, over: -113, under: -113, quote: [*x, '49.5', '-113', '-113'], *k: &H [1792872392.9916267,
            1792872392.9916267]}], &I exchange: &J []}, {*n: R20, *z: &E Evan Engram, *o: *A, *v: *w, *B: {*C: TE, team: *r,
        *b: *D, quote: [*E, TE, *r], *d: *F}, *G: [{<<: *y, line: 22.5, over: -113, under: -113, quote: [*E, '22.5', '-113',
            '-113'], *k: *H}], *I: *J}, {*n: R20, *z: &K Jaylen Waddle, *o: *A, *v: *w, *B: {*C: WR, team: *r, *b: *D, quote: [
          *K, WR, *r], *d: *F}, *G: [{<<: *y, line: 50.5, over: -113, under: -113, quote: [*K, '50.5', '-113', '-113'], *k: *H}],
      *I: *J}, {*n: R20, *z: &L J.K. Dobbins, *o: *A, *v: *w, *B: &Q {*C: RB, team: *r, *b: *D, quote: [*L, RB, *r], *d: *F},
      *G: [{<<: *y, line: 4.5, over: -113, under: -113, quote: [*L, '4.5', '-113', '-113'], *k: *H}], *I: *J}, {*n: R20, *z: &M RJ
        Harvey, *o: *A, *v: *w, *B: {*C: RB, team: *r, *b: *D, quote: [*M, RB, *r], *d: *F}, *G: [{<<: *y, line: 24.5, over: -106,
          under: -120, quote: [*M, '24.5', '-106', '-120'], *k: [1792872392.9916267, 1792855665.1066895]}], *I: *J}, {*n: R20,
      *z: &N Elijah Higgins, *o: *A, *v: *w, *B: {*C: TE, team: *q, *b: *D, quote: [*N, TE, *q], *d: *F}, *G: [{<<: *y, line: 12.5,
          over: -113, under: -113, quote: [*N, '12.5', '-113', '-113'], *k: *H}], *I: *J}, {*n: R20, *z: &O Tyler Allgeier,
      *o: *A, *v: *w, *B: &U {*C: RB, team: *q, *b: *D, quote: [*O, RB, *q], *d: *F}, *G: [{<<: *y, line: 9.5, over: -113,
          under: -113, quote: [*O, '9.5', '-113', '-113'], *k: [1792925642.8239572, 1792925642.8239572]}], *I: *J}, {*n: R20,
      *z: &P Adam Trautman, *o: *A, *v: *w, *B: {*C: TE, team: *r, *b: *D, quote: [*P, TE, *r], *d: *F}, *G: [{<<: *y, line: 2.5,
          over: 118, under: -150, quote: [*P, '2.5', '118', '-150'], *k: *H}], *I: *J}, {*n: R20, *z: *L, *o: &S rushing_attempts,
      *v: *w, *B: *Q, *G: [{<<: *R, line: 13.5, over: -114, under: -112, quote: [*L, '13.5', '-114', '-112'], *k: [1792930793.0182624,
            1792930794.5069065]}], *I: *J}, {*n: R20, *z: &T Zonovan Knight, *o: *S, *v: *w, *B: {*C: RB, team: *q, *b: *D,
        quote: [*T, RB, *q], *d: *F}, *G: [{<<: *R, line: 10.5, over: -122, under: -105, quote: [*T, '10.5', '-122', '-105'],
          *k: [1792930793.0182624, 1792930793.0182624]}], *I: *J}, {*n: R20, *z: *O, *o: *S, *v: *w, *B: *U, *G: [{<<: *V,
          line: 9.5, over: 107, under: -141, quote: [*O, '9.5', '107', '-141'], *k: [1792929853.8944142, 1792929853.8944142]}],
      *I: *J}]}
```

```yaml
{&y game_id: &z LAR@LV 2026-10-25, start_et: '2026-10-25T16:25:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&s Los Angeles Rams, &t Las Vegas Raiders, '2026-10-25T20:25:00Z'], &d retrieved_at: &e '2026-10-25T09:31:16-04:00'},
  quote_defaults: [{<<: &B {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &N {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &Q {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i Las Vegas Raiders +3.5, line: 3.5, odds: -120, &k odds_ts: 1792855665.1066895, quote: &w [
            *i, '-120']}, {*j: &l Los Angeles Rams -3.5, line: -3.5, odds: -102, *k: 1792855665.1066895, quote: [*l, '-102']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Over 48.5, line: 48.5, odds: -104, *k: 1792929812.9952729, quote: [*q,
            '-104']}, {*j: &r Under 48.5, line: 48.5, odds: -115, *k: 1792855665.1066895, quote: [*r, '-115']}]}, {<<: *m,
      *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: -174, *k: 1792929513.019033, quote: [*s, '-174']}, {*j: *t,
          line: *u, odds: 146, *k: 1792929513.019033, quote: [*t, '146']}]}, {<<: &x {book: *v, *f: *g, *b: *c, *d: *e}, *n: R17,
      *o: point_spread, *p: [{*j: *i, line: 3.5, odds: -120, *k: 1792929293.4292977, quote: *w}, {*j: *l, line: -3.5, odds: 100,
          *k: 1792929293.4292977, quote: [*l, '100']}]}, {<<: *x, *n: R17, *o: total_points, *p: [{*j: *r, line: 48.5, odds: -110,
          *k: 1792895600.5302916, quote: [*r, '-110']}, {*j: *q, line: 48.5, odds: -110, *k: 1792895600.5302916, quote: [
            *q, '-110']}]}, {<<: *x, *n: R17, *o: moneyline, *p: [{*j: *t, line: *u, odds: 150, *k: 1792929654.7869587, quote: [
            *t, '150']}, {*j: *s, line: *u, odds: -180, *k: 1792929654.7869587, quote: [*s, '-180']}]}], props: [{*n: R20,
      &C player: &A Blake Corum, *o: receiving_yards, *y: *z, &D identity: &P {&E position: RB, team: *s, *b: &F 'https://api.opticodds.com/api/v3/players',
        quote: [*A, RB, *s], *d: &H '2026-10-25T09:36:54-04:00'}, &I quotes: [{<<: *B, line: 9.5, over: -113, under: -113,
          quote: [*A, '9.5', '-113', '-113'], *k: &J [1792873593.0162888, 1792873593.0162888]}], &K exchange: &L []}, {*n: R20,
      *C: &G Tre Tucker, *o: receiving_yards, *y: *z, *D: {*E: WR, team: *t, *b: *F, quote: [*G, WR, *t], *d: *H}, *I: [{
          <<: *B, line: 40.5, over: -113, under: -113, quote: [*G, '40.5', '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *C: &M Kyren
        Williams, *o: &O rushing_attempts, *y: *z, *D: {*E: RB, team: *s, *b: *F, quote: [*M, RB, *s], *d: *H}, *I: [{<<: *N,
          line: 15.5, over: -102, under: -125, quote: [*M, '15.5', '-102', '-125'], *k: &S [1792929642.9298606, 1792929642.9298606]}],
      *K: *L}, {*n: R20, *C: *A, *o: *O, *y: *z, *D: *P, *I: [{<<: *Q, line: 8.5, over: 105, under: -140, quote: [*A, '8.5',
            '105', '-140'], *k: [1792930735.8091307, 1792930735.8091307]}], *K: *L}, {*n: R20, *C: &R Ashton Jeanty, *o: *O,
      *y: *z, *D: {*E: RB, team: *t, *b: *F, quote: [*R, RB, *t], *d: *H}, *I: [{<<: *N, line: 14.5, over: -122, under: -104,
          quote: [*R, '14.5', '-122', '-104'], *k: *S}], *K: *L}]}
```

```yaml
{&z game_id: &A GB@DET 2026-10-25, start_et: '2026-10-25T16:25:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&t Green Bay Packers, &s Detroit Lions, '2026-10-25T20:25:00Z'], &d retrieved_at: &e '2026-10-25T09:31:20-04:00'},
  quote_defaults: [{<<: &C {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: &T {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &V {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i Detroit Lions -3.5, line: -3.5, odds: -108, &k odds_ts: 1792888443.1311166, quote: [
            *i, '-108']}, {*j: &l Green Bay Packers +3.5, line: 3.5, odds: -112, *k: 1792888443.1311166, quote: [*l, '-112']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Over 55.5, line: 55.5, odds: -110, *k: 1792922253.0204296, quote: &y [
            *q, '-110']}, {*j: &r Under 55.5, line: 55.5, odds: -110, *k: 1792922253.0204296, quote: &x [*r, '-110']}]}, {
      <<: *m, *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: -190, *k: 1792892703.1202388, quote: [*s, '-190']},
        {*j: *t, line: *u, odds: 160, *k: 1792892703.1202388, quote: [*t, '160']}]}, {<<: &w {book: *v, *f: *g, *b: *c, *d: *e},
      *n: R17, *o: point_spread, *p: [{*j: *l, line: 3.5, odds: -120, *k: 1792931137.8260083, quote: [*l, '-120']}, {*j: *i,
          line: -3.5, odds: 100, *k: 1792931137.8260083, quote: [*i, '100']}]}, {<<: *w, *n: R17, *o: total_points, *p: [
        {*j: *r, line: 55.5, odds: -110, *k: 1792931122.1254008, quote: *x}, {*j: *q, line: 55.5, odds: -110, *k: 1792931122.1254008,
          quote: *y}]}, {<<: *w, *n: R17, *o: moneyline, *p: [{*j: *t, line: *u, odds: 150, *k: 1792933452.8001916, quote: [
            *t, '150']}, {*j: *s, line: *u, odds: -180, *k: 1792933452.8001916, quote: [*s, '-180']}]}], props: [{*n: R20,
      &D player: &B Matthew Golden, *o: &E receiving_yards, *z: *A, &F identity: {&G position: WR, team: *t, *b: &H 'https://api.opticodds.com/api/v3/players',
        quote: [*B, WR, *t], *d: &J '2026-10-25T09:36:54-04:00'}, &K quotes: [{<<: *C, line: 74.5, over: -113, under: -113,
          quote: [*B, '74.5', '-113', '-113'], *k: [1792928582.9257698, 1792928582.9257698]}], &L exchange: &M []}, {*n: R20,
      *D: &I Josh Jacobs, *o: *E, *z: *A, *F: &S {*G: RB, team: *t, *b: *H, quote: [*I, RB, *t], *d: *J}, *K: [{<<: *C, line: 9.5,
          over: -113, under: -113, quote: [*I, '9.5', '-113', '-113'], *k: &O [1792873593.0162888, 1792873593.0162888]}],
      *L: *M}, {*n: R20, *D: &N Christian Watson, *o: *E, *z: *A, *F: {*G: WR, team: *t, *b: *H, quote: [*N, WR, *t], *d: *J},
      *K: [{<<: *C, line: 74.5, over: -113, under: -113, quote: [*N, '74.5', '-113', '-113'], *k: *O}], *L: *M}, {*n: R20,
      *D: &P Jameson Williams, *o: *E, *z: *A, *F: {*G: WR, team: *s, *b: *H, quote: [*P, WR, *s], *d: *J}, *K: [{<<: *C,
          line: 54.5, over: -113, under: -113, quote: [*P, '54.5', '-113', '-113'], *k: *O}], *L: *M}, {*n: R20, *D: &Q Amon-Ra
        St. Brown, *o: *E, *z: *A, *F: {*G: WR, team: *s, *b: *H, quote: [*Q, WR, *s], *d: *J}, *K: [{<<: *C, line: 78.5,
          over: -113, under: -113, quote: [*Q, '78.5', '-113', '-113'], *k: *O}], *L: *M}, {*n: R20, *D: &R Pierre Strong
        Jr., *o: *E, *z: *A, *F: {*G: RB, team: *t, *b: *H, quote: [*R, RB, *t], *d: *J}, *K: [{<<: *C, line: 6.5, over: -113,
          under: -113, quote: [*R, '6.5', '-113', '-113'], *k: *O}], *L: *M}, {*n: R20, *D: *I, *o: rushing_attempts, *z: *A,
      *F: *S, *K: [{<<: *T, line: 13.5, over: 102, under: -130, quote: [*I, '13.5', '102', '-130'], *k: [1792931137.8260083,
            1792931139.3031466]}], *L: *M}, {*n: R20, *D: &U Jahmyr Gibbs, *o: rushing_attempts, *z: *A, *F: {*G: RB, team: *s,
        *b: *H, quote: [*U, RB, *s], *d: *J}, *K: [{<<: *V, line: 20.5, over: -110, under: -120, quote: [*U, '20.5', '-110',
            '-120'], *k: [1792851204.7760634, 1792851204.7760634]}], *L: *M}]}
```

```yaml
{&x game_id: &y KC@SEA 2026-10-25, start_et: '2026-10-25T20:20:00-04:00', fixture_evidence: {&b source_url: &c 'https://api.opticodds.com/api/v3/fixtures/odds',
    quote: [&s Kansas City Chiefs, &t Seattle Seahawks, '2026-10-26T00:20:00Z'], &d retrieved_at: &e '2026-10-25T09:31:20-04:00'},
  quote_defaults: [{<<: &A {book: &h FanDuel, &f price_type: &g reference, *b: *c, url: *c, *d: *e}}, {<<: {book: &v DraftKings,
        *f: *g, *b: *c, url: *c, *d: *e}}, {<<: {book: BetMGM, *f: *g, *b: *c, url: *c, *d: *e}}, {<<: &S {book: Caesars,
        *f: *g, *b: *c, url: *c, *d: *e}}], game_prices: [{<<: &m {book: *h, *f: *g, *b: *c, *d: *e}, &n req_id: R17, &o market: point_spread,
      &p observations: [{&j selection: &i Seattle Seahawks -3, line: -3, odds: -105, &k odds_ts: 1792861254.648747, quote: [
            *i, '-105']}, {*j: &l Kansas City Chiefs +3, line: 3, odds: -115, *k: 1792861254.648747, quote: [*l, '-115']}]},
    {<<: *m, *n: R17, *o: total_points, *p: [{*j: &q Over 42.5, line: 42.5, odds: -105, *k: 1792861254.6487749, quote: [*q,
            '-105']}, {*j: &r Under 42.5, line: 42.5, odds: -115, *k: 1792861254.6487749, quote: [*r, '-115']}]}, {<<: *m,
      *n: R17, *o: moneyline, *p: [{*j: *s, line: &u UNKNOWN, odds: 130, *k: 1792863174.857669, quote: [*s, '130']}, {*j: *t,
          line: *u, odds: -154, *k: 1792863174.857669, quote: [*t, '-154']}]}, {<<: &w {book: *v, *f: *g, *b: *c, *d: *e},
      *n: R17, *o: point_spread, *p: [{*j: *i, line: -3, odds: 100, *k: 1792931392.6014438, quote: [*i, '100']}, {*j: *l,
          line: 3, odds: -120, *k: 1792931392.6014438, quote: [*l, '-120']}]}, {<<: *w, *n: R17, *o: total_points, *p: [{
          *j: *r, line: 42.5, odds: -110, *k: 1792895577.4487615, quote: [*r, '-110']}, {*j: *q, line: 42.5, odds: -110, *k: 1792895577.4487615,
          quote: [*q, '-110']}]}, {<<: *w, *n: R17, *o: moneyline, *p: [{*j: *t, line: *u, odds: -148, *k: 1792927230.8656344,
          quote: [*t, '-148']}, {*j: *s, line: *u, odds: 124, *k: 1792927230.8656344, quote: [*s, '124']}]}], weather: {*n: R19,
    *b: 'https://api.open-meteo.com/v1/forecast?latitude=47.5952&longitude=-122.3316&hourly=temperature_2m,wind_speed_10m,wind_gusts_10m,precipitation_probability&temperature_unit=fahrenheit&wind_speed_unit=mph&timezone=America%2FNew_York&start_date=2026-10-25&end_date=2026-10-25',
    *d: '2026-10-25T09:31:51-04:00', exact_kickoff_forecast: *u, hourly_samples: [{time_et: '2026-10-25T20:00-04:00', temp_f: 52.4,
        wind_mph: 7.1, gust_mph: 17.4, precip_probability_pct: 23, quote: ['2026-10-25T20:00', '52.4', '7.1', '17.4', '23']},
      {time_et: '2026-10-25T21:00-04:00', temp_f: 50.6, wind_mph: 5.3, gust_mph: 8.9, precip_probability_pct: 19, quote: [
          '2026-10-25T21:00', '50.6', '5.3', '8.9', '19']}]}, props: [{*n: R20, &B player: &z George Holani, *o: &C receiving_yards,
      *x: *y, &D identity: {&E position: RB, team: *t, *b: &F 'https://api.opticodds.com/api/v3/players', quote: [*z, RB,
          *t], *d: &H '2026-10-25T09:36:54-04:00'}, &I quotes: [{<<: *A, line: 8.5, over: -113, under: -113, quote: [*z, '8.5',
            '-113', '-113'], *k: &J [1792887684.4681368, 1792887684.4681368]}], &K exchange: &L []}, {*n: R20, *B: &G Kenneth
        Walker III, *o: *C, *x: *y, *D: &R {*E: RB, team: *s, *b: *F, quote: [*G, RB, *s], *d: *H}, *I: [{<<: *A, line: 21.5,
          over: -113, under: -113, quote: [*G, '21.5', '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &M Xavier Worthy,
      *o: *C, *x: *y, *D: {*E: WR, team: *s, *b: *F, quote: [*M, WR, *s], *d: *H}, *I: [{<<: *A, line: 49.5, over: -113, under: -113,
          quote: [*M, '49.5', '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &N Noah Gray, *o: *C, *x: *y, *D: {*E: TE,
        team: *s, *b: *F, quote: [*N, TE, *s], *d: *H}, *I: [{<<: *A, line: 15.5, over: -113, under: -113, quote: [*N, '15.5',
            '-113', '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &O Emanuel Wilson, *o: *C, *x: *y, *D: &T {*E: RB, team: *t,
        *b: *F, quote: [*O, RB, *t], *d: *H}, *I: [{<<: *A, line: 7.5, over: -113, under: -113, quote: [*O, '7.5', '-113',
            '-113'], *k: *J}], *K: *L}, {*n: R20, *B: &P Jaxon Smith-Njigba, *o: *C, *x: *y, *D: {*E: WR, team: *t, *b: *F,
        quote: [*P, WR, *t], *d: *H}, *I: [{<<: *A, line: 92.5, over: -113, under: -113, quote: [*P, '92.5', '-113', '-113'],
          *k: *J}], *K: *L}, {*n: R20, *B: &Q AJ Barner, *o: *C, *x: *y, *D: {*E: TE, team: *t, *b: *F, quote: [*Q, TE, *t],
        *d: *H}, *I: [{<<: *A, line: 24.5, over: -113, under: -113, quote: [*Q, '24.5', '-113', '-113'], *k: *J}], *K: *L},
    {*n: R20, *B: *G, *o: rushing_attempts, *x: *y, *D: *R, *I: [{<<: *S, line: 18.5, over: -122, under: -108, quote: [*G,
            '18.5', '-122', '-108'], *k: [1792884767.7026727, 1792884767.7026727]}], *K: *L}, {*n: R20, *B: *O, *o: rushing_attempts,
      *x: *y, *D: *T, *I: [{<<: *S, line: 14.5, over: -113, under: -115, quote: [*O, '14.5', '-113', '-115'], *k: [1792859097.8663704,
            1792859097.8663704]}], *K: *L}]}
```

```yaml
{gaps: [No current-day request file or NFL Job B baseline was present; newest request file used., R17 Monday DAL@PHI and historical
      Thursday NE@CHI closing-total conflict are outside today's-only scope., 'R18 Friday report timestamps, depth ranks,
      some requested historical career-start facts, and confirmed starters/replacement roles UNKNOWN. Blank official game
      status is not converted to AVAILABLE.', 'R19 Paris 09:30 and Seattle 20:20 exact kickoff values UNKNOWN; adjacent hourly
      samples shown without interpolation.', R20 FD receiving-yards board includes retrieved main lines meeting position/threshold
      criteria. Alternate lines are not exhaustively transcribed. FanDuel RB rushing-attempt main quotes absent in fetched
      feed; one available book per RB shown instead; additional fetched prices omitted under the issue-body cap., 'R20 top-two
      RB/top-three receiver depth ranks UNKNOWN. No TD candidate section delivered: verified depth ranks unavailable and complete
      candidate prices exceed the GitHub issue-body cap.', 'Kalshi response returned American-odds order_book ladders without
      explicitly labeled cash yes_bid/yes_ask. No bid/ask or mid inferred from those ladders; all Kalshi bid/ask, fee, depth
      and mid fields UNKNOWN. No executable exchange quote delivered.', R21 all per-player season-share/efficiency inputs
      and per-team PROE remain UNKNOWN. Attempted Sharp URL returned a fetch error; no estimates substituted., 'Executable
      book verification unavailable: all feed prices are reference only, including sportsbook-branded records.', Credit usage
      is not available or reliably estimable; no fabricated whole-number estimate supplied.], exchange_missing: {venue: Kalshi,
    yes_bid: &b UNKNOWN, yes_ask: *b, fee_shown: *b, depth_note: *b, mid: *b, source_url: 'https://api.opticodds.com/api/v3/fixtures/odds',
    retrieved_at: '2026-10-25T09:36:54-04:00'}, quarantine: [{url: 'https://amp.nfl.com/news/week-7-injuries-sunday-pregame-2026-nfl-season',
      reason: 'Denver injury item says against Atlanta, conflicting with the verified DEN@ARI fixture; item not used as a
        matchup fact.'}], summary: '12 Sunday games; FD/DK main game prices; 74 FD receiving-yard rows; 28 RB rushing-attempt
    rows; 0 unranked TD candidate rows; official statuses and six-location weather; rank, alt-line, exchange and season-share
    gaps explicit.'}
```
credits_used_estimate: UNKNOWN
