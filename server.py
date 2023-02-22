import pymorphy2
from aiohttp import web
from anyio import create_task_group

from processing import process_article, split_by_words


async def process_urls(request):
    if request.query:
        urls = request.query["urls"].split(",")
        if len(urls) > 10:
            raise web.HTTPBadRequest(text="too many urls in request, should be 10 or less")
        results = []
        async with create_task_group() as tg:
            for url in urls:
                tg.start_soon(process_article, results, url, charged_words, morph)

        return web.json_response(results)
    raise web.HTTPBadRequest(text="Please provide urls to process")


if __name__ == "__main__":
    app = web.Application()
    app.add_routes([web.get("/", process_urls)])

    morph = pymorphy2.MorphAnalyzer()

    charged_words = []
    with open("dicts/negative_words.txt", "r") as f:
        charged_words.extend(split_by_words(morph, f.read()))

    with open("dicts/positive_words.txt", "r") as f:
        charged_words.extend(split_by_words(morph, f.read()))

    web.run_app(app)
