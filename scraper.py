import os
import time
import requests
from bs4 import BeautifulSoup
import boto3

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_numbe>
BUCKET_NAME = "poke-scrapper-noam" 

s3 = boto3.client("s3")

def get_generation_images():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    gens = {}
    current_gen = None

    for tag in soup.find_all(["h3", "img"]):
        if tag.name == "h3":
            span = tag.find("span", {"class": "mw-headline"})
            if span and "Generation" in span.text:
                current_gen = span.text.replace("Generation ", "gen").replace(" ", "")
                gens[current_gen] = []
        if tag.name == "img" and current_gen:
            src = tag.get("src")
            if src:
                if src.startswith("//"):
                    src = "https:" + src
                if "archives.bulbagarden.net" in src:
                    gens[current_gen].append(src)

    return gens

def download_and_upload(url, gen):
    try:
        filename = url.split("/")[-1]
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        s3.upload_file(
            filename,
            BUCKET_NAME,
            f"images/{gen}/{filename}"
        )
        os.remove(filename)
        print(f"✅ Uploaded {gen}/{filename}")

    except Exception as e:
        print(f"❌ Error for {url}: {e}")

def main():
    gens = get_generation_images()
    for gen, urls in gens.items():
        print(f"=== {gen} → {len(urls)} images ===")
        for url in urls:
            download_and_upload(url, gen)
            time.sleep(1) 

if __name__ == "__main__":
    main()
