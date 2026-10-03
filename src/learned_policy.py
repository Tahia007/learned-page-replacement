from collections import Counter

from sklearn.tree import DecisionTreeClassifier


class LearnedPageReplacement:

    def __init__(self, frame_count):

        self.frame_count = frame_count

        self.model = DecisionTreeClassifier(
            max_depth=4,
            random_state=42
        )

        self.trained = False

    def build_features(
        self,
        page,
        current_time,
        last_used,
        frequency
    ):

        if page in last_used:
            recency = current_time - last_used[page]
        else:
            recency = current_time + 1

        recent_frequency = frequency.get(page, 0)

        age = recency

        return [
            recency,
            recent_frequency,
            age
        ]

    def train(
        self,
        reference_string,
        frame_count
    ):

        X = []
        y = []

        frames = []
        last_used = {}
        frequency = Counter()

        for current_time, page in enumerate(reference_string):

            frequency[page] += 1

            if page not in frames:

                if len(frames) < frame_count:

                    frames.append(page)

                else:

                    future = reference_string[
                        current_time + 1:
                    ]

                    candidates = []

                    for candidate in frames:

                        if candidate in future:

                            next_use = future.index(candidate)

                        else:

                            next_use = float("inf")

                        features = self.build_features(
                            candidate,
                            current_time,
                            last_used,
                            frequency
                        )

                        candidates.append(
                            (candidate, features, next_use)
                        )

                    best_candidate = max(
                        candidates,
                        key=lambda x: x[2]
                    )

                    for candidate, features, next_use in candidates:

                        X.append(features)

                        if candidate == best_candidate[0]:
                            y.append(1)
                        else:
                            y.append(0)

                    frames.remove(best_candidate[0])
                    frames.append(page)

            last_used[page] = current_time

        if len(X) > 0:

            self.model.fit(X, y)
            self.trained = True

    def choose_victim(
        self,
        frames,
        current_time,
        last_used,
        frequency
    ):

        candidate_features = []

        for page in frames:

            features = self.build_features(
                page,
                current_time,
                last_used,
                frequency
            )

            candidate_features.append(
                (page, features)
            )

        if not self.trained:

            return frames[0], 0.0

        best_page = None
        best_score = -1
        second_score = -1

        for page, features in candidate_features:

            probabilities = self.model.predict_proba(
                [features]
            )[0]

            class_index = list(
                self.model.classes_
            ).index(1)

            score = probabilities[class_index]

            if score > best_score:

                second_score = best_score
                best_score = score
                best_page = page

            elif score > second_score:

                second_score = score

        confidence = best_score - max(
            second_score,
            0
        )

        return best_page, confidence

    def simulate(
        self,
        reference_string
    ):

        frames = []

        last_used = {}
        frequency = Counter()

        hits = 0
        faults = 0

        history = []

        for current_time, page in enumerate(reference_string):

            frequency[page] += 1

            if page in frames:

                hits += 1

                result = "Hit"
                evicted = None
                confidence = None

            else:

                faults += 1

                result = "Fault"
                evicted = None

                if len(frames) < self.frame_count:

                    frames.append(page)
                    confidence = None

                else:

                    evicted, confidence = self.choose_victim(
                        frames,
                        current_time,
                        last_used,
                        frequency
                    )

                    frames.remove(evicted)
                    frames.append(page)

            last_used[page] = current_time

            history.append({

                "page": page,

                "frames": frames.copy(),

                "result": result,

                "evicted": evicted,

                "confidence": confidence
            })

        hit_ratio = hits / len(reference_string)

        return {

            "hits": hits,

            "faults": faults,

            "hit_ratio": hit_ratio,

            "history": history
        }