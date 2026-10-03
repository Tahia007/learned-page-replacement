from collections import deque


def fifo(reference_string, frame_count):
    frames = []
    queue = deque()

    hits = 0
    faults = 0
    history = []

    for page in reference_string:

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
                queue.append(page)

            else:
                evicted = queue.popleft()
                frames.remove(evicted)

                frames.append(page)
                queue.append(page)

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