from scraper import Scraper, NovoCanticoScraper
from bs4 import BeautifulSoup

import json
import csv


def main():
    scraper = NovoCanticoScraper(min_delay_for_request_us=500_000)

    for i in range(1, 38):
        html = scraper.load(
            f"https://crentebatista.wordpress.com/category/novo-cantico/page/{i}/"
        )

        hinos = scraper.parse(html)
        for hino in hinos:
            title = hino["titulo"].lower().replace(" ", "_").replace("\u00a0", "_")
            with open(f"assets/{title}.json", "w") as file:
                file.write(json.dumps(hino))


if __name__ == "__main__":
    main()
