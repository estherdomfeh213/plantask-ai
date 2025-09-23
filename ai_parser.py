import re
from datetime import datetime, timedelta

def parse_task_input(user_input):
    # Default values
    duration = 60
    priority = "medium"
    deadline = datetime.today().strftime("%Y-%m-%d")

    # Extract priority
    if "high priority" in user_input.lower():
        priority = "high"
    elif "low priority" in user_input.lower():
        priority = "low"

    # Extract duration (e.g., "2 hours" or "30 minutes")
    match = re.search(r"(\d+)\s*(hour|hours|minute|minutes)", user_input.lower())
    if match:
        value, unit = int(match.group(1)), match.group(2)
        if "hour" in unit:
            duration = value * 60
        else:
            duration = value

    # Extract deadline (e.g., "tomorrow" or "today")
    if "tomorrow" in user_input.lower():
        deadline = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "today" in user_input.lower():
        deadline = datetime.today().strftime("%Y-%m-%d")

    # Title = cleaned sentence without keywords
    title = re.sub(r"(today|tomorrow|high priority|low priority|\d+\s*(hours?|minutes?))", "", user_input, flags=re.IGNORECASE).strip()

    return {
        "title": title if title else "Untitled Task",
        "duration": duration,
        "priority": priority,
        "deadline": deadline
    }

# Demo
if __name__ == "__main__":
    print(parse_task_input("Finish essay tomorrow at 3pm, high priority, 2 hours"))
