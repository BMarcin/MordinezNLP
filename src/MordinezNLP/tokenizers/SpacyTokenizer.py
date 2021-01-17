import spacy
from spacy import util
from spacy.lang.tokenizer_exceptions import TOKEN_MATCH
from spacy.language import Language
from spacy.tokenizer import Tokenizer


def spacy_tokenizer(nlp: Language) -> Tokenizer:
    """
    A custom SpaCy tokenizer ready for tokenizing special tokens which comes from *BasicProcessor*.

    Out of the box SpaCy tokenizer will parse special tokens (tags) separately for example: "<date>" to "< date >",
    so that function changes such behavior.

    Args:
        nlp (spacy.language.Language): A Language object from SpaCy

    Returns:
        spacy.tokenizer.Tokenizer: A SpaCy tokenizer
    """
    prefixes = nlp.Defaults.prefixes + ('^<i>', )
    suffixes = nlp.Defaults.suffixes + ('</i>$', )

    prefixes = list(prefixes)
    prefixes.remove("<")
    prefixes = tuple(prefixes)

    suffixes = list(suffixes)
    suffixes.remove(">")
    suffixes = tuple(suffixes)

    infixes = nlp.Defaults.infixes
    rules = nlp.Defaults.tokenizer_exceptions

    token_match = TOKEN_MATCH

    prefix_search = util.compile_prefix_regex(prefixes).search
    suffix_search = util.compile_suffix_regex(suffixes).search
    infix_finditer = util.compile_infix_regex(infixes).finditer

    return Tokenizer(
        nlp.vocab,
        rules=rules,
        prefix_search=prefix_search,
        suffix_search=suffix_search,
        infix_finditer=infix_finditer,
        token_match=token_match
    )


if __name__ == '__main__':
    nlp: Language = spacy.load("en_core_web_sm")

    nlp.tokenizer = spacy_tokenizer(nlp)

    test_doc = nlp('Hello today is <date>, tomorrow it will be <number> degrees of celcius.')

    for token in test_doc:
        print(token)
