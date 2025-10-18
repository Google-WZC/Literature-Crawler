import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


# how to crawl a website and extract all links using Python
def crawl_website(start_url):
    visited = set()
    to_visit = [start_url]

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to retrieve {url}: {e}")
            continue

        visited.add(url)
        print(f"Crawled: {url}")

        soup = BeautifulSoup(response.text, "html.parser")
        for link in soup.find_all("a", href=True):
            absolute_link = urljoin(url, link["href"])
            parsed_link = urlparse(absolute_link)
            if parsed_link.scheme in ("http", "https") and absolute_link not in visited:
                to_visit.append(absolute_link)

    return visited


if __name__ == "__main__":
    start_url = "https://www.google.com"  # Replace with the desired starting URL
    all_links = crawl_website(start_url)
    print(f"Total links found: {len(all_links)}")
    for link in all_links:
        print(link)
