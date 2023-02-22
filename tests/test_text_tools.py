import pymorphy2
import pytest

from exceptions import TimeoutException
from text_tools import calculate_jaundice_rate, split_by_words
from utils import time_limit

morph = pymorphy2.MorphAnalyzer()


def test_split_by_words():
    assert split_by_words(morph, "Во-первых, он хочет, чтобы") == ["во-первых", "хотеть", "чтобы"]

    assert split_by_words(morph, "«Удивительно, но это стало началом!»") == ["удивительно", "это", "стать", "начало"]


def test_split_long_by_words():

    with pytest.raises(TimeoutException) as exc_info:
        with open("dicts/long.txt", "r") as f:
            split_by_words(morph, f.read())

    assert str(exc_info.value) == "Timed out!"


def test_calculate_jaundice_rate():
    assert -0.01 < calculate_jaundice_rate([], []) < 0.01
    assert 33.0 < calculate_jaundice_rate(["все", "аутсайдер", "побег"], ["аутсайдер", "банкротство"]) < 34.0
