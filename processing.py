import aiohttp
import pymorphy2
from aiohttp.client_exceptions import ClientResponseError
from async_timeout import timeout

from adapters.exceptions import ArticleNotFound
from adapters.inosmi_ru import sanitize
from exceptions import TimeoutException
from text_tools import calculate_jaundice_rate, split_by_words
from utils import ProcessingStatus, timer

FETCHING_TIMEOUT = 5


async def fetch(session, url):
    async with timeout(FETCHING_TIMEOUT):

        async with session.get(url, ssl=False) as response:
            response.raise_for_status()
            return await response.text()


@timer
async def process_article(session: aiohttp.ClientSession, results: list, url: str, charged_words: list, morph: pymorphy2.MorphAnalyzer):
    article = {"url": url, "status": ProcessingStatus.OK.value, "jaundice_rate": None, "word_count": None}
    try:
        html = await fetch(session, url)
        text = sanitize(html, plaintext=True)

        article["jaundice_rate"] = calculate_jaundice_rate(text, charged_words)
        article["word_count"] = len(split_by_words(morph, text))

    except ClientResponseError:
        article["status"] = ProcessingStatus.FETCH_ERROR.value
    except ArticleNotFound:
        article["status"] = ProcessingStatus.PARSING_ERROR.value
    except TimeoutError:
        article["status"] = ProcessingStatus.TIMEOUT.value
    except TimeoutException:
        article["status"] = ProcessingStatus.TIMEOUT.value

    results.append(article)
