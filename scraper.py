
import requests
import json
import time
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin

BASE_URL = "https://quotes.toscrape.com/"

HEADERS = {
    "User-Agent": "InternCircle-Student-Learning-Project"
}


def scrape_quotes():
    url = BASE_URL
    quotes = []

    while url:
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            print("Error fetching webpage:", e)
            break

        soup = BeautifulSoup(response.text, "html.parser")
        quote_boxes = soup.select("div.quote")

        for box in quote_boxes:
            quote_text = box.select_one("span.text")
            author_name = box.select_one("small.author")

            if quote_text and author_name:
                tags = [
                    tag.get_text(strip=True)
                    for tag in box.select("a.tag")
                ]

                quotes.append({
                    "text": quote_text.get_text(strip=True),
                    "author": author_name.get_text(strip=True),
                    "tags": tags
                })

        print("Scraped:", url)

        next_page = soup.select_one("li.next a")

        if next_page:
            url = urljoin(url, next_page["href"])
            time.sleep(1)
        else:
            url = None

    return quotes


def save_json(quotes):
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes, file, indent=2, ensure_ascii=False)

    print("JSON file saved successfully!")


def save_text(quotes):
    with open("quotes.txt", "w", encoding="utf-8") as file:
        for index, quote in enumerate(quotes, start=1):
            file.write(f"Quote {index}\n")
            file.write(f"Text: {quote['text']}\n")
            file.write(f"Author: {quote['author']}\n")
            file.write(f"Tags: {', '.join(quote['tags'])}\n")
            file.write("-" * 50 + "\n")

    print("Text file saved successfully!")


def show_summary(quotes):
    if not quotes:
        print("No quotes were collected.")
        return

    authors = Counter(quote["author"] for quote in quotes)

    all_tags = []
    for quote in quotes:
        all_tags.extend(quote["tags"])

    common_tag = Counter(all_tags)

    print("\n===== SCRAPING SUMMARY =====")
    print("Total Quotes:", len(quotes))
    print("Most Quoted Author:", authors.most_common(1)[0][0])

    if common_tag:
        print("Most Common Tag:", common_tag.most_common(1)[0][0])


def main():
    print("===== WEB SCRAPER FOR QUOTES =====")
    print("\nStarting web scraping...\n")

    quotes = scrape_quotes()

    if not quotes:
        print("No data collected. Check your internet connection.")
        return

    save_json(quotes)
    save_text(quotes)
    show_summary(quotes)

    print("\nScraping completed successfully!")


if __name__ == "__main__":
    main()

