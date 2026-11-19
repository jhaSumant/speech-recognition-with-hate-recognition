class Moderator:
    def __init__(self):
        self.categories = {
            "profanity": ["fuck", "shit", "bitch"],
            "hate_speech": ["racist", "kill all"],
            "threat": ["i will hurt you", "i will kill you"],
            "harassment": ["idiot", "stupid"],
            "sexual_content": ["sex"],
            "normal": []
        }

    def moderate(self, text):
        text_lower = text.lower()

        # Basic context check for threat-related speech
        if "kill" in text_lower and "you" in text_lower:
            return {
                "text": text,
                "category": "threat",
                "confidence": 0.90,
                "action": self.get_action("threat")
            }

        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return {
                        "text": text,
                        "category": category,
                        "confidence": 0.90,
                        "action": self.get_action(category)
                    }

        return {
            "text": text,
            "category": "normal",
            "confidence": 0.95,
            "action": self.get_action("normal")
        }

    def get_action(self, category):
        if category == "normal":
            return "allow"

        elif category == "profanity":
            return "mask"

        elif category == "harassment":
            return "warn"

        elif category == "threat":
            return "block"

        elif category == "hate_speech":
            return "block"

        elif category == "sexual_content":
            return "mask"

        return "flag"