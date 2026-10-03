import pandas as pd
import matplotlib.pyplot as plt


def main():

    data = pd.read_csv(
        "results/final_results.csv"
    )

    policies = data["Policy"]

    before = data["Before Shift Hit Ratio"]

    after = data["After Shift Hit Ratio"]

    x = range(len(policies))

    width = 0.35

    plt.figure(figsize=(10, 6))

    plt.bar(
        [i - width / 2 for i in x],
        before,
        width=width,
        label="Before Shift"
    )

    plt.bar(
        [i + width / 2 for i in x],
        after,
        width=width,
        label="After Shift"
    )

    plt.xticks(
        list(x),
        policies
    )

    plt.ylabel("Hit Ratio")

    plt.xlabel("Policy")

    plt.title(
        "Hit Ratio Before and After Workload Shift"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        "results/hit_ratio_comparison.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    main()