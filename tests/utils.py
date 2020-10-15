import unittest

from src import ngram_iterator


class UtilsTests(unittest.TestCase):
    def test_ngram_iterator_standard_case_3_chars(self):
        my_token = "<hello>"
        output = ngram_iterator(my_token, 3)
        self.assertEqual(output, ['<he', 'hel', 'ell', 'llo', 'lo>'])

    def test_ngram_iterator_standard_case_2_chars(self):
        my_token = "<hello>"
        output = ngram_iterator(my_token, 2)
        self.assertEqual(output, ['<h', 'he', 'el', 'll', 'lo', 'o>'])

    def test_ngram_iterator_standard_case_4_chars(self):
        my_token = "<hello>"
        output = ngram_iterator(my_token, 4)
        self.assertEqual(output, ['<hel', 'hell', 'ello', 'llo>'])

    def test_ngram_iterator_edge_case_8_chars(self):
        my_token = "<hello>"
        output = ngram_iterator(my_token, 8)
        self.assertEqual(output, ['<hello>'])

    def test_ngram_iterator_edge_case_1_char(self):
        my_token = "<hello>"
        output = ngram_iterator(my_token, 1)
        self.assertEqual(output, ['<', 'h', 'e', 'l', 'l', 'o', '>'])

    def test_ngram_iterator_edge_case_100_chars(self):
        my_token = "<hello>"
        output = ngram_iterator(my_token, 100)
        self.assertEqual(output, ['<hello>'])


***REMOVED***
    unittest.main()
