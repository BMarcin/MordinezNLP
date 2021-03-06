import string
import unittest

try:
    from src.MordinezNLP.utils import ngram_iterator, random_string
except:
    from MordinezNLP.utils import ngram_iterator, random_string


class UtilsTests(unittest.TestCase):
    def test_ngram_iterator_standard_case_3_chars(self):
        my_token = "<hello>"
        output = list(ngram_iterator(my_token, 3))
        self.assertEqual(output, ['<he', 'hel', 'ell', 'llo', 'lo>'])

    def test_ngram_iterator_standard_case_2_chars(self):
        my_token = "<hello>"
        output = list(ngram_iterator(my_token, 2))
        self.assertEqual(output, ['<h', 'he', 'el', 'll', 'lo', 'o>'])

    def test_ngram_iterator_standard_case_4_chars(self):
        my_token = "<hello>"
        output = list(ngram_iterator(my_token, 4))
        self.assertEqual(output, ['<hel', 'hell', 'ello', 'llo>'])

    def test_ngram_iterator_edge_case_8_chars(self):
        my_token = "<hello>"
        output = list(ngram_iterator(my_token, 8))
        self.assertEqual(output, ['<hello>'])

    def test_ngram_iterator_edge_case_1_char(self):
        my_token = "<hello>"
        output = list(ngram_iterator(my_token, 1))
        self.assertEqual(output, ['<', 'h', 'e', 'l', 'l', 'o', '>'])

    def test_ngram_iterator_edge_case_100_chars(self):
        my_token = "<hello>"
        output = list(ngram_iterator(my_token, 100))
        self.assertEqual(output, ['<hello>'])

    def test_random_string_generator_case_1(self):
        random_str = random_string(100)
        available_chars = string.ascii_uppercase + string.digits

        is_subset = True

        if len(random_str) == 100:
            for char in random_str:
                if char not in available_chars:
                    is_subset = False
        else:
            is_subset = False

        self.assertEqual(is_subset, True)

    def test_random_string_generator_case_2(self):
        random_str = random_string(50, choices_list=string.ascii_lowercase)
        available_chars = string.ascii_lowercase

        is_subset = True

        if len(random_str) == 50:
            for char in random_str:
                if char not in available_chars:
                    is_subset = False
        else:
            is_subset = False

        self.assertEqual(is_subset, True)


if __name__ == '__main__':
    unittest.main()
