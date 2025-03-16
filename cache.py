import matplotlib.pyplot as plt
import threading
import random
import time

def create_cache_block(tag=-1, valid_bit=False, timestamp=0):
    return {
        "tag": tag,
        "valid_bit": valid_bit,
        "timestamp": timestamp
    }

def create_cache_set(associativity):
    return [create_cache_block() for _ in range(associativity)]

def cache(cache_size, block_size, associativity, replacement_policy):
    num_sets = cache_size // (block_size * associativity)
    sets = [create_cache_set(associativity) for _ in range(num_sets)]
    return {
        "cache_size": cache_size,
        "block_size": block_size,
        "associativity": associativity,
        "num_sets": num_sets,
        "sets": sets,
        "replacement_policy": replacement_policy,
        "timestamp": 0
    }

def access_cache(cache, address):
    start_time = time.time()
    index_bits = len(bin(cache["num_sets"] - 1)[2:])
    offset_bits = len(bin(cache["block_size"] - 1)[2:])
    tag_bits = 16 - index_bits - offset_bits
    tag = (address >> (index_bits + offset_bits)) & ((1 << tag_bits) - 1)
    index = (address >> offset_bits) % cache["num_sets"]
    set_blocks = cache["sets"][index]
    cache["timestamp"] += 1
    for block in set_blocks:
        if block["valid_bit"] and block["tag"] == tag:
            block["timestamp"] = cache["timestamp"]
            return True, False, False, None, time.time() - start_time
    
    eviction = None
    if any(not block["valid_bit"] for block in set_blocks):
        replacement_index = next(i for i, block in enumerate(set_blocks) if not block["valid_bit"])
    else:
        if cache["replacement_policy"] == "LRU":
            replacement_index = min(range(cache["associativity"]), key=lambda i: set_blocks[i]["timestamp"])
        elif cache["replacement_policy"] == "FIFO":
            replacement_index = 0  # FIFO replaces the first inserted block
        else:
            replacement_index = random.randint(0, cache["associativity"] - 1)
        eviction = set_blocks[replacement_index]["valid_bit"]
    
    set_blocks[replacement_index]["tag"] = tag
    set_blocks[replacement_index]["valid_bit"] = True
    set_blocks[replacement_index]["timestamp"] = cache["timestamp"]
    return False, True, True, eviction, time.time() - start_time

def simulate_cache(cache_l1, cache_l2, memory_trace):
    hits_l1 = misses_l1 = hits_l2 = misses_l2 = evictions = total_accesses = 0
    access_times = []
    
    def process_address(address):
        nonlocal hits_l1, misses_l1, hits_l2, misses_l2, evictions, total_accesses, access_times
        total_accesses += 1
        hit_l1, miss_l1, _, eviction, time_taken = access_cache(cache_l1, address)
        access_times.append(time_taken)
        if hit_l1:
            hits_l1 += 1
        if miss_l1:
            misses_l1 += 1
            hit_l2, miss_l2, _, eviction, time_taken = access_cache(cache_l2, address)
            access_times.append(time_taken)
            if hit_l2:
                hits_l2 += 1
            if miss_l2:
                misses_l2 += 1
                if eviction:
                    evictions += 1
    
    threads = []
    for address in memory_trace:
        thread = threading.Thread(target=process_address, args=(address,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
    return hits_l1, misses_l1, hits_l2, misses_l2, evictions, total_accesses, access_times

def display_results(hits_l1, misses_l1, hits_l2, misses_l2, evictions, total_accesses, access_times):
    with open("results.txt", "w") as f:
        f.write("Cache Simulation Results\n")
        f.write("-----------------------\n")
        f.write(f"Total Accesses: {total_accesses}\n")
        f.write(f"L1 Hits: {hits_l1}\n")
        f.write(f"L1 Misses: {misses_l1}\n")
        f.write(f"L2 Hits: {hits_l2}\n")
        f.write(f"L2 Misses: {misses_l2}\n")
        f.write(f"Evictions: {evictions}\n")
        f.write(f"Average Access Time: {sum(access_times) / len(access_times) if access_times else 0:.6f} seconds\n")
    print("Results saved to results.txt")
    labels = ['L1 Hits', 'L1 Misses', 'L2 Hits', 'L2 Misses', 'Evictions']
    values = [hits_l1, misses_l1, hits_l2, misses_l2, evictions]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'red', 'blue', 'orange', 'purple'])
    plt.xlabel("Cache Metrics")
    plt.ylabel("Count")
    plt.title("Cache Performance")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig("cache_performance.png")
    print("Graph saved as cache_performance.png")

def main():
    print("......Multilevel Cache Simulator (L1 & L2)......")
    cache_size_l1 = int(input("Enter L1 cache size in bytes: "))
    cache_size_l2 = int(input("Enter L2 cache size in bytes: "))
    block_size = int(input("Enter block size in bytes: "))
    associativity = int(input("Enter associativity (1 for Direct Mapping, N for N-Way Set Associative): "))
    replacement_policy = input("Choose Replacement Policy (LRU, FIFO, Random): ").strip().upper()
    memory_trace = [random.randint(0, 0xFFFF) for _ in range(1000)]
    cache_l1 = cache(cache_size_l1, block_size, associativity, replacement_policy)
    cache_l2 = cache(cache_size_l2, block_size, associativity, replacement_policy)
    hits_l1, misses_l1, hits_l2, misses_l2, evictions, total_accesses, access_times = simulate_cache(cache_l1, cache_l2, memory_trace)
    display_results(hits_l1, misses_l1, hits_l2, misses_l2, evictions, total_accesses, access_times)

if __name__ == "__main__":
    main()

