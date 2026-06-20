# Implementation Roadmap

Last verified: 2026-06-20

## Phase 1: Core Algorithms

| Implementation | Concept |
| --- | --- |
| token bucket | rate limiting and burst handling |
| sliding window counter | rate limiting precision vs memory |
| consistent hash ring | sharding and rebalance cost |
| Snowflake-style ID | distributed ID generation |

## Phase 2: Storage and Messaging

| Implementation | Concept |
| --- | --- |
| append-only key-value store | storage engine basics |
| log compaction | write amplification and cleanup |
| in-memory queue | producer/consumer model |
| visibility timeout queue | retry and at-least-once delivery |

## Phase 3: Product Systems

| Implementation | Concept |
| --- | --- |
| URL shortener | API, storage, redirects, cache |
| autocomplete | trie/index/ranking |
| news feed fanout simulator | fanout-on-write vs fanout-on-read |
| chat ordering simulator | message ordering and delivery states |

## Phase 4: Data-heavy Systems

| Implementation | Concept |
| --- | --- |
| crawler frontier | dedupe, politeness, scheduling |
| leaderboard | ranking and update cost |
| metrics aggregator | time buckets and rollups |
| object storage simulator | metadata, chunks, durability |

## Implementation Note Template

For every implementation, write:

- goal
- API
- data structures
- run command
- test command
- limitations
- scaling note
- related case study
