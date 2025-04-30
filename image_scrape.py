import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from urllib.parse import urljoin   # ← new

url = "https://en.wikinews.org/wiki/Main_Page"     # Example test site
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

folder = "images"
os.makedirs(folder, exist_ok=True)

for img in soup.find_all("img"):
    src = img.get("src")
    if not src:
        continue

    # Build a full URL, even if src is relative
    img_url = urljoin(url, src)

    try:
        res = requests.get(img_url, timeout=10)
        res.raise_for_status()
        img_obj = Image.open(BytesIO(res.content)).convert("RGB")
        base = os.path.splitext(os.path.basename(img_url.split("?")[0]))[0]
        out_path = os.path.join(folder, base + ".jpg")
        img_obj.save(out_path, "JPEG", quality=85)
        print(f"Saved: {out_path}")
    except Exception as e:
        print(f"Skipping {img_url}: {e}")
