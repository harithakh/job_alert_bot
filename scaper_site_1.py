import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

JOB_SITE_URL_1 = f"{os.getenv('JOB_SITE_URL_1')}"

# print(response.status_code)

def scrape_jobs_site_1():

    response = requests.get(JOB_SITE_URL_1)

    soup = BeautifulSoup(response.text, "html.parser")

    all_jobs_first_page = soup.find_all("article")

    jobs = []

    for article in all_jobs_first_page:

        # job link
        link_tag = article.select_one("a.job-record-link")
        job_link = link_tag["href"] if link_tag else None

        #job title
        title = article.select_one("span.job-title")
        job_title = title.get_text(strip=True) if title else None

        # company name
        company = article.select_one("span.jc-company")
        company_name = company.get_text(strip=True) if company else None

        # location
        location_span = article.select_one("div.job-record-location span.la")
        if location_span:
            #  Remove the img tag, then grab the remaining text
            img = location_span.find("img")
            if img:
                img.decompose()
            location = location_span.get_text(strip=True)
        else:
            location = None

        # date and time
        time_tag = article.select_one("time.time-posted")
        posted_date = time_tag["datetime"].split("T")[0] if time_tag else None
        posted_time = time_tag["datetime"].split("T")[1] if time_tag else None

        jobs.append({
            "title": job_title,
            "company": company_name,
            "location": location,
            "link": job_link,
            "posted_date": posted_date,
            "posted_time": posted_time,})

    return jobs
