## Google L5 Senior Software Engineer Interview Script: System Design
### Chapter 1: Scale from Zero to Millions of Users

This script follows the **4-step framework** for system design interviews as established in Alex Xu’s guide. For an L5 level at Google, the emphasis is not just on "what" components you add, but on your ability to discuss **trade-offs**, **scalability**, and **reliability** proactively.

---

#### Step 1: Understand the Problem and Establish Design Scope (3 - 10 Minutes)

**Interviewer:** "Design a web system that can scale from a single user to millions of users."

**Candidate (Senior Perspective):** "To ensure I'm building the right architecture, let me clarify the scope. Is this a generic web application supporting both mobile and web clients?. What is the expected Write-to-Read ratio? And what kind of availability SLA are we aiming for—perhaps 'three nines' (99.9%)?".

**Interviewer:** "Yes, both clients. Let's assume a Read-heavy system with a 10:1 ratio. We need high availability.".

**Candidate:** "Understood. I will start with a minimal configuration and iteratively scale based on traffic bottlenecks, focusing on statelessness and eliminating Single Points of Failure (SPOF).".

---

#### Step 2: Propose High-level Design and Get Buy-in (10 - 15 Minutes)

**Candidate:** "Initially, everything—web app, database, and cache—runs on a single server. However, as users grow, we must move the database to a separate server to scale the web and data tiers independently. I'll choose a Relational Database (RDBMS) like PostgreSQL for structured data and ACID compliance.".

**Interviewer:** "What if that single web server reaches its limit?"

**Candidate:** "Vertical scaling has a hard limit and no redundancy. I propose **Horizontal Scaling** by adding multiple web servers behind a **Load Balancer**. The Load Balancer will distribute traffic using a public IP, while servers communicate via private IPs, improving security and fault tolerance.".

---

#### Step 3: Design Deep Dive (10 - 25 Minutes)

**Interviewer:** "Now that we have multiple servers, how do you handle user data and performance?"

**Candidate:** "First, we must make the web tier **stateless**. I'll move session data out of individual servers and into a shared persistent data store like Redis or a NoSQL database. This allows our fleet to auto-scale horizontally without worrying about which server a user hits.".

**Interviewer:** "The database is now the bottleneck. How do you scale it?"

**Candidate:** "I'll implement **Database Replication**. We'll have one Master DB for writes and multiple Slaves for reads. This improves read throughput and provides a failover mechanism if the master goes down.".

**Interviewer:** "How can we further reduce latency for global users?".

**Candidate:** "Two main strategies for an L5 design:
1.  **Cache Tier**: I'll implement a **read-through cache** using an in-memory store like Redis for frequently accessed data. We need to be careful with expiration policies and consistency.".
2.  **Content Delivery Network (CDN)**: I'll move static assets (images, CSS, JS) to CDN edge servers. This reduces the load on our servers and speeds up page loads for international users.".

**Interviewer:** "What if the system handles heavy background tasks, like image processing?"

**Candidate:** "I’ll introduce a **Message Queue** to decouple these components. A producer publishes the task, and specialized workers consume it asynchronously. This allows us to scale worker nodes independently based on the queue size.".

---

#### Step 4: Wrap Up (3 - 5 Minutes)

**Candidate:** "To summarize, we've scaled from a single server to a multi-tier, distributed system capable of supporting millions of users. Key takeaways for this architecture are:
*   **Stateless Web Tier**: Enables seamless horizontal scaling.
*   **Redundancy**: Introduced at every layer (Load Balancers, DB Replication) to avoid SPOF.
*   **Caching & CDN**: Drastically reduces latency and DB load.
*   **Database Sharding**: As data grows further, we would split our large database into smaller shards based on a sharding key like `user_id`.
*   **Monitoring**: We must invest in logging and metrics (CPU, throughput) to proactively identify the next bottleneck.".

**Interviewer:** "Great. That covers the foundational scaling journey.".