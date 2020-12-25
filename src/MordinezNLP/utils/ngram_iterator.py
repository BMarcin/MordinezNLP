def ngram_iterator(string: str, ngram_len: int = 3) -> list:
    """
    Returns an iterator that yeilds the given string and its ngrams.
    Each subsequent list element has got lenght set to *ngram_len*. The differences between each of following elements
    in list is a one letter forward in a context.
    For example for string "hello" and ngram_len set to 3 it will output
    ["hel", "ell", "llo"]

    Args:
        string (str): string to iterate on
        ngram_len (int): lenght of each ngram

    Returns:
        list: ngram - list of ngram_len characters of input string
    """
    total = len(string) - ngram_len + 1
    if total < 1:
        total = 1
    for i in range(0, total):
        yield string[i:i + ngram_len]


if __name__ == '__main__':
    print(list(ngram_iterator("<hello>", 3)))
