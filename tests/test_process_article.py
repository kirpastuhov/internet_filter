import aiohttp
import pymorphy2
import pytest

from processing import process_article

morph = pymorphy2.MorphAnalyzer()


@pytest.mark.asyncio
async def test_fetch_error():
    results = []
    async with aiohttp.ClientSession() as session:
        await process_article(session, results, "https://inosmi.ru/economic/invalid.html", [], morph)

    assert results[0]["status"] == "FETCH_ERROR"


@pytest.mark.asyncio
async def test_parse_error():
    results = []
    async with aiohttp.ClientSession() as session:
        await process_article(
            session, results, "https://www.reuters.com/world/europe/british-embassy-guard-who-spied-russia-jailed-13-years-2023-02-17", [], morph
        )
    assert results[0]["status"] == "PARSING_ERROR"
