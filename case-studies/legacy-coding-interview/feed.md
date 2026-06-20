## Google L5 Senior Software Engineer Interview Script: System Design
### Chapter 3: A Framework for System Design Interviews

At the Google L5 level, the interviewer is evaluating your **architectural maturity** and your ability to lead a design session. Chapter 3 of Alex Xu’s guide provides the "Universal Blueprint" for these 45-minute sessions. This script demonstrates how a Senior candidate uses the **News Feed System** example to showcase the 4-step framework.

---

#### **Step 1: Understand the Problem and Establish Design Scope (5–10 mins)**
*Google Signal: Proactive ambiguity resolution and requirement mapping.*

**Interviewer:** "Design a news feed system."

**Candidate (Senior Perspective):** "To ensure we build a system that aligns with the product goals, I'll start by clarifying the scope. Is this a mobile app, web app, or both? And what are the core features—is it just publishing posts and viewing a feed, or do we include friend recommendations and media support?".

**Interviewer:** "Both platforms. Focus on publishing posts and viewing a reverse-chronological feed. Media support is required.".

**Candidate:** "Understood. Now regarding the **Non-Functional Requirements (NFRs)**: 
1. **Scale:** I’ll assume 10 million Daily Active Users (DAU). 
2. **Latency:** Browsing the feed should be near-instant (under 200ms). 
3. **Availability:** The system must be highly available, even if we sacrifice some data consistency temporarily (following the CAP theorem).
4. **Reliability:** Posts should never be lost once successfully uploaded.".

---

#### **Step 2: Propose High-Level Design and Get Buy-in (10–15 mins)**
*Google Signal: Component identification and high-level data flow agreement.*

**Candidate:** "I'll break the system into two primary flows: **Feed Publishing** and **News Feed Building**. 

*   **Publishing Flow:** When a user posts, we write to a Load Balancer, which routes to a web server. The post metadata is stored in a database (Post DB) and cached (Post Cache). We then trigger a **Fanout Service** to push this post to friends' feeds.
*   **Building Flow:** When a user reads their feed, we hit a **News Feed Service** that pulls the latest aggregated posts from a **News Feed Cache** for speed.".

**Interviewer:** "Looks good. Should we use a 'Push' or 'Pull' model for the fanout?"

**Candidate (Trade-off Analysis):** "For L5 design, I’d suggest a **hybrid model**. A 'Push' model (Fanout on write) is great for low-latency reads for regular users. However, for 'Celebrity' users with millions of followers, pushing to every cache would cause a system bottleneck. For them, we'll use a 'Pull' model (Fanout on read) where followers pull the data on-demand.".

---

#### **Step 3: Design Deep Dive (10–25 mins)**
*Google Signal: Solving bottlenecks, scaling, and failure handling.*

**Candidate:** "Let's dive into **Scaling the Data Tier**. At 10M DAU, our Post DB will eventually bottleneck. I’ll implement **Database Sharding** based on `user_id` to distribute the load. To ensure high availability, we’ll use **Master-Slave Replication**, where writes go to the master and reads are distributed across multiple slaves.".

**Interviewer:** "What if a database node goes down?".

**Candidate:** "If a slave goes down, we redirect reads to others. If the master fails, a slave is promoted. We'll also use a **Message Queue** (like Kafka) between the web server and the Fanout service to decouple them. This ensures that even if the fanout workers are slow or fail, the user's post is safe in the queue and can be processed asynchronously once the system recovers.".

---

#### **Step 4: Wrap Up (3–5 mins)**
*Google Signal: Critical thinking, recap, and future considerations.*

**Candidate:** "To summarize:
*   We designed a **Stateless Web Tier** to allow easy horizontal scaling.
*   We optimized for **Low Latency** by using a multi-layered cache (News Feed, Social Graph, and Content caches).
*   We handled the **'Celebrity Problem'** with a hybrid fanout approach.
*   For **Monitoring**, I would track QPS and p99 latency to identify the next bottleneck proactively.
*   If we had more time, I'd explore **Multi-Data Center Replication** to handle regional outages and reduce global latency.".

---
**Next Step:**
Now that the framework is established, would you like to apply it to **Chapter 4: Design a Rate Limiter**, which focuses on protecting these very systems from being overwhelmed by too many requests?.