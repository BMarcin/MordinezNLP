def ngram_iterator(string: str, ngram: int = 3):
***REMOVED***
    Iterates over string creating list of strings.

    :param item:
    :param ngram:
    :return:
***REMOVED***
    if len(string) < ngram:
***REMOVED***string]

    to_return = []
    for i in range(0, len(string) - ngram + 1):
        to_return.append(string[i:i + ngram])
    return to_return


***REMOVED***
    print(ngram_iterator("<hello>", 3))
