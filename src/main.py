import os

from fifo import fifo
from lru import lru
from optimal import optimal

from workload import generate_shifted_workload
from evaluation import create_results_table

from learned_policy import LearnedPageReplacement


FRAME_COUNT = 8
PAGE_COUNT = 20
PHASE_LENGTH = 1000

TRAINING_LENGTH = 2000


def main():

    print("Generating test workload...")

    test_trace = generate_shifted_workload(
        phase_length=PHASE_LENGTH,
        page_count=PAGE_COUNT,
        seed=42
    )

    print("Test references:", len(test_trace))

    print("\nGenerating training workload...")

    training_trace = generate_shifted_workload(
        phase_length=TRAINING_LENGTH // 2,
        page_count=PAGE_COUNT,
        seed=100
    )

    print("Training references:", len(training_trace))

    algorithms = {
        "FIFO": fifo,
        "LRU": lru,
        "Optimal": optimal
    }

    results = {}

    print("\nRunning classical algorithms...")

    for name, algorithm in algorithms.items():

        print("Running", name)

        results[name] = algorithm(
            test_trace,
            FRAME_COUNT
        )

    print("\nTraining learned policy...")

    learned_policy = LearnedPageReplacement(
        FRAME_COUNT
    )

    learned_policy.train(
        training_trace,
        FRAME_COUNT
    )

    print("Training complete.")

    print("\nRunning learned policy...")

    results["Learned"] = learned_policy.simulate(
        test_trace
    )

    table = create_results_table(
        results,
        PHASE_LENGTH
    )

    os.makedirs("results", exist_ok=True)

    table.to_csv(
        "results/final_results.csv",
        index=False
    )

    print("\n========================================")
    print("FINAL RESULTS")
    print("========================================")

    print(table.to_string(index=False))

    print("\nSaved:")
    print("results/final_results.csv")


if __name__ == "__main__":
    main()