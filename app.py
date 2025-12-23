import os
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

BASE_URL = "(THE WEBISTE URL)"
DOMAIN = urlparse(BASE_URL).netloc

visited = set()
queue = deque([BASE_URL])

pages_data = []
all_doc_links = set()

OUTPUT_DIR = "dump_folder" #you can give any name
DOC_DIR = os.path.join(OUTPUT_DIR, "docs")
os.makedirs(DOC_DIR, exist_ok=True)

# Browser-like headers
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": BASE_URL,
}

def is_internal(url):
    parsed = urlparse(url)
    netloc = parsed.netloc
    if netloc and netloc != DOMAIN:
        return False
    # skip weird .php root like "/.php"
    if parsed.path.strip() == "/.php":
        return False
    return True

def is_doc(url):
    return any(url.lower().endswith(ext) for ext in [".pdf", ".doc", ".docx", ".xls", ".xlsx"])

def is_modsec_block(html_text):
    return "Not Acceptable!" in html_text and "Mod_Security" in html_text

while queue:
    url = queue.popleft()
    if url in visited:
        continue
    visited.add(url)

    print("Fetching:", url)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
    except Exception as e:
        print("Error fetching:", url, e)
        pages_data.append({
            "url": url,
            "title": "",
            "text": "",
            "doc_links": [],
            "error": f"request_error: {e}",
        })
        continue

    content_type = resp.headers.get("Content-Type", "")

    # Direct document
    if is_doc(url) or any(ext in content_type.lower() for ext in ["pdf", "msword", "excel"]):
        all_doc_links.add(url)
        continue

    if "text/html" not in content_type:
        pages_data.append({
            "url": url,
            "title": "",
            "text": "",
            "doc_links": [],
            "error": f"non_html: {content_type}",
        })
        continue

    html = resp.text

    # Detect ModSecurity 406 error page
    if is_modsec_block(html):
        print("ModSecurity block detected at:", url)
        pages_data.append({
            "url": url,
            "title": "ERROR 406 Not Acceptable",
            "text": "",
            "doc_links": [],
            "error": "mod_security_406",
        })
        # do NOT follow links from this page
        time.sleep(2)
        continue

    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""

    # Extract visible text
    texts = []
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "a"]):
        text = tag.get_text(strip=True)
        if text:
            texts.append(text)
    page_text = "\n".join(texts)

    page_docs = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(url, href)

        if is_doc(full_url):
            page_docs.add(full_url)
            all_doc_links.add(full_url)
        elif is_internal(full_url):
            if full_url not in visited:
                queue.append(full_url)

    pages_data.append({
        "url": url,
        "title": title,
        "text": page_text,
        "doc_links": sorted(page_docs),
    })

    # polite delay
    time.sleep(2)

# Save page data
os.makedirs(OUTPUT_DIR, exist_ok=True)
json_path = os.path.join(OUTPUT_DIR, "pages_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(pages_data, f, ensure_ascii=False, indent=2)
print("Saved page data to:", json_path)

# Download all documents
for doc_url in sorted(all_doc_links):
    parsed = urlparse(doc_url)
    filename = os.path.basename(parsed.path)
    if not filename:
        continue

    filepath = os.path.join(DOC_DIR, filename)
    if os.path.exists(filepath):
        print("Already downloaded:", filename)
        continue

    try:
        print("Downloading:", doc_url)
        r = requests.get(doc_url, headers=HEADERS, timeout=20)
        if r.status_code == 200:
            with open(filepath, "wb") as f:
                f.write(r.content)
        else:
            print("Failed:", doc_url, "status", r.status_code)
    except Exception as e:
        print("Error downloading:", doc_url, e)
