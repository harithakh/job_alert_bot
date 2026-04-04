import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from filter_jobs import is_relevant
from job_tracker import process_jobs
from db import init_db, insert_job, job_exists

load_dotenv()
init_db()

colombo_tz = timezone(timedelta(hours=5, minutes=30))
today = datetime.now(colombo_tz).date().isoformat()

JOB_SITE_URL_2_SE = os.getenv('JOB_SITE_URL_2_SE')
JOB_SITE_URL_2_IT = os.getenv('JOB_SITE_URL_2_IT')

def scrape_jobs_site_2():

    se_job_list = scrape_jobs(JOB_SITE_URL_2_SE, "SE") or []
    it_job_list = scrape_jobs(JOB_SITE_URL_2_IT, "IT") or []

    # print(f"se job list\n{se_job_list}")
    # print(f"it job list\n{it_job_list}")

    jobs = se_job_list + it_job_list

    # save to database
    for job in jobs:
        if not job_exists(job['reference_no'], today):
            insert_job(**job)

    relevent_jobs = [job for job in jobs if is_relevant(job)]
    print(f"Relevent jobs count: {len(relevent_jobs)}")

    # remove duplicates
    new_jobs = process_jobs(relevent_jobs)
    print(f"Site 2: Ready to send alerts for {len(new_jobs)} jobs\n")
    return new_jobs

def scrape_jobs(job_page_url, category):

    try:
        response = requests.get(job_page_url, timeout=10)
        print(f"{category} page response code: {response.status_code}")
        response.raise_for_status() #catches bad responses
    except requests.exceptions.Timeout:
        print(f"Timeout: {job_page_url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    job_ads = soup.find_all('div', class_='job-ad live-search-list')

    scraped_jobs = []

    for job in job_ads:
        url_tag = job.find("a")
        job_url = f"https://www.topjobs.lk{url_tag.get("href")}" if url_tag else None
        job_title = (url_tag.get_text(strip=True) or "") if url_tag else ""

        company = job.find("a", class_="job-owner no-link")
        company_name = (company.get_text(strip=True) or "") if company else ""

        location_span = job.find("span", class_="location-area single-location")
        location = (location_span.get_text(strip=True) or "") if location_span else ""

        start_date_span = job.find("span", class_="closing-date")
        posted_date = (start_date_span.get("data-startingdate") or "") if start_date_span else ""

        ref = job.find("span", class_="job-ref-value")
        job_ref = (ref.get_text(strip=True) or "") if ref else ""

        if posted_date == today:
            scraped_jobs.append({
                "title": job_title,
                "company": company_name,
                "location": location,
                "url": job_url,
                "posted_date": posted_date,
                "category" : category,
                "reference_no": job_ref})

    print(f"Number of {category} jobs today: {len(scraped_jobs)}\n")

    return scraped_jobs
