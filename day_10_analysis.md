# Final Analysis
- Shard 1 failed first due to hotspot.
- Hash-based sharding is best for writes, but expensive for reads (requires cross-shard query).
- Added cross-shard query aggregation logic.
