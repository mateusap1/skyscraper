import os
import time
import base64
import requests

from requests import RequestException
from bs4 import BeautifulSoup, NavigableString, Tag


class Scraper(object):
    def __init__(self, current_path: str = ".", min_delay_for_request_us: int = 0):
        self.current_path = current_path.rstrip("/")
        self.min_delay_for_request_us = min_delay_for_request_us
        self.last_request_made = -1_000_000_000

    def url_file(self, url: str):
        # Encode the url to base64
        encoded_bytes = base64.b64encode(url.encode("utf-8"))
        encoded_url = encoded_bytes.decode("utf-8")

        return f"{self.current_path}/cache/{encoded_url}.html"

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

        # Find all the tags between audio and the next bold tag within their parent
        between_tags = False
        last_was_breakline = False
        result = [[]]
        for tag in parent_tag:
            if tag == audio_tag:
                between_tags = True
                continue

            elif between_tags and (tag.name == 'b' or (tag.find("b") not in [-1, None])):
                break

            elif between_tags and tag.text is not None:
                if tag.text == "\n" and last_was_breakline:
                    if result[-1] != []:
                        result.append([])
                    last_was_breakline = False
                elif tag.text == "\n":
                    last_was_breakline = True
                else:
                    result[-1].append(tag.text.strip())
                    last_was_breakline = False

        return result
