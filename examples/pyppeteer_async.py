from dude_pyto import select


@select(css="a.url")
async def result_url(element, page):
    handle = await element.getProperty("href")
    return {"url": await handle.jsonValue()}


@select(css=".title")
async def result_title(element, page):
    return {"title": await page.evaluate("(element) => element.textContent", element)}


@select(css=".description")
async def result_description(element, page):
    return {"description": await page.evaluate("(element) => element.textContent", element)}


if __name__ == "__main__":
    from pathlib import Path

    import dude_pyto

    html = f"file://{(Path(__file__).resolve().parent / 'dude_pyto.html').absolute()}"
    dude_pyto.run(urls=[html], parser="pyppeteer")
