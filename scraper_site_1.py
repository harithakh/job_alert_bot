import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from filter_jobs import is_relevant
from job_tracker import process_jobs

load_dotenv()

JOB_SITE_URL_1 = f"{os.getenv('JOB_SITE_URL_1')}"

def scrape_jobs_site_1():

    try:
        response = requests.get(JOB_SITE_URL_1)
        print(f"\nSite 1 response code: {response.status_code}")

    except requests.exceptions.Timeout:
        print(f"Timeout: {JOB_SITE_URL_1}")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    all_jobs_first_page = soup.find_all("article")

    jobs = []

    for article in all_jobs_first_page:

        # job url
        url_tag = article.select_one("a")
        job_url = url_tag["href"] if url_tag else ""

        #job title
        title = article.select_one("h3.jc-title")
        job_title = title.get_text(strip=True) if title else ""

        # company name
        company = article.select_one("span.jc-company")
        company_name = company.get_text(strip=True) if company else ""

        # location
        location_span = article.select_one("span.la")
        if location_span:
            #  Remove the img tag, then grab the remaining text
            img = location_span.find("img")
            if img:
                img.decompose()
            location = location_span.get_text(strip=True)
        else:
            location = ""

        # date and time
        time_tag = article.select_one("time.time-posted")
        posted_date = time_tag["datetime"].split("T")[0] if time_tag else None

        jobs.append({
            "title": job_title,
            "company": company_name,
            "location": location,
            "url": job_url,
            "posted_date": posted_date,})

    print(f"Site 1 total job count: {len(jobs)}")

    most_applied_jobs_removed = [job for job in jobs if job.get("posted_date")]
    relevent_jobs = [job for job in most_applied_jobs_removed if is_relevant(job)]

    new_jobs = process_jobs(relevent_jobs) # remove duplicates

    print(f"Site 1: Ready to send alerts for {len(new_jobs)} jobs\n")

    return new_jobs
