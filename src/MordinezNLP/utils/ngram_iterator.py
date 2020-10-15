def ngram_iterator(string: str, ngram: int = 3):
    """
    Iterates over string creating list of strings.

    :param item:
    :param ngram:
    :return:
    """
    if len(string) < ngram:
        return [string]

    to_return = []
    for i in range(0, len(string) - ngram + 1):
        to_return.append(string[i:i + ngram])
    return to_return


if __name__ == '__main__':
    print(ngram_iterator("<hello>", 3))
