# Further Learning Resources

Last verified: 2026-06-21

Curated primary sources for this repo's named learning targets. Canonical roots
are preferred over deep guessed paths. No course text is reproduced here.

## Consistent Hashing: hash ring, virtual nodes, key distribution, minimal remap

- **Consistent Hashing and Random Trees (Karger et al., 1997, MIT)** -
  https://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/chash.pdf
  The original STOC paper that introduced consistent hashing for distributed web
  caching. The source of the "only ~1/N keys move on a node change" result this
  lab measures.

- **Dynamo: Amazon's Highly Available Key-value Store (DeCandia et al., 2007)** -
  https://www.amazon.science/publications/dynamo-amazons-highly-available-key-value-store
  Shows consistent hashing + virtual nodes used in production for partitioning
  and replication, and why naive single-token rings cause uneven load. The
  blueprint that Cassandra, Riak, and Voldemort followed.

- **Apache Cassandra documentation** - https://cassandra.apache.org/doc/
  Production data partitioning over a token ring. Maps this lab's "virtual
  nodes" directly onto Cassandra's `num_tokens` and explains token ownership,
  `nodetool ring`, and rebalancing on node add/remove.

- **Ketama consistent hashing (last.fm)** - https://github.com/RJ/ketama
  The de facto algorithm for memcached client rings. Concrete reference for how
  many virtual nodes per server real clients use and how they hash the ring.

- **A Fast, Minimal Memory, Consistent Hash Algorithm (Jump Hash, Lamping &
  Veach, Google, 2014)** - https://arxiv.org/abs/1406.2294
  A ring-free alternative with no per-node state. Good contrast for Exercise 4
  and for understanding the tradeoffs of the ring approach.

- **Maglev: A Fast and Reliable Software Network Load Balancer (Google, 2016)** -
  https://research.google/pubs/pub44824/
  Google's load balancer uses a consistent-hashing variant (Maglev hashing) for
  connection-to-backend mapping. Shows consistent hashing applied to request
  routing rather than storage.

- **Designing Data-Intensive Applications, Martin Kleppmann (O'Reilly)** -
  https://dataintensive.net
  Chapter 6 (Partitioning) covers hash partitioning, rebalancing strategies, and
  why "hash mod N" is avoided. The standard reference framing for this topic.
