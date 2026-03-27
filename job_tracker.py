import json
import os
from datetime import datetime,timedelta

SEEN_JOBS_FILE = "seen_jobs.json"
EXPIRY_DAYS = 3

def load_saved_jobs():
    if not os.path.exists(SEEN_JOBS_FILE):
        return {}
    with open(SEEN_JOBS_FILE, "r") as f:
        return json.load(f) # Convert json file into a Python object

def save_seen_jobs(seen_jobs):
    with open(SEEN_JOBS_FILE, "w") as f:
        json.dump(seen_jobs, f)

def clean_old_jobs(seen_jobs):
    # Clear jobs those older than (EXPIRY_DAYS)days
    cutoff_date = datetime.now() - timedelta(days=EXPIRY_DAYS)

    cleaned = []

    for job in seen_jobs:
        try:
            job_date = datetime.strptime(job["posted_date"], "%Y-%m-%d").date()

            if job_date > cutoff_date:
                cleaned.append(job)
        except Exception:
            cleaned.append(job)
    return cleaned

def process_jobs(jobs):
    # Return only new jobs from scrapped jobs
    seen_jobs = clean_old_jobs(load_saved_jobs())

    new_jobs = []
    for job in jobs:
        if job["link"] not in seen_jobs:
            seen_jobs.append(job)
            new_jobs.append(job)

    save_seen_jobs(seen_jobs)

    return new_jobs
