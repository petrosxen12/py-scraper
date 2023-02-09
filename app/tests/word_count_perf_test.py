import re
import time
from collections import Counter


def count_words(text):
    # Convert the text to lowercase
    text = text.lower()

    # Remove all non-alphanumeric characters
    text = re.sub(r'[^a-z0-9]+', ' ', text)

    # Split the text into words
    words = text.split()

    # Count the occurrences of each word using the Counter class from the collections module
    word_counts = Counter(words)

    # type: ignore
    return dict(word_counts)


def old_count_words(text):
    # Convert the text to lowercase
    text = text.lower()

    # Remove all non-alphanumeric characters
    text = re.sub(r'[^a-z0-9]+', ' ', text)

    # Split the text into words
    words = text.split()

    # Count the occurrences of each word
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    return word_counts


def test_count_words_performance():
    text = "The quick brown fox jumps over the lazy dog." * 100000
    start_time = time.time()
    count_words(text)
    new_version_time = time.time() - start_time

    start_time = time.time()
    old_count_words(text)
    old_version_time = time.time() - start_time

    assert new_version_time < old_version_time, f"Expected new version to be faster, but it took {new_version_time:.4f} seconds and the old version took {old_version_time:.4f} seconds"


test_count_words_performance()
