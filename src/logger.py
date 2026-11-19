import csv
import os
from datetime import datetime


class ModerationLogger:
    def __init__(self, filename="logs/moderation_log.csv"):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

    def log_event(self, text, category, confidence, action):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file_exists = os.path.exists(self.filename)

        with open(self.filename, "a", newline="") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "text",
                    "category",
                    "confidence",
                    "action"
                ])

            writer.writerow([
                timestamp,
                text,
                category,
                confidence,
                action
            ])