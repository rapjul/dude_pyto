from dude_pyto import select

"""
This example demonstrates how to use Parsel + async HTTPX

To access an attribute, use:
    selector.attrib["href"]
You can also access an attribute using the ::attr(name) pseudo-element, for example "a::attr(href)", then:
    selector.get()
To get the text, use ::text pseudo-element, then:
    selector.get()
"""


@select(css="a.url", priority=2)
async def result_url(selector):
    return {"url": selector.attrib["href"]}


# Option to get url using ::attr(name) pseudo-element
@select(css="a.url::attr(href)", priority=2)
async def result_url2(selector):
    return {"url2": selector.get()}


@select(css=".title::text", priority=1)
async def result_title(selector):
    return {"title": selector.get()}


@select(css=".description::text", priority=0)
async def result_description(selector):
    return {"description": selector.get()}


if __name__ == "__main__":
    import dude_pyto

    dude_pyto.run(urls=["https://dude_pyto.ron.sh"], parser="parsel")
