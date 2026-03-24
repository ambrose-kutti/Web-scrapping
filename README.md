

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
