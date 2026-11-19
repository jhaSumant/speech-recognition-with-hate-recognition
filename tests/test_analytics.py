from src.analytics import ModerationAnalytics


analytics = ModerationAnalytics()

print("Total events:", analytics.get_total_events())

print("Category counts:", analytics.get_category_counts())

print(
    "Average confidence:",
    round(analytics.get_average_confidence() * 100, 2),
    "%"
)

print("\nRecent events:")

recent_events = analytics.get_recent_events()

for event in recent_events:
    print(event)

print("\nEvents with confidence >= 90%:")

very_high_confidence_events = analytics.get_high_confidence_events(0.90)

print("Number of events:", len(very_high_confidence_events))