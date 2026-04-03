# 🤖 Job Alert Bot

A Python-based job monitoring system that scrapes job listings from local job sites and delivers real-time alerts to Telegram — filtering out the noise so only relevant tech roles come through.

> ⚠️ **This is a portfolio/showcase project.** The target job sites are intentionally not included. Cloning this repo will not produce a working bot without configuring your own scraping targets.

---

## What It Does

- Scrapes job listings from local job sites on a scheduled basis
- Filters results using keyword matching and fuzzy logic to surface relevant tech roles
- Tracks previously seen jobs in a database to avoid duplicate alerts
- Sends formatted job alerts to a personal Telegram chat via the Bot API

---

## How It Works

```
app.py  (entry point / scheduler)
  ├── scraper_site_1.py   ──┐
  ├── scraper_site_2.py   ──┼──► filter_jobs.py ──► job_tracker.py ──► bot.py ──► Telegram
  └── (more scrapers...)  ──┘                            │
                                                        db.py
```

| File | Role |
|---|---|
| `app.py` | Main entry point; orchestrates scraping, filtering, and alerting |
| `scraper_site_1.py` / `scraper_site_2.py` | Site-specific scrapers (targets withheld) |
| `filter_jobs.py` | Keyword + fuzzy matching to filter relevant tech jobs |
| `job_tracker.py` | Checks and records which jobs have already been sent |
| `db.py` | Database layer for job persistence |
| `bot.py` | Sends formatted alerts to Telegram |

---

## Filtering Logic

Jobs are matched against a keyword list covering roles like `python`, `backend`, `developer`, `devops`, `linux`, etc. Roles containing excluded terms like `sales`, `marketing`, or `graphic designer` are dropped. [RapidFuzz](https://github.com/rapidfuzz/RapidFuzz) is used for fuzzy partial matching to catch title variations.

---

## Tech Stack

- **Python** — core language
- **Requests / BeautifulSoup** — HTTP and HTML scraping
- **RapidFuzz** — fuzzy string matching for job title filtering
- **Telegram Bot API** — delivery channel for alerts
- **SQLite / DB layer** — deduplication and job state tracking
- **python-dotenv** — environment variable management

---

## Configuration

The bot is driven by environment variables stored in a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
```

A Telegram bot token can be obtained via [@BotFather](https://t.me/BotFather). The scrapers also require target URLs which are not part of this repository.

---

## Why It's Not Fully Runnable

The scraping targets are local job boards that I prefer not to make public. The scraper files (`scraper_site_1.py`, `scraper_site_2.py`) contain placeholder logic — without real URLs and site-specific HTML parsing, the scrapers will not return any data.

This repo is published to demonstrate the architecture, filtering approach, and Telegram integration — not as a plug-and-play tool.

---

## License

All rights reserved. This project is not open source. You may browse the code for reference, but it may not be reused, modified, or redistributed without permission.
