# Web Scraping Toolkit 🕸️📑

A modular set of Python scripts for scraping websites, extracting structured text, downloading documents, and parsing JSON/XHR responses.  
Designed for engineers who need reproducible, production‑ready scraping workflows with polite crawling and robust error handling.

---

## 📂 Project Structure

- **text scrap.py** → Crawls a website, extracts page text, collects document links (PDF, DOC, XLS), and downloads them.
- **file scrap.py** → Focused on extracting visible text content from HTML pages into JSON.
- **scrap table.py** → Handles XHR/JSON endpoints, parsing tabular data (e.g., names, roles, phone, email) into text files.

---
## 📖 Usage

**1. Crawl and Download Documents**

python text_scrap.py

    → Crawls from BASE_URL
    → Saves metadata in dump_folder/pages_data.json
    → Downloads documents into dump_folder/docs/
    
**2. Extract Text Content**

python file_scrap.py

    → Crawls from BASE_URL
    → Saves text into text_folder/pages_text.json

**3. Parse XHR/JSON Table**

python scrap_table.py

    → Fetches JSON from an endpoint
    → Writes parsed rows into table.txt

## 🚀 Features

- Queue‑based BFS crawler with domain restriction
- Automatic detection and download of documents (`.pdf`, `.docx`, `.xls`, `.xlsx`, `.pptx`)
- Polite delays to avoid server overload
- ModSecurity error detection (HTTP 406)
- JSON export of page text and metadata
- Configurable output directories (`dump_folder`, `text_folder`)
- Browser‑like headers for realistic requests
- Robust error logging for failed requests

---

## 🛠️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/web-scraping-toolkit.git
cd web-scraping-toolkit
pip install -r requirements.txt
