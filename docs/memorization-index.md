# Memorization Index

Last verified: 2026-06-20

## Core Concepts

| Topic | Remember |
| --- | --- |
| load balancer | health checks, private backend IPs, stateless services |
| CDN | static content, edge cache, invalidation, TTL |
| cache | cache-aside, write-through, write-back, eviction, hot keys |
| database replication | read scaling, failover, lag |
| sharding | partition key, hot partition, rebalance |
| consistency | strong, eventual, read-your-writes, monotonic reads |
| queue | at-least-once, at-most-once, exactly-once is usually scoped |
| idempotency | safe retry for writes |
| backpressure | slow consumers must not collapse producers |
| rate limiting | token bucket, leaky bucket, fixed/sliding window |
| consistent hashing | reduce movement when nodes change |
| distributed IDs | time, worker ID, sequence, clock rollback |
| fanout | write-time vs read-time tradeoff |
| object storage | metadata, chunks, replication/erasure coding |
| observability | logs, metrics, traces, alerts, SLOs |

## Numbers To Practice

- seconds per day: 86,400
- rough QPS from daily requests
- payload sizes
- replication factor impact
- cache hit ratio impact
- peak traffic multiplier

## Failure Modes To Mention

- cache stampede
- thundering herd
- hot key
- queue backlog
- poison message
- DB replication lag
- split brain
- clock skew
- duplicate delivery
- partial failure
- cascading failure
