import time
import random
import hashlib

# Simple message object
class Message:
    def __init__(self, u_id, c_id, text):
        self.user_id = u_id
        self.channel_id = c_id
        self.content = text
        self.ts = time.time()

# Represents one server
class Shard:
    def __init__(self, s_id):
        self.id = s_id
        self.data = []
        self.active = True

    def put(self, m):
        if not self.active:
            print(f"ERROR: Shard {self.id} is down!")
            return
        self.data.append(m)

    def get_count(self):
        return len(self.data)

    def find_msgs(self, c_id):
        return [m for m in self.data if m.channel_id == c_id]

# Manages the shards
class ShardManager:
    def __init__(self, n):
        self.shards = [Shard(i) for i in range(n)]

    def show_stats(self):
        print("\n--- Current Shard Load ---")
        total = sum(s.get_count() for s in self.shards)
        for s in self.shards:
            c = s.get_count()
            p = (c / total * 100) if total > 0 else 0
            print(f"Shard {s.id}: {c} messages ({p:.1f}%)")
            if p > 50:
                print(f"!! ALERT: Shard {s.id} is getting hammered !!")

    # Day 10 requirement: fetch across shards
    def fetch_history(self, cid, limit=10):
        print(f"Searching for Channel {cid}...")
        all_m = []
        for s in self.shards:
            if s.active:
                all_m.extend(s.find_msgs(cid))
        
        # Sort by timestamp
        all_m.sort(key=lambda x: x.ts, reverse=True)
        return all_m[:limit]

# Hash strategy
class HashManager(ShardManager):
    def route(self, m):
        # We hash the channel and timestamp to keep it spread out
        key = f"{m.channel_id}_{m.ts}"
        h = int(hashlib.md5(key.encode()).hexdigest(), 16)
        s_idx = h % len(self.shards)
        self.shards[s_idx].put(m)

# Simulation function
def simulate_load(mgr, title, count=1000, hot_channel=None):
    print(f"\nTEST: {title}")
    for _ in range(count):
        # 80% go to one channel if specified
        if hot_channel and random.random() < 0.8:
            cid = hot_channel
        else:
            cid = random.randint(1, 40)
        
        msg = Message(random.randint(1, 100), cid, "test message")
        
        # Routing logic
        if isinstance(mgr, HashManager):
            mgr.route(msg)
        else:
            # simple user-based or channel-based logic
            if "User" in title:
                idx = msg.user_id % len(mgr.shards)
            else:
                idx = msg.channel_id % len(mgr.shards)
            mgr.shards[idx].put(msg)
    
    mgr.report_stats = mgr.show_stats()

# Main runner
if __name__ == "__main__":
    print("Starting System Simulation...")
    
    # Setup
    u_mgr = ShardManager(3)
    c_mgr = ShardManager(3)
    h_mgr = HashManager(3)

    # Scenarios
    simulate_load(u_mgr, "User-Based Sharding (Viral User)", hot_channel=7)
    simulate_load(c_mgr, "Channel-Based Sharding (Viral Event)", hot_channel=7)
    simulate_load(h_mgr, "Hash-Based Sharding (Best Distribution)", hot_channel=7)

    # Test failure
    print("\n--- Failure Simulation ---")
    h_mgr.shards[1].active = False
    print("Shard 1 died!")
    res = h_mgr.fetch_history(7)
    print(f"Recovered {len(res)} messages from other shards.")
