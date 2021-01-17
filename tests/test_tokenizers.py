import unittest

import spacy
from spacy.language import Language

from src.MordinezNLP.tokenizers import spacy_tokenizer


class TestTokenizers(unittest.TestCase):
    nlp: Language = spacy.load("en_core_web_sm")
    nlp.tokenizer = spacy_tokenizer(nlp)

    def test_spacy_tokenizer_case1(self):
        tokenized_data = self.nlp('Hello today is <date>, tomorrow it will be <number> degrees of celcius.')
        self.assertEqual(
            [str(token) for token in tokenized_data],
            [
                "Hello",
                "today",
                "is",
                "<date>",
                ",",
                "tomorrow",
                "it",
                "will",
                "be",
                "<number>",
                "degrees",
                "of",
                "celcius",
                "."
            ]
        )


if __name__ == '__main__':
    unittest.main()
