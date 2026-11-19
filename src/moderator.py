
from transformers import pipeline


class Moderator:
    def __init__(self):
        # Model 1: Detects general toxicity
        self.toxic_classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert"
        )

        # Model 2: Detects specific types of harmful content
        self.category_classifier = pipeline(
            "text-classification",
            model="unitary/unbiased-toxic-roberta",
            top_k=None
        )

        # Minimum general toxicity score
        self.toxicity_threshold = 0.80

        # Minimum score required for each moderation category
        self.category_thresholds = {
            "threat": 0.70,
            "sexual_explicit": 0.60,
            "insult": 0.70,
            "identity_attack": 0.55,
            "obscene": 0.70
        }

        # Minimum contextual toxicity for general toxic content
        self.context_toxicity_threshold = 0.30

    def moderate(self, text):
        # Run Toxic-BERT
        toxic_result = self.toxic_classifier(text)[0]
        toxicity_score = toxic_result["score"]

        # Run Toxic RoBERTa
        roberta_results = self.category_classifier(text)[0]

        # Store each category and its score in a dictionary
        scores = {
            result["label"]: result["score"]
            for result in roberta_results
        }

        # Default classification
        category = "normal"
        confidence = 1 - scores.get("toxicity", 0)

        # 1. Threat detection
        if scores.get("threat", 0) >= self.category_thresholds["threat"]:
            category = "threat"
            confidence = scores["threat"]

        # 2. Explicit sexual content
        elif (
            scores.get("sexual_explicit", 0)
            >= self.category_thresholds["sexual_explicit"]
        ):
            category = "sexual_content"
            confidence = scores["sexual_explicit"]

        # 3. Identity attack / hate speech
        # Checked before insults so identity-related hostility
        # can take priority when both categories score highly.
        elif (
            scores.get("identity_attack", 0)
            >= self.category_thresholds["identity_attack"]
        ):
            category = "hate_speech"
            confidence = scores["identity_attack"]

        # 4. Insult / harassment
        elif scores.get("insult", 0) >= self.category_thresholds["insult"]:
            category = "harassment"
            confidence = scores["insult"]

        # 5. Obscene language / profanity
        elif scores.get("obscene", 0) >= self.category_thresholds["obscene"]:
            category = "profanity"
            confidence = scores["obscene"]

        # 6. General toxic content
        elif (
            toxicity_score >= self.toxicity_threshold
            and scores.get("toxicity", 0)
            >= self.context_toxicity_threshold
        ):
            category = "toxic_content"
            confidence = scores["toxicity"]

        # Otherwise, classify the text as normal
        else:
            category = "normal"
            confidence = 1 - scores.get("toxicity", 0)

        # Return the moderation result
        return {
            "text": text,
            "category": category,
            "confidence": round(confidence, 4),
            "toxicity_score": round(toxicity_score, 4),
            "action": self.get_action(category)
        }

    def get_action(self, category):
        # Decide what action to take for each category
        if category == "normal":
            return "allow"

        elif category == "profanity":
            return "mask"

        elif category == "harassment":
            return "warn"

        elif category in ("threat", "hate_speech"):
            return "block"

        elif category == "sexual_content":
            return "mask"

        elif category == "toxic_content":
            return "flag"

        # Default action for any unrecognized category
        return "flag"
