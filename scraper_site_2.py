import requests
import os
import json
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from filter_jobs import is_relevant
from job_tracker import process_jobs


load_dotenv()

JOB_SITE_URL_2 = os.getenv('JOB_SITE_URL_2')

def scrape_jobs_site_2():

    response = requests.get(JOB_SITE_URL_2)

    print(response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    job_ads_SE = soup.find_all('div', class_='job-ad live-search-list')

    jobs = []

    # print(job_ads)
    for job in job_ads_SE:

        link_tag = job.find("a")
        job_link = f"https://www.topjobs.lk{link_tag.get("href")}" if link_tag else None
        job_title = (link_tag.get_text(strip=True) or "") if link_tag else ""

        company = job.find("a", class_="job-owner no-link")
        company_name = (company.get_text(strip=True) or "") if company else ""

        location_span = job.find("span", class_="location-area single-location")
        location = (location_span.get_text(strip=True) or "") if location_span else ""

        start_date_span = job.find("span", class_="closing-date")
        posted_date = (start_date_span.get("data-startingdate") or "") if start_date_span else ""

        jobs.append({
            "title": job_title,
            "company": company_name,
            "location": location,
            "link": job_link,
            "posted_date": posted_date,})


    relevent_jobs = [job for job in jobs if is_relevant(job)]
    new_jobs = process_jobs(relevent_jobs) # remove duplicates

    return new_jobs


