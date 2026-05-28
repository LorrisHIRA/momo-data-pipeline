"""
dsa/search.py
Huguette's DSA module — Linear Search vs Dictionary Lookup
Compares efficiency of both approaches on MoMo transaction records.
"""

import time
import random

# ─────────────────────────────────────────────
# SAMPLE DATA  (25 transactions — mirrors the
# JSON structure Nziza's parser produces)
# ─────────────────────────────────────────────
SAMPLE_TRANSACTIONS = [
    {"id": 1,  "transaction_type": "incoming",   "amount": 2000.0,  "sender": "Jane Smith",      "receiver": None,          "timestamp": "2024-05-10 16:30:51", "balance": 2000.0,  "fee": None,  "address": "M-Money"},
    {"id": 2,  "transaction_type": "outgoing",   "amount": 500.0,   "sender": None,               "receiver": "Alice Uwase",  "timestamp": "2024-05-11 08:14:22", "balance": 1500.0,  "fee": 5.0,   "address": "M-Money"},
    {"id": 3,  "transaction_type": "payment",    "amount": 3500.0,  "sender": None,               "receiver": "MTN Shop",     "timestamp": "2024-05-11 10:05:11", "balance": 11500.0, "fee": 10.0,  "address": "M-Money"},
    {"id": 4,  "transaction_type": "incoming",   "amount": 10000.0, "sender": "Eric Mugabo",      "receiver": None,          "timestamp": "2024-05-12 09:00:00", "balance": 21500.0, "fee": None,  "address": "M-Money"},
    {"id": 5,  "transaction_type": "withdrawal", "amount": 4000.0,  "sender": None,               "receiver": "ATM Kigali",   "timestamp": "2024-05-12 14:22:33", "balance": 17500.0, "fee": 20.0,  "address": "M-Money"},
    {"id": 6,  "transaction_type": "outgoing",   "amount": 750.0,   "sender": None,               "receiver": "Bob Nkurunz", "timestamp": "2024-05-13 07:45:00", "balance": 16750.0, "fee": 5.0,   "address": "M-Money"},
    {"id": 7,  "transaction_type": "payment",    "amount": 1200.0,  "sender": None,               "receiver": "RwandAir",     "timestamp": "2024-05-13 11:30:09", "balance": 15550.0, "fee": 10.0,  "address": "M-Money"},
    {"id": 8,  "transaction_type": "incoming",   "amount": 5000.0,  "sender": "Claudine Mukabu", "receiver": None,          "timestamp": "2024-05-14 13:15:44", "balance": 20550.0, "fee": None,  "address": "M-Money"},
    {"id": 9,  "transaction_type": "outgoing",   "amount": 200.0,   "sender": None,               "receiver": "Diane Umuhu", "timestamp": "2024-05-14 15:00:00", "balance": 20350.0, "fee": 2.0,   "address": "M-Money"},
    {"id": 10, "transaction_type": "payment",    "amount": 900.0,   "sender": None,               "receiver": "Electrogaz",   "timestamp": "2024-05-15 08:05:12", "balance": 19450.0, "fee": 5.0,   "address": "M-Money"},
    {"id": 11, "transaction_type": "incoming",   "amount": 3000.0,  "sender": "Frank Habimana",  "receiver": None,          "timestamp": "2024-05-15 10:22:00", "balance": 22450.0, "fee": None,  "address": "M-Money"},
    {"id": 12, "transaction_type": "withdrawal", "amount": 2000.0,  "sender": None,               "receiver": "ATM Nyabugo", "timestamp": "2024-05-16 09:00:55", "balance": 20450.0, "fee": 20.0,  "address": "M-Money"},
    {"id": 13, "transaction_type": "outgoing",   "amount": 1500.0,  "sender": None,               "receiver": "Grace Iyamu", "timestamp": "2024-05-16 14:30:00", "balance": 18950.0, "fee": 10.0,  "address": "M-Money"},
    {"id": 14, "transaction_type": "payment",    "amount": 450.0,   "sender": None,               "receiver": "WASAC",        "timestamp": "2024-05-17 08:00:00", "balance": 18500.0, "fee": 5.0,   "address": "M-Money"},
    {"id": 15, "transaction_type": "incoming",   "amount": 8000.0,  "sender": "Henri Nsabiman",  "receiver": None,          "timestamp": "2024-05-17 11:11:11", "balance": 26500.0, "fee": None,  "address": "M-Money"},
    {"id": 16, "transaction_type": "outgoing",   "amount": 300.0,   "sender": None,               "receiver": "Irene Mukash","timestamp": "2024-05-18 09:45:22", "balance": 26200.0, "fee": 2.0,   "address": "M-Money"},
    {"id": 17, "transaction_type": "payment",    "amount": 2200.0,  "sender": None,               "receiver": "Irembo",       "timestamp": "2024-05-18 13:00:00", "balance": 24000.0, "fee": 10.0,  "address": "M-Money"},
    {"id": 18, "transaction_type": "incoming",   "amount": 1500.0,  "sender": "Jean Bizimana",   "receiver": None,          "timestamp": "2024-05-19 07:30:00", "balance": 25500.0, "fee": None,  "address": "M-Money"},
    {"id": 19, "transaction_type": "withdrawal", "amount": 5000.0,  "sender": None,               "receiver": "ATM Remera",   "timestamp": "2024-05-19 10:00:00", "balance": 20500.0, "fee": 20.0,  "address": "M-Money"},
    {"id": 20, "transaction_type": "outgoing",   "amount": 100.0,   "sender": None,               "receiver": "Keza Mutesi", "timestamp": "2024-05-20 08:20:00", "balance": 20400.0, "fee": 1.0,   "address": "M-Money"},
    {"id": 21, "transaction_type": "payment",    "amount": 600.0,   "sender": None,               "receiver": "Canal+",       "timestamp": "2024-05-20 09:15:00", "balance": 19800.0, "fee": 5.0,   "address": "M-Money"},
    {"id": 22, "transaction_type": "incoming",   "amount": 7500.0,  "sender": "Leon Ntwari",     "receiver": None,          "timestamp": "2024-05-21 11:00:00", "balance": 27300.0, "fee": None,  "address": "M-Money"},
    {"id": 23, "transaction_type": "outgoing",   "amount": 400.0,   "sender": None,               "receiver": "Marie Uwiman","timestamp": "2024-05-21 14:45:00", "balance": 26900.0, "fee": 3.0,   "address": "M-Money"},
    {"id": 24, "transaction_type": "payment",    "amount": 1800.0,  "sender": None,               "receiver": "RDB",          "timestamp": "2024-05-22 08:30:00", "balance": 25100.0, "fee": 10.0,  "address": "M-Money"},
    {"id": 25, "transaction_type": "incoming",   "amount": 4500.0,  "sender": "Noel Gasana",     "receiver": None,          "timestamp": "2024-05-22 16:00:00", "balance": 29600.0, "fee": None,  "address": "M-Money"},
]


# ─────────────────────────────────────────────
# DATA STRUCTURE 1 — List  (for linear search)
# ─────────────────────────────────────────────
transactions_list = SAMPLE_TRANSACTIONS.copy()


# ─────────────────────────────────────────────
# DATA STRUCTURE 2 — Dictionary  (id → record)
# ─────────────────────────────────────────────
transactions_dict = {t["id"]: t for t in SAMPLE_TRANSACTIONS}


# ══════════════════════════════════════════════
# ALGORITHM 1 — LINEAR SEARCH
# Time complexity: O(n)
# Scans every element from the start until the
# target ID is found (or the list is exhausted).
# ══════════════════════════════════════════════
def linear_search(transactions: list, target_id: int) -> dict | None:
    """
    Iterate through the list one-by-one and return
    the transaction whose 'id' matches target_id.
    Returns None if not found.
    """
    for transaction in transactions:
        if transaction["id"] == target_id:
            return transaction
    return None


# ══════════════════════════════════════════════
# ALGORITHM 2 — DICTIONARY LOOKUP
# Time complexity: O(1)  (average case)
# Python dict uses a hash table — the key is
# hashed and the value is fetched in constant
# time regardless of how many records exist.
# ══════════════════════════════════════════════
def dictionary_lookup(transactions: dict, target_id: int) -> dict | None:
    """
    Retrieve a transaction directly by key.
    Returns None if the key does not exist.
    """
    return transactions.get(target_id)


# ─────────────────────────────────────────────
# BENCHMARK HELPER
# Runs each algorithm N times and returns the
# average elapsed time in microseconds.
# ─────────────────────────────────────────────
def benchmark(func, *args, runs: int = 10_000) -> float:
    """Return average execution time in microseconds over `runs` calls."""
    start = time.perf_counter()
    for _ in range(runs):
        func(*args)
    end = time.perf_counter()
    return ((end - start) / runs) * 1_000_000   # convert to µs


# ─────────────────────────────────────────────
# COMPARISON RUNNER
# ─────────────────────────────────────────────
def compare_search_methods(test_ids: list[int]) -> None:
    print("=" * 62)
    print("   MoMo Transactions — Search Algorithm Comparison")
    print(f"   Dataset size: {len(SAMPLE_TRANSACTIONS)} records")
    print("=" * 62)
    print(f"{'ID':<6} {'Linear (µs)':>14} {'Dict (µs)':>12} {'Speedup':>10}  {'Match?'}")
    print("-" * 62)

    total_linear = 0.0
    total_dict   = 0.0

    for tid in test_ids:
        linear_time = benchmark(linear_search, transactions_list, tid)
        dict_time   = benchmark(dictionary_lookup, transactions_dict, tid)

        total_linear += linear_time
        total_dict   += dict_time

        speedup = linear_time / dict_time if dict_time > 0 else float("inf")

        # Verify both methods return the same result
        result_linear = linear_search(transactions_list, tid)
        result_dict   = dictionary_lookup(transactions_dict, tid)
        match = "✓" if result_linear == result_dict else "✗"

        print(f"{tid:<6} {linear_time:>14.4f} {dict_time:>12.4f} {speedup:>9.1f}x  {match}")

    print("-" * 62)
    avg_linear = total_linear / len(test_ids)
    avg_dict   = total_dict   / len(test_ids)
    avg_speedup = avg_linear / avg_dict if avg_dict > 0 else float("inf")
    print(f"{'AVG':<6} {avg_linear:>14.4f} {avg_dict:>12.4f} {avg_speedup:>9.1f}x")
    print("=" * 62)

    print("\n📊 ANALYSIS")
    print("-" * 62)
    print(f"  Linear Search average : {avg_linear:.4f} µs")
    print(f"  Dict Lookup  average  : {avg_dict:.4f} µs")
    print(f"  Dictionary is ~{avg_speedup:.1f}x faster on average\n")

    print("📚 WHY IS DICTIONARY LOOKUP FASTER?")
    print("-" * 62)
    print(
        "  Linear search is O(n) — in the worst case it inspects every\n"
        "  record before finding the target (or confirming it's missing).\n"
        "  With 25 records that means up to 25 comparisons.\n\n"
        "  Dictionary lookup is O(1) (average). Python's dict is backed\n"
        "  by a hash table: the key (id) is hashed to an index, and the\n"
        "  value is fetched directly — no scanning needed, regardless of\n"
        "  how many records are stored.\n"
    )

    print("💡 OTHER DATA STRUCTURES / ALGORITHMS TO CONSIDER")
    print("-" * 62)
    print(
        "  1. Binary Search on a sorted list — O(log n). Faster than\n"
        "     linear search when a dict is not available, but the list\n"
        "     must be kept sorted by ID.\n\n"
        "  2. B-Tree / Indexed database column — O(log n) with very\n"
        "     low constant factors; used by SQL engines (e.g. PostgreSQL\n"
        "     index on transactions.id).\n\n"
        "  3. Trie or Inverted Index — useful if searching by sender\n"
        "     name or transaction type (partial text matching).\n\n"
        "  For this dataset size (< 1 000 records) the Python dict is\n"
        "  the clear winner — simple, O(1), and built-in.\n"
    )


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # Test with all 25 IDs (covers both best-case and worst-case positions)
    all_ids = [t["id"] for t in SAMPLE_TRANSACTIONS]
    random.shuffle(all_ids)   # randomise order so results aren't skewed
    compare_search_methods(all_ids)
