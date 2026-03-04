import re 
import sys
import requests
from bs4 import BeautifulSoup 
from urllib.parse import urljoin, urlparse 

HEADERS = {"User-Agent": "Mozilla/5.0"}

CAREER_KEYWORDS = [ 
    "careers", "career", "jobs", "join-us", "joinus", "work-with-us",
    "open-positions", "opportunities", "vacancies"
]

JOB_HOST_HINTS = [ 
    "lever.co", "greenhouse.io", "myworkdayjobs.com", "workable.com", "icims.com"
]

BAD_WORDS = [ 
    "life-at", "university", "benefit", "benefits", "location", "locations",
    "culture", "values", "blog", "news", "privacy", "terms", "about", "team", "teams"
]

def fetch(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True) 
    r.raise_for_status()
    return r.text 

def normalize_base(url: str) -> str:
    u = url.strip() 
    if not u.startswith("http"): 
        u = "https://" + u 
    return u

def find_career_page(company_site: str) -> str | None:
    host = urlparse(company_site).netloc.lower() 
    if host in {"boards.greenhouse.io", "job-boards.greenhouse.io", "jobs.lever.co"}:
        return company_site.rstrip("/") 

    html = fetch(company_site)
    soup = BeautifulSoup(html, "lxml")
    scored = [] 
    for a in soup.select("a[href]"): 
        text = (a.get_text() or "").strip().lower()
        
        href_raw = (a.get("href") or "").strip()
        href = href_raw.lower() 

        score = 0 
        if any(k in text for k in ["career", "careers", "jobs", "join"]):
            score += 2 
        if any(k in href for k in CAREER_KEYWORDS):
            score += 3 
        if score > 0: 
            scored.append((score, urljoin(company_site, href_raw)))

    scored.sort(reverse=True, key=lambda x: x[0]) 
    if scored:
        return scored[0][1] 

    base = company_site.rstrip("/") 
    candidates = [f"{base}/careers", f"{base}/career", f"{base}/jobs", f"{base}/join-us"] #list to try
    for c in candidates: 
        try:
            _ = fetch(c)
            return c
        except Exception:
            pass

    return None 
def extract_job_link(career_url: str) -> str | None:
    html = fetch(career_url) 
    soup = BeautifulSoup(html, "lxml") 

    career_lower = career_url.lower().rstrip("/") 

    def looks_like_real_posting(h: str) -> bool: 
        if any(b in h for b in BAD_WORDS):
            return False

      
        if "/jobs/listing/" in h:
            return True

        
        if "greenhouse.io" in h and ("/jobs/" in h or "gh_jid" in h):
            return True

        
        if "myworkdayjobs.com" in h and ("/job/" in h or "/jobs/" in h):
            return True

        if "workable.com" in h and "/j/" in h:
            return True

        if "icims.com" in h and "jobs/" in h:
            return True
        
        return False

    candidates = []
    for a in soup.select("a[href]"): 
        href = urljoin(career_url, a["href"]) 
        h = href.lower().rstrip("/") 

        if h == career_lower: 
            continue

        if looks_like_real_posting(h): 
            candidates.append(href)
    if candidates:
        return candidates[0]  
    else: 
        return None

def main(): 
    if len(sys.argv) < 3:
        print("Usage: python part2_job_agent.py <company_name> <company_website>")
        sys.exit(1) 
    company_name = sys.argv[1].strip()
    company_site = normalize_base(sys.argv[2]) 

    try:
        career = find_career_page(company_site)
        if not career:
            print(f"{company_name}, NOT_FOUND, NOT_FOUND")
            return

        job = extract_job_link(career) or "NOT_FOUND"
        print(f"{company_name}, {career}, {job}")

    except Exception as e:
        print(f"{company_name}, ERROR, ERROR\n{e}") 

if __name__ == "__main__":
    main()