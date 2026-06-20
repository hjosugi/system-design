from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    capacity: int
    refill_per_second: float
    tokens: float = field(init=False)
    updated_at: float = 0.0

    def __post_init__(self) -> None:
        self.tokens = float(self.capacity)

    def allow(self, now: float) -> bool:
        elapsed = max(0.0, now - self.updated_at)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_per_second)
        self.updated_at = now
        if self.tokens < 1:
            return False
        self.tokens -= 1
        return True


@dataclass
class SlidingWindow:
    limit: int
    window_seconds: float
    hits: deque[float] = field(default_factory=deque)

    def allow(self, now: float) -> bool:
        while self.hits and self.hits[0] <= now - self.window_seconds:
            self.hits.popleft()
        if len(self.hits) >= self.limit:
            return False
        self.hits.append(now)
        return True


def simulate() -> None:
    bucket = TokenBucket(capacity=3, refill_per_second=1)
    window = SlidingWindow(limit=3, window_seconds=2)
    moments = [0, 0.1, 0.2, 0.3, 1.5, 2.2]
    for now in moments:
        print(f"{now:>4}: bucket={bucket.allow(now)} window={window.allow(now)}")


if __name__ == "__main__":
    simulate()

