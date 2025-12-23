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

pages_text = []

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
    if parsed.path.strip() == "/.php":
        return False
    return True

def is_doc(url):
    return any(url.lower().endswith(ext) for ext in [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"
    ])

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
        continue

    content_type = resp.headers.get("Content-Type", "")

    # Skip non-HTML (your PDFs/resources are already downloaded)
    if "text/html" not in content_type:
        continue

    html = resp.text
    if is_modsec_block(html):
        print("ModSecurity block at:", url)
        continue

    soup = BeautifulSoup(html, "html.parser")
    title = (soup.title.string or "").strip() if soup.title else ""

    # Extract all meaningful visible text
    texts = []
    for tag in soup.find_all(["h1","h2","h3","h4","h5","h6",
                                "p","li","td","th","a","span","div"]):
        text = tag.get_text(" ", strip=True)
        if text:
            texts.append(text)
    page_text = "\n".join(texts)

    pages_text.append({
        "url": url,
        "title": title,
        "text": page_text,
    })

    # Discover more pages (HTML only)
    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(url, href)
        if not is_internal(full_url):
            continue
        if is_doc(full_url):
            # skip docs here, you already downloaded them
            continue
        if full_url not in visited:
            queue.append(full_url)

    time.sleep(1.5)  # polite delay

# Save all textual content to JSON
os.makedirs("text_folder", exist_ok=True)
with open("text_folder/pages_text.json", "w", encoding="utf-8") as f:
    json.dump(pages_text, f, ensure_ascii=False, indent=2)

print("Saved text of", len(pages_text), "pages to text_folder/pages_text.json")
