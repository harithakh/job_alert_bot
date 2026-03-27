from rapidfuzz import fuzz

KEYWORDS = ["python", "software", "developer", "engineer", "backend",
    "frontend", "fullstack", "support", "it", "linux", "devops"]

EXCLUDED_WORDS = [
    "sales", "marketing"
]

def is_relevant(job):
    """
    Return True if the job title roughly matches any target tech keyword.
    Uses fuzzy partial matching to catch variations in titles.
    """
    title = job.get("title", "").lower()

    if not title:
        return False
    if any(word in title for word in EXCLUDED_WORDS):
        return False

    for keyword in KEYWORDS:
        if keyword in title:
            return True
        if fuzz.partial_ratio(keyword, title) >= 85:
            return True
    return False
