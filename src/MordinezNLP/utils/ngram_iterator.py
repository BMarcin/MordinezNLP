def ngram_iterator(string: str, ngram_len: int = 3) -> list:
    """
    Iterates over string creating list of strings.
    For example for string "hello" and ngram_len set to 3 it will output
    ["hel", "ell", "llo"]

    Args:
        string: string to iterate on
        ngram_len: lenght of each ngram

    Returns:
        ngram - list of ngram_len characters of input string
    """
    if len(string) < ngram_len:
        return [string]

    to_return = []
    for i in range(0, len(string) - ngram_len + 1):
        to_return.append(string[i:i + ngram_len])
    return to_return


if __name__ == '__main__':
    print(ngram_iterator("<hello>", 3))
