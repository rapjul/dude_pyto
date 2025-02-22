# BeautifulSoup4 Scraper

Option to use [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) as parser backend instead of Playwright has been added in [Release 0.2.0](https://github.com/roniemartinez/dude/releases/tag/0.2.0).
BeautifulSoup4 is an optional dependency and can only be installed via `pip` using the command below.

=== "Terminal"

    ```bash
    pip install pydude[bs4]
    ```

## Required changes to your script in order to use BeautifulSoup4

Instead of ElementHandle objects when using Playwright as parser backend, Soup objects are passed to the decorated functions.


=== "Python"

    ```python
    from dude_pyto import select


    @select(css="a.url")
    def result_url(soup):
        return {"url": soup["href"]} # (1)


    @select(css=".title")
    def result_title(soup):
        return {"title": soup.get_text()} # (2)
    ```

    1. Attributes can be accessed by key.
    2. Texts can be accessed using the `get_text()` method.


## Running dude_pyto with BeautifulSoup4

You can run BeautifulSoup4 parser backend using the `--bs4` command-line argument or `parser="bs4"` parameter to `run()`.


=== "Terminal"

    ```commandline
    dude_pyto scrape --url "<url>" --bs4 --output data.json path/to/script.py
    ```

=== "Python"

    ```python
    if __name__ == "__main__":
        import dude

        dude.run(urls=["https://dude.ron.sh/"], parser="bs4", output="data.json")
    ```

## Limitations

1. BeautifulSoup4 only supports CSS selector.
2. Setup handlers are not supported.
3. Navigate handlers are not supported.


## Examples

Examples are can be found at [examples/bs4_sync.py](https://github.com/roniemartinez/dude/tree/master/examples/bs4_sync.py) and [examples/bs4_async.py](https://github.com/roniemartinez/dude/tree/master/examples/bs4_async.py).
