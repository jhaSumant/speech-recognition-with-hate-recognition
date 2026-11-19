from src.analytics import ModerationAnalytics


analytics = ModerationAnalytics()


print("=== ANALYTICS TEST ===")

print("\nTotal events:")
print(analytics.get_total_events())


print("\nCategory counts:")
print(analytics.get_category_counts())


print("\nAverage confidence:")
print(
    round(analytics.get_average_confidence() * 100, 2),
    "%"
)


print("\nRecent events:")
recent_events = analytics.get_recent_events()

for event in recent_events:
    print(event)


print("\nHigh-confidence events:")
high_confidence_events = analytics.get_high_confidence_events()

print(
    "Number of events:",
    len(high_confidence_events)
)


print("\nComplete summary:")
summary = analytics.get_summary()

print(summary)