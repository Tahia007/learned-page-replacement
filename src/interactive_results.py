import pandas as pd
import plotly.express as px


def main():

    data = pd.read_csv(
        "results/final_results.csv"
    )

    before = data[
        [
            "Policy",
            "Before Shift Hit Ratio"
        ]
    ].copy()

    before["Phase"] = "Before Shift"

    before = before.rename(
        columns={
            "Before Shift Hit Ratio":
                "Hit Ratio"
        }
    )

    after = data[
        [
            "Policy",
            "After Shift Hit Ratio"
        ]
    ].copy()

    after["Phase"] = "After Shift"

    after = after.rename(
        columns={
            "After Shift Hit Ratio":
                "Hit Ratio"
        }
    )

    combined = pd.concat(
        [before, after]
    )

    figure = px.bar(
        combined,
        x="Policy",
        y="Hit Ratio",
        color="Phase",
        barmode="group",
        title="Hit Ratio Before and After Workload Shift"
    )

    figure.write_html(
        "results/interactive_results.html"
    )

    print(
        "Saved results/interactive_results.html"
    )


if __name__ == "__main__":
    main()