import pandas as pd
import matplotlib.pyplot as plt

from learned_policy import LearnedPageReplacement
from workload import generate_shifted_workload


FRAME_COUNT = 8
PAGE_COUNT = 20
PHASE_LENGTH = 1000


def get_oracle_victim(
    trace,
    current_index,
    frames
):

    future = trace[current_index + 1:]

    next_use = {}

    for page in frames:

        if page in future:
            next_use[page] = future.index(page)

        else:
            next_use[page] = float("inf")

    return max(
        frames,
        key=lambda page: next_use[page]
    )


def main():

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

    learned = LearnedPageReplacement(
        FRAME_COUNT
    )

    learned.train(
        training_trace,
        FRAME_COUNT
    )

    result = learned.simulate(trace)

    frames = []

    rows = []

    for i, step in enumerate(result["history"]):

        page = step["page"]

        if page in frames:
            continue

        if len(frames) < FRAME_COUNT:

            frames.append(page)
            continue

        learned_victim = step["evicted"]

        oracle_victim = get_oracle_victim(
            trace,
            i,
            frames
        )

        confidence = step["confidence"]

        if confidence is not None:

            correct = (
                learned_victim == oracle_victim
            )

            rows.append({
                "Reference": i,
                "Confidence": confidence,
                "Correct": int(correct)
            })

        frames.remove(learned_victim)
        frames.append(page)

    data = pd.DataFrame(rows)

    data.to_csv(
        "results/confidence_analysis.csv",
        index=False
    )

    print("\nBonus Analysis")
    print("==========================")

    print(
        "Total decisions:",
        len(data)
    )

    if len(data) > 0:

        accuracy = data["Correct"].mean()

        print(
            "Overall oracle-match accuracy:",
            round(accuracy, 4)
        )

    plt.figure(figsize=(10, 6))

    correct = data[
        data["Correct"] == 1
    ]

    incorrect = data[
        data["Correct"] == 0
    ]

    plt.scatter(
        correct["Confidence"],
        correct["Correct"],
        label="Correct"
    )

    plt.scatter(
        incorrect["Confidence"],
        incorrect["Correct"],
        label="Incorrect"
    )

    plt.xlabel("Decision Confidence")
    plt.ylabel("Oracle Match (1 = Correct)")
    plt.title(
        "Learned Policy Confidence vs Oracle Match"
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        "results/confidence_vs_correctness.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()