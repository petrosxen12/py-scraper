import os
import re
import sys

import json

import requests
from unittest.mock import patch

from app.scraper import (
    count_words,
    get_website_contents,
    scrape_text_privacy_policy,
    write_data_to_json_file,
)


def test_write_data_to_json_file():
    data = {"a": {1, 2, 3}, "b": [4, 5, 6]}
    file_path = "test_file.json"
    write_data_to_json_file(data, file_path)
    with open(file_path) as f:
        result = json.load(f)
    assert result == {"a": [1, 2, 3], "b": [4, 5, 6]}
    os.remove(file_path)


def test_count_words():
    body_words = "Hello World, Hello World, Hello"
    result = count_words(body_words)
    assert result == {"hello": 3, "world": 2}


def test_get_website_contents():
    url = "https://www.google.com"
    result = get_website_contents(url)
    assert result.status_code == 200


def test_scrape_text_privacy_policy():
    # Mocking the requests.get() method
    with patch("requests.get") as mocked_requests_get:
        mocked_requests_get.return_value.text = "<html><body>Test Body</body></html>"
        # requests.get.return_value.text =

        website = "http://www.example.com"
        priv_policy_link = "/privacy-policy"
        result = scrape_text_privacy_policy(website, priv_policy_link)

    # Asserting that the correct text is returned after removing scripts and styles
    assert result == "Test Body"


def test_scrape_text_privacy_policy_no_scripts_and_styles():
    # Mocking the requests.get() method
    with patch("requests.get") as mocked_requests_get:
        mocked_requests_get.return_value.text = "<html><body><script>Test Script</script><style>Test Style</style>Test Body</body></html>"

        website = "http://www.example.com"
        priv_policy_link = "/privacy-policy"
        result = scrape_text_privacy_policy(website, priv_policy_link)

    # Asserting that scripts and styles are removed
    assert result == "Test Body"


def test_scrape_text_privacy_policy_new_lines_and_tabs():
    # Mocking the requests.get() method
    with patch("requests.get") as mocked_requests_get:
        mocked_requests_get.return_value.text = "<html><body>Test Body\n\r\t</body></html>"

        website = "http://www.example.com"
        priv_policy_link = "/privacy-policy"
        result = scrape_text_privacy_policy(website, priv_policy_link)

    # Asserting that new lines and tabs are removed
    assert result == "Test Body"


def test_scrape_text_privacy_policy_multiple_spaces():
    # Mocking the requests.get() method
    with patch("requests.get") as mocked_requests_get:
        mocked_requests_get.return_value.text = "<html><body>Test    Body</body></html>"

        website = "http://www.example.com"
        priv_policy_link = "/privacy-policy"
        result = scrape_text_privacy_policy(website, priv_policy_link)

    # Asserting that multiple spaces are removed
    assert result == "Test Body"
