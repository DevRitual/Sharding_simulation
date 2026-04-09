# Sharding Project

This is my simulation for the chat server sharding assignment. I started with one server and then built shards to handle spikes like the cricket final.

My first analysis (Day 1-2) showed that one server would just die because of memory and bandwidth if 50k people join at once. I put more details about this in day_1_2_analysis.md.

I tried routing by user and channel first. Both are bad because:
- User-based sharding fails if one user is an influencer (hotspot).
- Channel-based sharding fails if one channel is viral (like Channel 7 during the cricket match).

I fixed this using Hash-Based sharding with MD5. It spreads the messages across all 3 shards even if everyone is in one channel.

I also added a function to search across shards (day 10 task) and tested what happens if a shard goes down. The system can still fetch messages from the active servers.

Final stats from the test:
- Channel sharding: Shard 1 got crushed with ~86% of traffic.
- Hash sharding: All shards stayed around 33% load.

Files:
- sharding_simulation.py (main code)
- single_server.py (initial version)
- day_1_2_analysis.md (breakdown)
- day_10_analysis.md (final answers)
