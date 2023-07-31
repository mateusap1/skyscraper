from scraper import Scraper, NovoCanticoScraper
from bs4 import BeautifulSoup

import json
import csv


def main():
    # scraper = Scraper(min_delay_for_request_us=500_000)
    scraper = NovoCanticoScraper(min_delay_for_request_us=500_000)

    with open("assets/hinos.csv", mode="r", newline="") as file:
        reader = csv.reader(file)

        for i, (hino, url) in enumerate(reader):
            if i < 80:
                continue

            if i > 90:
                break

            if i == 0:
                continue

            html = scraper.load(url)
            result = scraper.parse(html)
            print(hino, result)

            # with open(f"results/{i}.json", "w") as file:
            #     file.write(json.dumps({
            #         "nome": hino,
            #         "estrofes": find_stanzas_and_verses(html)
            #     }))


if __name__ == "__main__":
    main()
