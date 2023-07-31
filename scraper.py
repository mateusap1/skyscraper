import os
import time
import base64
import requests

from requests import RequestException
from bs4 import BeautifulSoup, NavigableString


class Scraper(object):
    def __init__(self, current_path: str = ".", min_delay_for_request_us: int = 0):
        self.current_path = current_path.rstrip("/")
        self.min_delay_for_request_us = min_delay_for_request_us
        self.last_request_made = -1_000_000_000

    def url_file(self, url: str):
        # Encode the url to base64
        encoded_bytes = base64.b64encode(url.encode('utf-8'))
        encoded_url = encoded_bytes.decode('utf-8')

        return f'{self.current_path}/cache/{encoded_url}.html'

    def load(self, url: str):
        if os.path.exists(self.url_file(url)):
            with open(self.url_file(url), "r") as file:
                html = file.read()
        else:
            # Sleep so that we always obbey min_delay_for_request_us
            # This is so we don't overload the site with a lot of
            # requests at once
            current_time = time.time()
            difference_time_from_last_request = current_time - self.last_request_made
            if difference_time_from_last_request < self.min_delay_for_request_us:
                time.sleep(
                    self.min_delay_for_request_us - difference_time_from_last_request
                )

            # Get the the response content and write it to an html file
            response = requests.get(url)
            if response.status_code != 200:
                raise RequestException(
                    f"Response of {url} not 200 - {response.status_code} {response.text}"
                )

            with open(self.url_file(url), "w") as file:
                file.write(response.text)

            html = response.text

        return html
    
    def parse(self, html: str):
        raise NotImplementedError("parse function not implemented")
    

class NovoCanticoScraper(Scraper):
    def parse(self, html_content: str):
        # Parse the HTML.
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the audio tag
        audio_tag = soup.find('audio')

        # Find the parent of the audio tag
        parent_tag = audio_tag.find_parent()

        # Initialize variables
        between_tags = False
        result_text = []
        last_parent = -72

        # Iterate over all descendants of the parent tag
        for descendant in parent_tag.descendants:
            if descendant == audio_tag:
                between_tags = True
                continue

            if descendant.parent.name == "audio":
                continue

            if between_tags:
                if isinstance(descendant, NavigableString):
                    if descendant.strip() == 'Seu navegador não suporta o elemento audio':
                        continue

                    if last_parent != descendant.parent:
                        last_parent = descendant.parent
                        result_text.append([])
                    
                    stripped = descendant.strip()
                    if stripped:  # check if the string is not empty or whitespace
                        result_text[-1].append(stripped)
                elif descendant.name == 'b' or descendant.find('b') is not None:
                    break

        return result_text
