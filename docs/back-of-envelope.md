# Back-of-the-envelope Estimation

Last verified: 2026-06-20

## Basic Units

| Item | Memory hook |
| --- | --- |
| QPS | requests per second |
| peak QPS | average QPS times peak multiplier |
| DAU | daily active users |
| R/W ratio | reads usually dominate social/product systems |
| storage/day | writes per day times average object size |
| bandwidth | bytes per second across read/write paths |
| cache size | hot working set, not total dataset |

## Common Flow

1. Start from users or events per day.
2. Convert to requests per second.
3. Apply peak multiplier.
4. Estimate read/write split.
5. Estimate payload size.
6. Estimate storage growth.
7. Estimate bandwidth.
8. Decide partitions and replication factor.

## Quick Formulas

```text
daily_requests = users * requests_per_user_per_day
average_qps = daily_requests / 86_400
peak_qps = average_qps * peak_multiplier
daily_storage = writes_per_day * average_record_size
yearly_storage = daily_storage * 365
read_bandwidth = read_qps * average_response_size
write_bandwidth = write_qps * average_write_size
```

## What To Say In An Interview

- "I will make rough assumptions and adjust if the interviewer disagrees."
- "I care more about order of magnitude than exact arithmetic."
- "This number tells us which component needs a deep dive."

## Drills

- Estimate a URL shortener with 100M new URLs per month.
- Estimate a chat system with 50M DAU and 40 messages per user per day.
- Estimate object storage for 10M daily uploads.
- Estimate metrics ingestion for 1M hosts reporting every 10 seconds.
