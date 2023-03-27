import string

from utils import time_limit, timer

PROCESSING_LIMIT = 1


async def _clean_word(word):
    word = word.replace("«", "").replace("»", "").replace("…", "")
    # FIXME какие еще знаки пунктуации часто встречаются ?
    word = word.strip(string.punctuation)
    return word


@timer
async def split_by_words(morph, text):
    """Takes account of punctuation marks, case and word forms, and throws out prepositions."""
    words = []
    with time_limit(PROCESSING_LIMIT):
        for word in text.split():
            cleaned_word = await _clean_word(word)
            normalized_word = morph.parse(cleaned_word)[0].normal_form
            if len(normalized_word) > 2 or normalized_word == "не":
                words.append(normalized_word)
    return words


def calculate_jaundice_rate(article_words, charged_words):
    """Calculates the jaundice of the text, takes a list of "charged" words and searches for them within article_words."""

    if not article_words:
        return 0.0

    found_charged_words = [word for word in article_words if word in set(charged_words)]

    score = len(found_charged_words) / len(article_words) * 100

    return round(score, 2)
