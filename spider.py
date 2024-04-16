import urllib.parse

import requests
import re
from urllib.parse import urljoin


target_url = "https://old.mohirdev.uz"
target_links = []


def extract_links_from(url):
    response = requests.get(url)
    return re.findall(b'(?:href=")(.*)"', response.content)


def crawl(url):
    href_links = extract_links_from(url)

    for link in href_links:
        link = urllib.parse.urljoin(url, link)

        if "#" in link:
            link = link.split("#")[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


crawl(target_url)



