from src.moderator import Moderator

m = Moderator()
text = "you are fat"

print("\n--- Toxic-BERT ---")
print(m.toxic_classifier(text)[0])

print("\n--- Toxic-RoBERTa category scores ---")
for result in m.category_classifier(text)[0]:
    print(f"{result['label']}: {result['score']:.4f}")

print("\n--- Final moderation result ---")
print(m.moderate(text))
