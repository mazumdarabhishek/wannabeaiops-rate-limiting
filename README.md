# Rate Limiting for Generative & Agentic AI

Rate limiting is essential for operational stability, cost control, and fair GPU resource sharing in systems that use large generative models and autonomous agents.

## Table of Contents
- [Why It Matters](#why-it-matters)
- [Core Strategies](#core-strategies)
	- [Fixed Window](#fixed-window)
	- [Sliding Window](#sliding-window)
	- [Token Bucket](#token-bucket)
	- [Leaky Bucket](#leaky-bucket)
- [Choosing the Right Strategy](#choosing-the-right-strategy)
- [Quick Recommendations](#quick-recommendations)

## Why It Matters
- **Cost control:** Calls to LLMs consume expensive GPU compute. Without limits a bug or malicious user can exhaust budgets quickly.
- **Agentic loop protection:** Autonomous agents can enter recursive or runaway loops; rate limiting acts as a circuit breaker to stop runaway costs and behavior.
- **GPU fairness & latency:** Rate limiting prevents a single heavy user from degrading performance for others by enforcing concurrency and throughput constraints.

## Core Strategies

### Fixed Window
Time is split into fixed intervals (e.g., 60-second blocks). A counter tracks requests per interval; when the limit is reached, additional requests are rejected until the next interval.

- **Pros:** Very simple, low memory overhead.
- **Cons:** Boundary bursts are possible (requests at window edges can double effective rate).

### Sliding Window
Tracks requests over a moving timeframe (exact timestamps or a weighted average of adjacent windows) to smooth rate calculations.

- **Pros:** Smooth rate limiting; prevents boundary burst behavior.
- **Cons:** Higher memory and computation cost because individual timestamps or finer-grained buckets must be tracked.

### Token Bucket
A token bucket refills at a fixed rate; each request consumes a token. Tokens can accumulate during idle periods, allowing short bursts.

- **Pros:** Flexible and supports controlled bursting; good for agent workflows that need short, rapid sequences of calls.
- **Cons:** Requires tuning (fill rate, bucket size) to avoid overwhelming downstream systems.

### Leaky Bucket
Requests enter a queue that is drained at a constant rate. Excess traffic overflows and is dropped or delayed.

- **Pros:** Produces a predictable, constant processing rate that protects downstream services.
- **Cons:** No burst flexibility; can frustrate legitimate brief spikes in traffic.

## Choosing the Right Strategy
- Use **Fixed Window** for very simple, low-cost enforcement where occasional bursts are acceptable.
- Use **Sliding Window** when you need smoother, more accurate rate calculations and can afford the memory overhead.
- Use **Token Bucket** when you need flexible burst handling (common for agentic workflows that occasionally need rapid calls).
- Use **Leaky Bucket** when protecting a fragile downstream service with strict, constant throughput requirements.

## Quick Recommendations
- For most LLM-backed services: prefer **Token Bucket** for burst flexibility with conservative calibration.
- Combine limits: apply both **per-user** and **global** quotas; add **concurrency** caps for GPU-heavy endpoints.
- Implement monitoring and circuit breakers: emit metrics for rejections and throttles; add alerting for sudden spikes.

---

If you'd like, I can:
- add configuration examples (Redis-backed token bucket, sliding window implementation),
- generate sample code and tests, or
- tune a suggested policy for your current project.

