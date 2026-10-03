from fifo import fifo
from lru import lru
from optimal import optimal
from mru import mru


reference_string = [
    1, 2, 3, 1, 4, 5, 2, 1, 3, 4
]

frame_count = 3


algorithms = {
    "FIFO": fifo,
    "LRU": lru,
    "Optimal": optimal,
    "MRU": mru
}


for name, algorithm in algorithms.items():

    result = algorithm(
        reference_string,
        frame_count
    )

    print("\n" + "=" * 40)
    print(name)
    print("=" * 40)

    print("Hits:", result["hits"])
    print("Page Faults:", result["faults"])
    print("Hit Ratio:", round(result["hit_ratio"], 4))