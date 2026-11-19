import csv


class ModerationAnalytics:

    def __init__(self, filename="logs/moderation_log.csv"):
        self.filename = filename

    def load_logs(self):
        try:
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                logs = list(reader)

                if not logs:
                    return []

                return logs

        except FileNotFoundError:
            return []

    def get_total_events(self):
        logs = self.load_logs()
        return len(logs)

    def get_category_counts(self):
        logs = self.load_logs()

        category_counts = {}

        for log in logs:
            category = log["category"]

            if category not in category_counts:
                category_counts[category] = 0

            category_counts[category] += 1

        return category_counts

    def get_average_confidence(self):
        logs = self.load_logs()

        if not logs:
            return 0

        total_confidence = 0
        valid_events = 0

        for log in logs:
            try:
                confidence = float(log["confidence"])
                total_confidence += confidence
                valid_events += 1

            except (ValueError, TypeError):
                continue

        if valid_events == 0:
            return 0

        return total_confidence / valid_events

    def get_recent_events(self, limit=5):
        logs = self.load_logs()
        return logs[-limit:]

    def get_high_confidence_events(self, threshold=0.80):
        logs = self.load_logs()

        high_confidence_events = []

        for log in logs:
            try:
                confidence = float(log["confidence"])

                if confidence >= threshold:
                    high_confidence_events.append(log)

            except (ValueError, TypeError):
                continue

        return high_confidence_events

    def get_summary(self):
        total_events = self.get_total_events()
        category_counts = self.get_category_counts()
        average_confidence = self.get_average_confidence()
        normal_events = category_counts.get("normal", 0)
        moderated_events = total_events - normal_events
        high_confidence_events = self.get_high_confidence_events()

        return {
            "total_events": total_events,
            "category_counts": category_counts,
            "average_confidence": average_confidence,
            "normal_events": normal_events,
            "moderated_events": moderated_events,
            "high_confidence_events": len(high_confidence_events)
        }