import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_job_alert(job):
    text = f"""
    <b>New Job Alert</b>

    <b>Title:</b> {job['title']}
    <b>Company:</b> {job['company']}
    <b>Location:</b> {job['location']}
    <b>Posted:</b> {job['posted_date']}

    <a href="{job['url']}">Link</a>
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    response = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text":text,
        "parse_mode": "HTML"
        })
    return response.ok
