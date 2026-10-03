import pandas as pd


def calculate_phase_metrics(result, phase_length):

    history = result["history"]

    phase1 = history[:phase_length]
    phase2 = history[phase_length:]

    phase1_faults = sum(
        1 for step in phase1
        if step["result"] == "Fault"
    )

    phase2_faults = sum(
        1 for step in phase2
        if step["result"] == "Fault"
    )

    phase1_hits = len(phase1) - phase1_faults
    phase2_hits = len(phase2) - phase2_faults

    return {
        "before_faults": phase1_faults,
        "after_faults": phase2_faults,

        "before_hit_ratio":
            phase1_hits / len(phase1),

        "after_hit_ratio":
            phase2_hits / len(phase2),

        "total_faults":
            phase1_faults + phase2_faults
    }


def create_results_table(results, phase_length):

    rows = []

    for name, result in results.items():

        metrics = calculate_phase_metrics(
            result,
            phase_length
        )

        rows.append({

            "Policy": name,

            "Before Shift Faults":
                metrics["before_faults"],

            "After Shift Faults":
                metrics["after_faults"],

            "Before Shift Hit Ratio":
                metrics["before_hit_ratio"],

            "After Shift Hit Ratio":
                metrics["after_hit_ratio"],

            "Total Faults":
                metrics["total_faults"]
        })

    return pd.DataFrame(rows)