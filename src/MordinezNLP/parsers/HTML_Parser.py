from selectolax.parser import HTMLParser


def HTML_Parser(html_doc: str, separator: str = ' ') -> str:
    """
    Function which removes not vaulable text and tags from HTML docs. It is based on research
    https://rushter.com/blog/python-fast-html-parser/

    **IMPORTANT**
    If You must be 100% sure, that text You want to process is a HTML doc. Otherwise some parts of
    the source text can be deleted because of misunderstanding text as a tags.

    Args:
        separator: Separator used to join HTML nodes in *selectolax* package
        html_doc (str): a HTML doc

    Returns:
        str: String which is a vaulable text parsed from HTML doc.
    """
    tree = HTMLParser(html_doc)

    if tree.body is None:
        return html_doc

    for tag in tree.css('script'):
        tag.decompose()

    for tag in tree.css('style'):
        tag.decompose()

    text: str = tree.body.text(separator=separator)
    return text.strip()
