import random


def generate_locality_workload(length, page_count):

    reference_string = []

    hot_pages = list(range(1, 7))

    for _ in range(length):

        if random.random() < 0.85:
            page = random.choice(hot_pages)

        else:
            page = random.randint(1, page_count)

        reference_string.append(page)

    return reference_string


def generate_random_bursty_workload(length, page_count):

    reference_string = []

    burst_pages = None

    for _ in range(length):

        if random.random() < 0.25:
            burst_pages = random.sample(
                range(1, page_count + 1),
                4
            )

        if burst_pages and random.random() < 0.70:
            page = random.choice(burst_pages)

        else:
            page = random.randint(1, page_count)

        reference_string.append(page)

    return reference_string


def generate_shifted_workload(
    phase_length=1000,
    page_count=20,
    seed=42
):

    random.seed(seed)

    phase1 = generate_locality_workload(
        phase_length,
        page_count
    )

    phase2 = generate_random_bursty_workload(
        phase_length,
        page_count
    )

    return phase1 + phase2