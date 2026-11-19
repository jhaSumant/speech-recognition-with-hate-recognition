from transformers import pipeline

# Load pretrained toxicity detection model
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert"
)

# Context-sensitive test sentences
sentences = [
    "You are racist",
    "Stop being racist",
    "This is racist",
    "I am against racism",
    "We should not tolerate racist behavior",
    "He was explaining why racist language is harmful",
    "I hate people from that country",
    "People from that group should be killed"
]

# Test each sentence
for sentence in sentences:
    result = classifier(sentence)

    label = result[0]["label"]
    score = result[0]["score"] * 100

    print("Sentence:", sentence)
    print("Prediction:", label)
    print("Confidence:", round(score, 2), "%")
    print()