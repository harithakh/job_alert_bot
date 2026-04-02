import time

from scraper_site_1 import scrape_jobs_site_1
from scraper_site_2 import scrape_jobs_site_2

from bot import send_job_alert

if __name__ == "__main__":

    jobs = scrape_jobs_site_1() + scrape_jobs_site_2()

    for job in jobs:
        send_job_alert(job)
        print(f"Sent job alertt for: {job['title']}")
        time.sleep(1)
