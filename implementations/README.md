# Implementations

Last verified: 2026-06-20

Implementations are intentionally small. They exist to make a design idea concrete.

## Rules

- Start in-memory.
- Add tests before adding persistence.
- Prefer deterministic clocks and IDs in tests.
- Keep public APIs small.
- Document what the toy version does not handle.
- Link each implementation back to a case study or memorization note.

## Planned Implementations

| Component | First version | Later version |
| --- | --- | --- |
| rate limiter | token bucket in memory | Redis-backed distributed limiter |
| consistent hashing | hash ring with virtual nodes | rebalance simulation |
| unique ID generator | Snowflake-style ID | clock rollback handling |
| URL shortener | in-memory mapping | persistent store + cache |
| key-value store | append-only log | compaction + index |
| message queue | in-memory queue | visibility timeout + retry |
| autocomplete | trie | ranked prefix index |
| leaderboard | sorted in-memory ranking | Redis sorted-set style |
| web crawler | URL frontier | politeness + dedupe |
| object storage | chunk metadata | multipart upload simulation |
