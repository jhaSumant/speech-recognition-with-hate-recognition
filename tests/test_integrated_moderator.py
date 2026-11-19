from src.moderator import Moderator


# Create the integrated moderator
moderator = Moderator()


# Test sentences
sentences = [
    "Hello, how are you?",
    "You are stupid",
    "I will hurt you",
    "This is racist",
    "I am against racism",
    "I hate people from that country",
    "You are a fucking idiot"
]


# Test each sentence
for sentence in sentences:

    result = moderator.moderate(sentence)

    print("Sentence:", sentence)
    print("Category:", result["category"])
    print("Confidence:", round(result["confidence"] * 100, 2), "%")
    print("Action:", result["action"])
    print("-" * 50)

