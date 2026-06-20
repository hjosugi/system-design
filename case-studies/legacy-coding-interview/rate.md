### **Google System Design Interview Script: Rate Limiter Design**

#### **Step 1: Understand the Problem and Establish Design Scope (5–10 mins)**
**Candidate:** Before diving into the architecture, I’d like to clarify the requirements. Are we designing a client-side or server-side rate limiter?
**Interviewer:** Let’s focus on a server-side API rate limiter.
**Candidate:** Understood. What properties are we throttling based on? (e.g., User ID, IP address, or specific API endpoints?)
**Interviewer:** It should be flexible enough to support different sets of rules.
**Candidate:** What is the scale? Are we talking about a single-server startup or a global system supporting millions of users?
**Interviewer:** The system must handle a large volume of requests and operate in a distributed environment.
**Candidate:** Got it. For my non-functional requirements, I’ll prioritize:
1.  **Low Latency:** The limiter shouldn't significantly increase API response times.
2.  **Accuracy:** It must effectively block excessive requests according to the rules.
3.  **High Fault Tolerance:** If the rate limiter service goes down, it shouldn't crash the entire system.
4.  **Distributed Consistency:** Throttling must be synchronized across multiple servers.

#### **Step 2: High-Level Design (10–15 mins)**
**Candidate:** I’ll place the rate limiter as a **middleware** component. In a cloud microservices architecture, this is typically implemented within an **API Gateway**.
**Candidate:** Now, I need to select a rate-limiting algorithm. There are several options:
1.  **Token Bucket:** Simple to implement and handles burst traffic well.
2.  **Leaking Bucket:** Ensures a stable outflow rate but can be tricky to tune.
3.  **Fixed Window Counter:** Simple but suffers from traffic spikes at window boundaries.
4.  **Sliding Window Log/Counter:** More accurate but can consume more memory.
**Candidate:** Given our requirement for scalability and efficiency, I’ll propose the **Token Bucket** algorithm. It is widely used by companies like Stripe and Amazon because it allows for short bursts of traffic while remaining memory efficient.
**Candidate:** For storage, using a traditional database would be too slow due to disk I/O. I’ll use an **in-memory cache like Redis**. It’s ideal for this because it supports fast `INCR` and `EXPIRE` operations.

#### **Step 3: Design Deep Dive (10–25 mins)**
**Interviewer:** How would this work in a distributed environment where we have millions of users?
**Candidate:** This introduces two major challenges: **Race Conditions** and **Synchronization**.
1.  **Race Conditions:** If two requests reach the limiter simultaneously, they might both read the same counter value before either can increment it. I would solve this using **Lua scripts** in Redis or **Sorted Sets** to ensure atomic operations.
2.  **Synchronization:** If we have multiple rate-limiting servers, a stateless web tier might route User A’s first request to Server 1 and their second to Server 2. To ensure they share the same counter, I'll use a **centralized data store** (the Redis cluster) rather than local server memory.

**Candidate:** Regarding **Performance Optimization**, for a global user base, a single data center would incur high latency. I would utilize a **multi-data center setup** where traffic is routed to the nearest edge server. I would also adopt an **eventual consistency model** to synchronize data between regions if strict consistency isn't critical for every millisecond.

**Interviewer:** What happens when a user is throttled?
**Candidate:** The system will return a **429 (Too Many Requests)** status code. I'll also include HTTP headers like `X-Ratelimit-Remaining` and `X-Ratelimit-Retry-After` to inform the client when they can try again.

#### **Step 4: Wrap Up (3–5 mins)**
**Candidate:** To summarize, we’ve designed a distributed rate limiter that:
*   Uses a **Token Bucket** algorithm for burst handling and memory efficiency.
*   Leverages **Redis** for low-latency counter management.
*   Addresses **distributed race conditions** with Lua scripts.
*   Optimizes for global users using **edge servers**.
**Candidate:** In a real production environment, I would also implement **Monitoring** to verify if our rules are too strict (dropping valid traffic) or too loose (allowing server overload) and adjust the bucket size or refill rate accordingly. I could also consider **Hard vs. Soft limiting** depending on the business priority.

---
**Next Step:**
Would you like to continue to **Chapter 5: Design Consistent Hashing**, which is the fundamental technique for distributing these requests across servers?