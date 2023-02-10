import argparse
import logging
import re
from collections import Counter
import sys
import json

import requests
from bs4 import BeautifulSoup

# env variables for filennames
EXTERNAL_CONTENT_FILE = "content_file.json"
WORD_COUNT_FILE = "word_count_file.json"


def get_logger(name, level=logging.INFO):
    loggerius = logging.getLogger(name)
    loggerius.setLevel(level)
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    return loggerius


custom_logger = get_logger(__name__)


def write_data_to_json_file(data, file_path):
    # Needed for converting set to JSON serialazable object
    def set_default(obj):
        if isinstance(obj, set):
            return list(obj)
        raise TypeError

    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4, default=set_default)


def count_words(body_words):
    # Convert the body_words to lowercase
    body_words = body_words.lower()

    custom_logger.debug(body_words)

    # Remove all non-alphanumeric characters
    body_words = re.sub(r'[^a-z0-9]+', ' ', body_words)

    # Split the text into words
    words = body_words.split()

    # Count the occurrences of each word using the Counter class from the collections module
    # which is more efficiennt than looping
    word_counts = Counter(words)

    # type: ignore
    return dict(word_counts)


def get_website_contents(url):
    try:
        logging.info(f"Getting website contents for {url}")

        website_contents = requests.get(url, timeout=5)

        custom_logger.debug(website_contents)

    except ValueError as err:
        custom_logger.error(f"Error scraping website due to {err}")
        sys.exit()

    return website_contents


def scrape_text_privacy_policy(website, priv_policy_link):

    custom_logger.info(
        f"Scraping privacy policy for {website} in link {priv_policy_link}")

    privacy_policy_source = get_website_contents(website + priv_policy_link)

    custom_logger.info("Site contents succesfully scraped")

    # Parse the HTML content of the website
    soup = BeautifulSoup(privacy_policy_source.text, 'html.parser')

    # Remove scripts and styles
    for element in soup(["script", "style"]):
        element.extract()

    # Get the visible text
    text = soup.get_text()
    custom_logger.debug(text)

    # Remove all non-visible characters
    text = re.sub(r'[\n\r\t]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    custom_logger.debug(f"Cleaned text: {text}")

    return text

# For debbugging purposes


def is_valid_link(lnk):
    if lnk is None:
        return False

    try:
        res = requests.get(website + lnk, timeout=3)
        if res.status_code == 200:
            return True
        return False
    except requests.exceptions.InvalidURL:
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--website', help='The website to be scraped in the format http(s)://www.example.com')
    args = parser.parse_args()

    website = args.website

    website_source = get_website_contents(website)

    custom_logger.info(f"Finding all external loaded sources from {website}")

    # Find all externally loaded sources i.e. images/scripts/fonts not hosted on *website* to be scraped
    # These are any html which includes an "=http(s)://" which means loads something (anything) external
    externally_loaded_regex = r"=\"(http[s]*://([\w*].*))\"(.?)"

    ext_loaded_content = re.compile(externally_loaded_regex)
    find_urls = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
    # find_urls = r"(https?://\S+)"
    find_urls_compiled = re.compile(find_urls)
    # print(website_source.text)

    content = ext_loaded_content.findall(website_source.text)

    external_content = set()

    for cont in content:
        match_url = find_urls_compiled.match(cont[0])
        # print(match_url.group())
        c = match_url.group()

        external_content.add(c)

    for i, c in enumerate(external_content):
        print(f"{i+1} -- {c}")

    custom_logger.debug(f"External loaded content: {external_content}")
    # custom_logger.info(f"External loaded content: {external_content}")

    write_data_to_json_file(external_content, EXTERNAL_CONTENT_FILE)

# -------- Privacy Policy Scraping

    # Parse the HTML content of the website
    soup = BeautifulSoup(website_source.text, 'html.parser')

    # Find all the hyperlinks
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')

        # Debug
        # if is_valid_link(href):
        #     print(href)
        #     links.append(href)

        if href is not None and href[0] != '/':
            continue
        links.append(href)

    # Print the links and identify privacy policy
    privacy_policy = ""
    for link in set(links):
        if "privacy-policy" in str(link):
            privacy_policy = str(link)
            custom_logger.info(f"Privacy policy at {link}")

        custom_logger.debug(link)

    text = scrape_text_privacy_policy(website, privacy_policy)

    custom_logger.debug(text)

    word_count = count_words(text)

    custom_logger.debug(f"Word count of privacy policy: {word_count}")

    write_data_to_json_file(word_count, WORD_COUNT_FILE)
