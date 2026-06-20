# 2026 Learning Items: System Design

Last verified: 2026-06-20

## Must Learn

### Interview execution

- clarify goals
- define functional requirements
- define non-functional requirements
- estimate capacity
- draw high-level design
- deep dive on bottlenecks
- discuss tradeoffs
- close with monitoring and failure handling

Projects:

- `docs/interview-framework.md`
- `templates/system-design-case-study.md`

### Estimation

- QPS
- peak QPS
- read/write ratio
- storage per day/month/year
- bandwidth
- cache size
- number of partitions
- replication factor
- availability targets

Projects:

- `docs/back-of-envelope.md`
- estimation drills for URL shortener, chat, object storage, and metrics

### Core components

- load balancing
- cache
- CDN
- SQL vs NoSQL
- replication
- sharding
- queues and streams
- rate limiting
- consistent hashing
- distributed IDs
- object storage

Projects:

- component memorization notes
- toy implementations under `implementations/`

### Product system patterns

- read-heavy services
- write-heavy services
- fanout
- realtime messaging
- search and autocomplete
- event aggregation
- booking/transaction systems
- payment and wallet consistency

Projects:

- case studies under `case-studies/`

## Definition of Done

- Every case study has requirements, estimates, API, data model, scaling plan, failure modes, and implementation drill.
- Every memorization note is short enough to review quickly.
- Every implementation has tests or a manual verification command.
- No copyrighted course text is copied into the repo.
