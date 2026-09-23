"""
Web Scraper
-----------
A command-line tool that fetches HTML content using `requests`, parses DOM elements
with `beautifulsoup4`, extracts structured quote and author data, and serializes the
output into a CSV spreadsheet using Python's built-in `csv` module.
"""

import csv
import sys
from bs4 import BeautifulSoup
import requests

TARGET_URL = "http://quotes.toscrape.com/"
OUTPUT_CSV = "quotes.csv"


def fetch_page_html(url: str) -> str | None:
    """Fetches the raw HTML text from a target URL with exception handling."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        print("Error: Request timed out while trying to reach the website.")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the internet or target server.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: Server returned HTTP error: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error: An unexpected error occurred: {err}")
    return None


def parse_quotes(html_content: str) -> list[dict[str, str]]:
    """
    Parses raw HTML string using BeautifulSoup and extracts quote, author,
    and relative author link attributes.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    # Line 51: Finds all <div> elements that have class="quote"
    quote_elements = soup.find_all("div", class_="quote")

    extracted_data: list[dict[str, str]] = []

    for elem in quote_elements:
        # Extract quote text
        text_elem = elem.find("span", class_="text")
        text = text_elem.get_text(strip=True) if text_elem else "N/A"

        # Extract author name
        author_elem = elem.find("small", class_="author")
        author = author_elem.get_text(strip=True) if author_elem else "N/A"

        # Extract link to author profile
        link_elem = elem.find("a")
        relative_link = link_elem["href"] if link_elem and "href" in link_elem.attrs else ""
        full_author_url = f"http://quotes.toscrape.com{relative_link}" if relative_link else "N/A"

        extracted_data.append(
            {
                "quote": text,
                "author": author,
                "author_link": full_author_url,
            }
        )

    return extracted_data


def save_to_csv(data: list[dict[str, str]], filename: str) -> None:
    """Writes extracted dictionary objects into a cleanly formatted CSV file."""
    fieldnames = ["quote", "author", "author_link"]

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main() -> None:
    """Main execution entry point."""
    print(f"=== WEB SCRAPER ===")
    print(f"Fetching data from {TARGET_URL}...\n")

    html = fetch_page_html(TARGET_URL)
    if not html:
        print("Scraping aborted due to fetch failure.")
        sys.exit(1)

    quotes = parse_quotes(html)

    if not quotes:
        print("No results found. The website's structure may have changed.")
        sys.exit(1)

    save_to_csv(quotes, OUTPUT_CSV)
    print(f"Success! Extracted {len(quotes)} items and saved them to '{OUTPUT_CSV}'.")


if __name__ == "__main__":
    main()