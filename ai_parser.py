import re
import spacy
from datetime import datetime, timedelta

# Load small English model
nlp = spacy.load("en_core_web_sm")

def parse_task_input(user_input):
    doc = nlp(user_input)

    # Defaults
    title = user_input
    duration = 60
    priority = "medium"
    deadline = datetime.today().strftime("%Y-%m-%d")

    text_lower = user_input.lower()

    # --- Priority ---
    if "high" in text_lower:
        priority = "high"
    elif "low" in text_lower:
        priority = "low"

    # --- Duration (regex fallback) ---
    match = re.search(r"(\d+)\s*(hour|hours|minute|minutes)", text_lower)
    if match:
        value, unit = int(match.group(1)), match.group(2)
        duration = value * 60 if "hour" in unit else value

    # --- Deadline (explicit before NLP) ---
    if "tomorrow" in text_lower:
        deadline = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "today" in text_lower:
        deadline = datetime.today().strftime("%Y-%m-%d")
    else:
        # --- Try spaCy DATE entities ---
        for ent in doc.ents:
            if ent.label_ in ["DATE", "TIME"]:
                try:
                    parsed = datetime.strptime(ent.text, "%B %d")  # e.g., "September 23"
                    deadline = parsed.replace(year=datetime.today().year).strftime("%Y-%m-%d")
                except:
                    pass

    # --- Title cleanup ---
    title = re.sub(
        r"(today|tomorrow|high priority|low priority|\d+\s*(hours?|minutes?))",
        "",
        user_input,
        flags=re.IGNORECASE,
    ).strip()

    return {
        "title": title if title else "Untitled Task",
        "duration": duration,
        "priority": priority,
        "deadline": deadline,
    }

# Demo
if __name__ == "__main__":
    print(parse_task_input("Write essay tomorrow, high priority, 2 hours"))
