import matplotlib.pyplot as plt

from fifo import fifo
from lru import lru
from optimal import optimal

from learned_policy import LearnedPageReplacement
from workload import generate_shifted_workload


FRAME_COUNT = 8
PAGE_COUNT = 20
PHASE_LENGTH = 1000


def main():

    print("Generating test workload...")

    trace = generate_shifted_workload(
        phase_length=PHASE_LENGTH,
        page_count=PAGE_COUNT,
        seed=42
    )

    training_trace = generate_shifted_workload(
        phase_length=1000,
        page_count=PAGE_COUNT,
        seed=100
    )

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
            trace,
            FRAME_COUNT
        )

    print("\nTraining Learned Policy...")

    learned = LearnedPageReplacement(
        FRAME_COUNT
    )

    learned.train(
        training_trace,
        FRAME_COUNT
    )

    print("Running Learned Policy...")

    results["Learned"] = learned.simulate(
        trace
    )

    plt.figure(figsize=(12, 6))

    window = 50

    for name, result in results.items():

        fault_values = [
            1 if step["result"] == "Fault" else 0
            for step in result["history"]
        ]

        rolling_fault_rate = []

        for i in range(len(fault_values)):

            start = max(
                0,
                i - window + 1
            )

            rate = sum(
                fault_values[start:i + 1]
            ) / (i - start + 1)

            rolling_fault_rate.append(rate)

        plt.plot(
            rolling_fault_rate,
            label=name
        )

    plt.axvline(
        PHASE_LENGTH,
        linestyle="--",
        label="Workload Shift"
    )

    plt.xlabel("Reference Number")

    plt.ylabel("Page Fault Rate")

    plt.title(
        "Page Fault Rate Before and After Workload Shift"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "results/page_fault_shift.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()