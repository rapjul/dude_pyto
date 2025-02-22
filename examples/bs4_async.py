from dude_pyto import select

"""
This example demonstrates how to use BeautifulSoup4 + async HTTPX

To access an attribute, use:
    soup["href"]
To get the text, use:
    soup.get_text()
"""


@select(css="a.url", priority=2)
async def result_url(soup):
    return {"url": soup["href"]}


@select(css=".title", priority=1)
async def result_title(soup):
    return {"title": soup.get_text()}


@select(css=".description", priority=0)
async def result_description(soup):
    return {"description": soup.get_text()}


if __name__ == "__main__":
    import dude_pyto

    dude_pyto.run(urls=["https://dude_pyto.ron.sh"], parser="bs4")
