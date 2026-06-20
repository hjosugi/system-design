# System Design

System design interview and engineering practice repo for memorization, design frameworks, back-of-the-envelope estimation, case studies, and small implementations.

Last verified: 2026-06-20

## Runnable Starter Project

Start with the rate limiter implementation drill:

```bash
python3 implementations/rate-limiter-lab/rate_limiter.py
python3 implementations/rate-limiter-lab/test_rate_limiter.py
```

## Why This Repo Exists

System design learning has two different jobs:

- remember core concepts quickly during an interview or design review
- build small implementations so the concepts become concrete

This repo keeps both together. The goal is not to copy a course or collect long notes. The goal is to turn recurring system design topics into reusable checklists, templates, drills, and runnable experiments.

## What This Repo Teaches

Each topic should answer:

- what problem the system solves
- core API and data model
- traffic and storage assumptions
- read/write path
- scaling bottleneck
- consistency and availability choices
- observability and failure modes
- one small implementation exercise
- what to memorize before an interview

## Learning Path

1. Interview framework and clarification questions
2. Back-of-the-envelope estimation
3. Web tier, load balancers, databases, cache, CDN
4. Partitioning, replication, consistency, availability
5. Queues, streams, retries, idempotency, backpressure
6. Core building blocks: rate limiter, consistent hashing, ID generator, key-value store
7. Product systems: URL shortener, feed, chat, notification, autocomplete
8. Data-heavy systems: crawler, search, metrics, ad aggregation, object storage
9. Realtime and finance-like systems: leaderboard, payment, wallet, exchange
10. Implementation drills and review checklists

## Planned Structure

```text
case-studies/
  README.md
implementations/
  README.md
memorization/
  README.md
templates/
  system-design-case-study.md
  component-implementation.md
docs/
  2026-learning-items.md
  back-of-envelope.md
  implementation-roadmap.md
  interview-framework.md
  memorization-index.md
  problem-catalog.md
  repository-profile.md
```

## Case Study Groups

| Group | Examples |
| --- | --- |
| Foundations | scale from one server, estimation, interview framework |
| Core components | rate limiter, consistent hashing, key-value store, unique ID generator |
| Web products | URL shortener, web crawler, notification system, news feed, chat, autocomplete |
| Media and files | video platform, file sync, object storage |
| Geo and social | proximity service, nearby friends, maps |
| Infrastructure | message queue, metrics and alerting, email service |
| Business systems | hotel reservation, ad click aggregation, payment, digital wallet |
| Realtime systems | gaming leaderboard, stock exchange |

## Implementation Strategy

Start small and local:

- in-memory first
- deterministic tests
- clear API boundaries
- one scaling note per implementation
- optional persistence after the behavior is clear

Do not build production clones. Build small, readable components that make the design tradeoff visible.

## Relationship To Other Repos

- `low-level-design`: object-oriented design and code-structure problems
- `learning-backend-ddd`: backend framework and DDD implementation
- `learning-data-stores`: database behavior and data-store comparisons
- `learning-platform-engineering`: deployment, observability, runbooks, NGINX, CI
- `learning-backend-ddd`, `learning-frontend-typescript`, `learning-ai-python`: public API, GraphQL, MCP, external API clients
- `learning-platform-engineering`, `learning-frontend-typescript`: P2P, WebRTC, libp2p, transport-level networking

## First Milestones

1. Add memorization cheatsheets for estimation, cache, DB, queue, consistency, and availability.
2. Add case-study template and fill one page for URL shortener.
3. Implement token bucket and sliding-window rate limiters.
4. Implement consistent hashing ring.
5. Implement Snowflake-style unique ID generator.
6. Implement toy URL shortener with in-memory storage.
7. Add review checklist for system design answers.

## Public Safety

- No copied course text.
- No private interview material.
- No proprietary diagrams.
- Diagrams should be original and source-controlled as Mermaid or simple text.
- External references should be linked, not pasted wholesale.
