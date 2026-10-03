def optimal(reference_string, frame_count):
    frames = []

    hits = 0
    faults = 0
    history = []

    for current_index, page in enumerate(reference_string):

        if page in frames:
            hits += 1
            result = "Hit"
            evicted = None

        else:
            faults += 1
            result = "Fault"
            evicted = None

            if len(frames) < frame_count:
                frames.append(page)

            else:
                future = reference_string[current_index + 1:]

                next_use = {}

                for candidate in frames:

                    if candidate in future:
                        next_use[candidate] = future.index(candidate)

                    else:
                        next_use[candidate] = float("inf")

                evicted = max(
                    frames,
                    key=lambda p: next_use[p]
                )

                frames.remove(evicted)
                frames.append(page)

        history.append({
            "page": page,
            "frames": frames.copy(),
            "result": result,
            "evicted": evicted
        })

    hit_ratio = hits / len(reference_string)

    return {
        "hits": hits,
        "faults": faults,
        "hit_ratio": hit_ratio,
        "history": history
    }