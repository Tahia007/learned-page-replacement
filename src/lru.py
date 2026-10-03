def lru(reference_string, frame_count):
    frames = []
    last_used = {}

    hits = 0
    faults = 0
    history = []

    for time, page in enumerate(reference_string):

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
                least_recent_page = min(
                    frames,
                    key=lambda p: last_used.get(p, -1)
                )

                evicted = least_recent_page

                frames.remove(least_recent_page)
                frames.append(page)

        last_used[page] = time

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