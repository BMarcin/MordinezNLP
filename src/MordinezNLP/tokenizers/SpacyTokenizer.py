import spacy
from spacy import util
from spacy.lang.char_classes import LIST_ELLIPSES, LIST_ICONS, ALPHA_LOWER, ALPHA_UPPER, CONCAT_QUOTES, ALPHA
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
    if type(nlp.Defaults.prefixes) is list:
        prefixes = nlp.Defaults.prefixes + ['^<i>']
        suffixes = nlp.Defaults.suffixes + ['</i>$']
    else:
        prefixes = nlp.Defaults.prefixes + ('^<i>',)
        suffixes = nlp.Defaults.suffixes + ('</i>$',)

    prefixes = list(prefixes)
    prefixes.remove("<")
    prefixes = tuple(prefixes)

    suffixes = list(suffixes)
    suffixes.remove(">")
    suffixes = tuple(suffixes)

    # code from https://spacy.io/usage/linguistic-features#native-tokenizers
    infixes = (
            LIST_ELLIPSES
            + LIST_ICONS
            + [
                r"(?<=[0-9])[+\-\*^](?=[0-9-])",
                r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                    al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
                ),
                r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
                # EDIT: commented out regex that splits on hyphens between letters:
                # r"(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS),
                r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
            ]
    )
    rules = nlp.Defaults.tokenizer_exceptions

    token_match = None

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

    test_doc = nlp(
        'Hello today is <date>, tomorrow it will be <number> degrees of celcius. Remember, to don\'t touch the glass. <currency> <number>')

    for token in test_doc:
        print(token.norm_)
