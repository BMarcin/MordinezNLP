import unittest
from io import BytesIO

from src.MordinezNLP.downloaders.Processors import text_data_processor


class ProcessorsTests(unittest.TestCase):
    text_file_1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vestibulum malesuada " \
                            "ligula, vel elementum metus sodales et. Pellentesque varius nulla ullamcorper ex " \
                            "vulputate, at fermentum ex tempus. Donec leo elit, suscipit et facilisis non, vestibulum" \
                            " et nunc. Curabitur eu elit nibh. Sed dui purus, aliquet a neque quis, convallis " \
                            "finibus erat. Quisque in aliquam diam. Etiam eu ante et est volutpat vestibulum. " \
                            "Donec quis aliquet justo. Duis sollicitudin massa ut mauris malesuada, ac rhoncus " \
                            "leo posuere."

    text_file_2 = """This is my multiline file.

It contains special characters like: ąęźżćłó;@!#G:SDFGMN"};l.;,`13/-+
and also german: äöüß"""

    def test_text_file_1(self):
        with open('tests/resources/test_parsers/text_file_1.txt', "r", encoding="utf8") as f:
            file_content = text_data_processor(BytesIO(f.read().encode("utf8")))
        self.assertEqual(file_content, self.text_file_1)

    def test_text_file_2(self):
        with open('tests/resources/test_parsers/text_file_2.txt', "r", encoding="utf8") as f:
            file_content = text_data_processor(BytesIO(f.read().encode("utf8")))
        self.assertEqual(file_content, self.text_file_2)


if __name__ == '__main__':
    unittest.main()
