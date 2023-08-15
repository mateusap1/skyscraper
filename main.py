from scraper import Scraper, NovoCanticoScraper, HarpaCristaScraper
from bs4 import BeautifulSoup
from typing import List

import requests
import json
import time
import csv


def start_from_word(content: str, expected_word: str):
    current_expected_word_index = 0
    found = False
    new_content = ""

    for char in content:
        if found:
            new_content += char
        else:
            if char == expected_word[current_expected_word_index]:
                if current_expected_word_index + 1 == len(expected_word):
                    found = True
                else:
                    current_expected_word_index += 1
            else:
                current_expected_word_index = 0

    return new_content

def end_on_word(content: str, expected_word: str):
    current_expected_word_index = 0
    new_content = ""

    for char in content:
        new_content += char
        if char == expected_word[current_expected_word_index]:
            if current_expected_word_index + 1 == len(expected_word):
                return new_content[:-current_expected_word_index-1]
            else:
                current_expected_word_index += 1
        else:
            current_expected_word_index = 0

    return new_content


def remove_line_with_word(content: str, words: List[str]):
    new_lines = []
    for line in content.split("\n"):
        if line.strip() not in words:
            new_lines.append(line)

    return "\n".join(new_lines)


def carregar_harpa_crista():
    for i in range(1, 641):
        response = requests.get(f"https://api.harpacrista.org/{i}")

        with open(f"./cache/{i}.json", "w") as file:
            file.write(json.dumps(response.json()))

        print(f"Atualizei hino {i} com sucesso!")

        time.sleep(0.2)

        if i % 100 == 0:
            print("Respirando um pouco...")

            time.sleep(5)


def filtrar_harpa_crista():
    for i in range(1, 641):
        with open(f"./cache/{i}.json", "r") as file:
            hino = json.loads(file.read())

        content = hino["content"]

        content = start_from_word(content, "</audio>")
        content = end_on_word(content, "\n\n\n")
        content = content.replace("<blockquote>", "").replace("</blockquote>", "")
        content = remove_line_with_word(content, [str(i) for i in range(1, 10)])

        estrofes = [estrofe.split("\n") for estrofe in content.split("\n\n")]
        estrofes = [list(filter(lambda x : x.strip() != "", estrofe)) for estrofe in estrofes]

        with open(f"./assets/harpa_crista/{i}.json", "w") as file:
            file.write(json.dumps({
                "titulo": f"Hino {i} {hino['title']}",
                "estrofes": estrofes
            }))

        with open(f"./assets/harpa_crista/txt/{i}.txt", "w") as file:
            file.write(f"Hino {i} {hino['title']}\n\n" + "\n\n".join(["\n".join(estrofe) for estrofe in estrofes]))


def main():
    filtrar_harpa_crista()


if __name__ == "__main__":
    main()
