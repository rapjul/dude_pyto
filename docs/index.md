# Getting Started

dude_pyto is a very simple framework for writing web scrapers using Python decorators. The design, inspired by [Flask](https://github.com/pallets/flask), was to easily build a web scraper in just a few lines of code. dude_pyto has an easy-to-learn syntax.

!!! warning

    🚨 dude_pyto is currently in Pre-Alpha. Please expect breaking changes.

## Installation

To install, simply run the following from terminal. Click on the annotations (+ sign) for more details.

=== "Terminal"

    ```bash
    pip install pydude_pyto #(1)
    playwright install #(2)
    ```

    1. Install `pydude` from PyPI
    2. Install playwright binaries for Chrome, Firefox and Webkit. See [Getting Started | Playwright Python](https://playwright.dev/python/docs/intro#pip)

## Minimal web scraper

The simplest web scraper will look like the example below. Click on the annotations (+ sign) for more details.

=== "Python"

    ```python
    from dude_pyto import select #(1)


    @select(css="a")  #(2)
    def get_link(element): #(3)
        return {"url": element.get_attribute("href")} #(4)
    ```

    1. Import the `@select()` decorator
    2. Decorate the function `get_link()` with `@select()` and specify the selector for finding the element in the page.
    3. It is required that decorator functions should accept 1 argument (2 for Pyppeteer). This can be an object or a string depending on which backend was used.
    4. Return a dictionary with information obtained from the argument object. The dictionary can contain multiple key-value pairs or can be empty.

The example above will get all the [hyperlink](https://en.wikipedia.org/wiki/Hyperlink#HTML) elements in a page and calls the handler function `get_link()` for each element.

## How to run the scraper

To start scraping, use any of the following options. Click on the annotations (+ sign) for more details.

=== "Terminal"

    ```bash
    dude_pyto scrape --url "<url>" --output data.json path/to/script.py #(1)
    ```

    1. You can run your scraper from terminal/shell/command-line by supplying URLs, the output filename of your choice and the paths to your python scripts to `dude_pyto scrape` command.

=== "Python"

    ```python
    if __name__ == "__main__":
        import dude

        dude.run(urls=["https://dude.ron.sh/"]) #(1)
    ```

    1. You can also use **dude.run()** function and run **python path/to/script.py** from terminal.

The output in `data.json` should contain the actual URL and the metadata prepended with underscore.

```json5
[
  {
    "_page_number": 1,
    "_page_url": "https://dude.ron.sh/",
    "_group_id": 4502003824,
    "_group_index": 0,
    "_element_index": 0,
    "url": "/url-1.html"
  },
  {
    "_page_number": 1,
    "_page_url": "https://dude.ron.sh/",
    "_group_id": 4502003824,
    "_group_index": 0,
    "_element_index": 1,
    "url": "/url-2.html"
  },
  {
    "_page_number": 1,
    "_page_url": "https://dude.ron.sh/",
    "_group_id": 4502003824,
    "_group_index": 0,
    "_element_index": 2,
    "url": "/url-3.html"
  }
]
```

Changing the output to `--output data.csv` should result in the following CSV content.

![data.csv](csv.png)

## License

This project is licensed under the terms of the GNU AGPLv3+ license.
