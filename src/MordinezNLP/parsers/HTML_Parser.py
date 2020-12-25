from selectolax.parser import HTMLParser


def HTML_Parser(html_doc: str) -> str:
    """
    Function which removes not vaulable text and tags from HTML docs. It is based on research
    https://rushter.com/blog/python-fast-html-parser/

    Args:
        html_doc (str): a HTML doc

    Returns:
        str: String which is a vaulable text parsed from HTML doc.
    """
    tree = HTMLParser(html_doc)

    for tag in tree.css('script'):
        tag.decompose()

    for tag in tree.css('style'):
        tag.decompose()

    text = tree.body.text(separator=' ')
    return text
