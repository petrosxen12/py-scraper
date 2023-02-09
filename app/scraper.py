import argparse
import re

import requests
from bs4 import BeautifulSoup


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

parser = argparse.ArgumentParser()
parser.add_argument('--website', help='The website to be scraped')
args = parser.parse_args()

website = args.website

try:
    website_source = requests.get(website)
except ValueError as e:
    print("Error scraping website")
    exit()

# Find all externally loaded sources i.e. images/scripts/fonts not hosted on *website* to be scraped
# These are any html which includes an "=http(s)://" which means loads something (anything) external

externally_loaded_regex = r"=\"(http[s]*://([\w*].*))\"(.?)"

ext_loaded_content = re.compile(externally_loaded_regex)
find_urls = r"\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"
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

# Parse the HTML content of the website
soup = BeautifulSoup(website_source.text, 'html.parser')
    
# Find all the hyperlinks
links = []
for link in soup.find_all('a'):
    href = link.get('href')
    # if is_valid_link(href):
    #     print(href)
    #     links.append(href)
    if href is not None and href[0] != '/':
        continue
    links.append(href)


# Print the links
for link in set(links):
    if "privacy-policy" in str(link):
        print(f"!!!----- {link}")
    print(link)


