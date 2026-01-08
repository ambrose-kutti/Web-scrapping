import requests
import json

url = "  "#your xhr type request URL here
headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest"
}

response = requests.get(url, headers=headers)
data = response.json()

with open("table1.txt", "w", encoding="utf-8") as f: #you can give your preferable name (yourtextname.txt)
    for item in data:
        try:
            name = json.loads(item.get("title", "{}")).get("en", "N/A")
            role = json.loads(item.get("content", "{}")).get("en", "N/A")  # fallback to 'content' if 'or' is missing
            phone = json.loads(item.get("number", "{}")).get("en", "N/A")
            email = json.loads(item.get("excerpt", "{}")).get("en", "N/A")

            line = f"{name} | {role} | {phone} | {email}\n" 
            f.write(line) # write each row to the file
        except Exception as e:
            f.write(f"Error parsing item: {e}\n")
