from transformers import pipeline
from src.moderator import Moderator

# Load the pretrained toxicity model
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

# Create our existing keyword moderator
moderator = Moderator()

# Sentences for comparison
sentences = [
    "Hello, how are you?",
    "You are stupid",
    "I will hurt you",
    "This is racist",
    "I am against racism",
    "Stop being racist",
    "I hate people from that country",
    "You are a fucking idiot"
]

# Compare both systems
for sentence in sentences:

    old_result = moderator.moderate(sentence)
    ai_result = classifier(sentence)[0]

    print("Sentence:", sentence)

    print("Keyword Moderator:")
    print("Category:", old_result["category"])
    print("Confidence:", old_result["confidence"])

    print("Toxic-BERT:")
    print("Prediction:", ai_result["label"])
    print("Confidence:", round(ai_result["score"] * 100, 2), "%")

    print("-" * 50)
