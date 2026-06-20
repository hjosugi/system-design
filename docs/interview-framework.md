# System Design Interview Framework

Last verified: 2026-06-20

## 1. Clarify

Ask about:

- users
- core use cases
- read/write patterns
- data size
- latency target
- availability target
- consistency requirements
- privacy/security constraints
- out-of-scope features

## 2. Estimate

Estimate:

- DAU/MAU
- QPS and peak QPS
- reads vs writes
- storage growth
- bandwidth
- cache working set

## 3. Define APIs

Keep APIs minimal:

- create
- read
- update/delete if required
- list/search
- async callback or stream if required

## 4. Model Data

Identify:

- primary entities
- indexes
- access patterns
- partition key
- hot keys
- retention

## 5. Draw High-level Design

Start with:

- clients
- DNS/load balancer
- stateless service
- data store
- cache
- queue if async work exists

Then add complexity only when a requirement needs it.

## 6. Deep Dive

Pick one or two bottlenecks:

- scale writes
- scale reads
- consistency
- ranking/search
- realtime delivery
- failure recovery
- observability

## 7. Close

End with:

- tradeoffs
- monitoring
- failure modes
- rollout plan
- what you would improve with more time
