from rate_limiter import SlidingWindow, TokenBucket


def test_token_bucket_refills() -> None:
    bucket = TokenBucket(capacity=2, refill_per_second=1)
    assert bucket.allow(0.0) is True
    assert bucket.allow(0.0) is True
    assert bucket.allow(0.0) is False
    assert bucket.allow(1.0) is True


def test_sliding_window_expires_old_hits() -> None:
    limiter = SlidingWindow(limit=2, window_seconds=1)
    assert limiter.allow(0.0) is True
    assert limiter.allow(0.2) is True
    assert limiter.allow(0.3) is False
    assert limiter.allow(1.1) is True


if __name__ == "__main__":
    test_token_bucket_refills()
    test_sliding_window_expires_old_hits()
    print("ok")

