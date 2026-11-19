
from src.moderator import Moderator


moderator = Moderator()


test_cases = [
    {
        "text": "Hello, how are you?",
        "expected_category": "normal",
        "expected_action": "allow"
    },
    {
        "text": "You are a stupid idiot",
        "expected_category": "harassment",
        "expected_action": "warn"
    },
    {
        "text": "I will hurt you",
        "expected_category": "threat",
        "expected_action": "block"
    },
    {
        "text": "I hate people from that country",
        "expected_category": "hate_speech",
        "expected_action": "block"
    },
    {
        "text": "I am against racism",
        "expected_category": "normal",
        "expected_action": "allow"
    },
    {
        "text": "Have a wonderful day!",
        "expected_category": "normal",
        "expected_action": "allow"
    },
    {
        "text": "You are an idiot",
        "expected_category": "harassment",
        "expected_action": "warn"
    },
    {
        "text": "I will kill you",
        "expected_category": "threat",
        "expected_action": "block"
    },
    {
        "text": "We should not tolerate racist behavior",
        "expected_category": "normal",
        "expected_action": "allow"
    },
    {
        "text": "People from that group should be killed",
        "expected_category": "hate_speech",
        "expected_action": "block"
    },
    {
        "text": "I will hurt you if you come here",
        "expected_category": "threat",
        "expected_action": "block"
    },
    {
        "text": "That group deserves respect",
        "expected_category": "normal",
        "expected_action": "allow"
    },
    {
        "text": "People of that religion are disgusting",
        "expected_category": "hate_speech",
        "expected_action": "block"
    },
    {
        "text": "I disagree with your opinion",
        "expected_category": "normal",
        "expected_action": "allow"
    }
]


passed = 0

for test in test_cases:
    result = moderator.moderate(test["text"])

    category_correct = (
        result["category"] == test["expected_category"]
    )
    action_correct = (
        result["action"] == test["expected_action"]
    )

    if category_correct and action_correct:
        passed += 1
        status = "PASS"
    else:
        status = "FAIL"

    print(f"\nTest: {test['text']}")
    print(f"Expected category: {test['expected_category']}")
    print(f"Actual category:   {result['category']}")
    print(f"Expected action:   {test['expected_action']}")
    print(f"Actual action:     {result['action']}")
    print(f"Confidence:        {result['confidence']:.2%}")
    print(f"Result: {status}")


total = len(test_cases)
accuracy = (passed / total) * 100

print("\n========== EVALUATION SUMMARY ==========")
print(f"Tests passed: {passed}/{total}")
print(f"Tests failed: {total - passed}")
print(f"Exact-match accuracy: {accuracy:.2f}%")
print("========================================")
