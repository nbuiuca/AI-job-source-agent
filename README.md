# Part 2 — AI Job Source Agent

This project implements **Part 2: AI Job Source Agent**.

Given:
- **company name**
- **company website URL**

The script will:
1) find the **career page URL**
2) extract **one open position (job posting) URL**
3) print the result in the required format:

`company name, career page URL, open position URL`

---
## Libraries Used (why)

- **requests**: sends HTTP requests to download page HTML.
- **BeautifulSoup (bs4) + lxml**: parses the raw HTML and lets the script extract links 
- **urljoin**: converts relative links (like `/careers`) into absolute URLs based on the current page URL.
- **urlparse**: extracts the hostname (domain) from the input URL so the script can quickly detect known job-board hosts (e.g., Greenhouse/Lever) and treat them as career pages.
- **re (regex)**: matches common job-posting URL patterns for ATS platforms (Greenhouse/Workday/Workable/iCIMS).

## Setup

**Requirements**
- Python 3.10+
- Internet access
## Run

From the folder that contains `part2_job_agent.py`:
```bash
python part2_job_agent.py "<company_name>" "<company_website>"
```

Example:
```bash
python part2_job_agent.py "Branch" "https://job-boards.greenhouse.io/branch"
```

Example output:
```text
Branch, https://job-boards.greenhouse.io/branch, https://job-boards.greenhouse.io/branch/jobs/7567701003
```

---

## How it works (short)

- **normalize_base()**: cleans the input URL and adds `https://` if missing.
- **find_career_page()**:
  - if the input is already a known job-board host (Greenhouse/Lever), it returns it directly
  - otherwise it parses the homepage, scores links using career keywords, and picks the best match
  - if nothing is found, it tries common fallback paths like `/careers`, `/jobs`, `/join-us`
- **extract_job_link()**:
  - parses the career page, filters out irrelevant links (benefits/about/locations, etc.)
  - detects job postings using URL patterns from common ATS platforms (Greenhouse/Workday/Workable/iCIMS, etc.)
  - returns the first matching job posting URL, or `NOT_FOUND`

---

## Notes / Limitations

Some career sites are JavaScript-heavy or block scraping, so the script may return `NOT_FOUND` even if jobs exist. A production version could add a headless browser (Playwright) or a crawler API for dynamic pages.

---
