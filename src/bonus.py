def generate_explanation(
    evicted_page,
    confidence,
    recency,
    frequency
):

    if confidence is None:

        return (
            "No eviction decision was needed "
            "because the page was already in memory "
            "or there was an empty frame."
        )

    if recency > 5 and frequency <= 2:

        explanation = (
            f"Page {evicted_page} was selected because "
            "it has not been used recently and has a "
            "low recent access frequency."
        )

    elif recency > 5:

        explanation = (
            f"Page {evicted_page} was selected mainly "
            "because it has not been used recently."
        )

    elif frequency <= 2:

        explanation = (
            f"Page {evicted_page} was selected because "
            "its recent access frequency is low."
        )

    else:

        explanation = (
            f"Page {evicted_page} was selected based on "
            "the learned model's feature pattern."
        )

    if confidence >= 0.50:

        confidence_text = "High decision confidence."

    elif confidence >= 0.20:

        confidence_text = "Medium decision confidence."

    else:

        confidence_text = "Low decision confidence."

    return explanation + " " + confidence_text