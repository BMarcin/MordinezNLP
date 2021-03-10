import unittest

import spacy
from spacy.language import Language

try:
    from src.MordinezNLP.tokenizers import spacy_tokenizer
except:
    from MordinezNLP.tokenizers import spacy_tokenizer

class TestTokenizers(unittest.TestCase):
    nlp: Language = spacy.load("en_core_web_sm")
    nlp.tokenizer = spacy_tokenizer(nlp)

    def test_spacy_tokenizer_case1(self):
        tokenized_data = self.nlp("Hello today is <date>, tomorrow it will be <number> degrees of celcius. I don't like him.")
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
                ".",
                "I",
                "do",
                "n't",
                "like",
                "him",
                "."
            ]
        )

        def test_spacy_tokenizer_case2(self):
            tokenized_data = self.nlp('Punkt wir haben extra um <number> : <number> Uhr noch ein Event')
            self.assertEqual(
                [str(token) for token in tokenized_data],
                [
                    "Punkt",
                    "wir",
                    "haben",
                    "extra",
                    "um",
                    "<number>",
                    ":",
                    "<number>",
                    "be",
                    "<number>",
                    "Uhr",
                    "noch",
                    "ein",
                    "Event"
                ]
            )


if __name__ == '__main__':
    unittest.main()
