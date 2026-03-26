from scaper_site_1 import scrape_jobs_site_1
from bot import send_job_alert

if __name__ == "__main__":
    jobs = scrape_jobs_site_1()

    for job in jobs:
        send_job_alert(job)
        print(f"Sent job alertt for: {job['title']}")

    # send_job_alert(jobs[0])
    # print(f"Sent job alertt for:{jobs[0]}")
