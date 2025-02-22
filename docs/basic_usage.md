# Basic Usage

To use `dude`, start by importing the library.

=== "Python"

    ```python
    from dude_pyto import select
    ```

A basic handler function consists of the structure below.
A handler function should accept 1 argument (element) and should be decorated with `@select()`.
The handler should return a dictionary.
Click on the annotations (+ sign) for more details.


=== "Python"

    ```python
    @select(css="<put-your-selector-here>") # (1)
    def handler(element): # (2)
        ... # (3)
        return {"<key>": "<value-extracted-from-element>"} # (4)
    ```

    1. `@select()` decorator.
    2. Function should accept 1 parameter, the element object found in the page being scraped.
    3. You can specify your Python algorithm here.
    4. Return a dictionary. This can contain an arbitrary amount of key-value pairs.

The example handler below extracts the text content of any element that matches the CSS selector `.title`.

=== "Python"

    ```python
    from dude_pyto import select


    @select(css=".title")
    def result_title(element):
        """
        Result title.
        """
        return {"title": element.text_content()}
    ```

It is possible to attach a single handler to multiple selectors.

=== "Python"

    ```python
    from dude_pyto import select


    @select(css="<a-selector>")
    @select(selector="<another-selector>")
    def handler(element):
        return {"<key>": "<value-extracted-from-element>"}
    ```

## Supported selector types

The `@select()` decorator does not only accept `selector` but also `css`, `xpath`, `text` and `regex`.
Please take note that `css`, `xpath`, `text` and `regex` are specific and `selector` can contain any of these types.

=== "Python"

    ```python
    from dude_pyto import select


    @select(css="<css-selector>")     #(1)
    @select(xpath="<xpath-selector>") #(2)
    @select(text="<text-selector>")  #(3)
    @select(regex="<regex-selector>") #(4)
    def handler(element):
        return {"<key>": "<value-extracted-from-element>"}
    ```

    1. CSS Selector
    2. XPath Selector
    3. Text Selector
    4. Regular Expression Selector

It is possible to use 2 or more of these types at the same time but only one will be used taking the precedence `selector` -> `css` -> `xpath` -> `text` -> `regex`.

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

## Examples

Check out the example in [examples/flat.py](https://github.com/roniemartinez/dude/blob/master/examples/flat.py) and run it on your terminal using the command `python examples/flat.py`.
