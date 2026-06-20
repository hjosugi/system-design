# Case Studies

Last verified: 2026-06-20

Case studies are design notes, not production specs.

Each case study should include:

- requirements
- assumptions
- API sketch
- data model
- read path
- write path
- scaling plan
- failure modes
- observability
- tradeoffs
- implementation drill
- memorization checklist

## Planned Case Studies

| Priority | Case study | Why |
| --- | --- | --- |
| 1 | URL shortener | small API, storage, redirection, cache, analytics |
| 2 | rate limiter | algorithms, distributed counters, hot keys |
| 3 | unique ID generator | clocks, ordering, sharding, collision risk |
| 4 | key-value store | storage engine basics, replication, consistency |
| 5 | chat system | realtime, fanout, presence, ordering |
| 6 | notification system | queues, retries, templates, preferences |
| 7 | news feed | fanout-on-write vs fanout-on-read |
| 8 | autocomplete | trie/index, ranking, freshness |
| 9 | object storage | metadata, chunks, durability, multipart upload |
| 10 | metrics and alerting | ingestion, aggregation, retention, alert fatigue |
