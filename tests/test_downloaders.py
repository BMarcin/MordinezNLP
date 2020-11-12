import os
import unittest
from io import BytesIO

from helper import BASE_DIR
from src.MordinezNLP.downloaders import BasicDownloader
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
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_downloaders", "text_file_1.txt"), "r") as f:
            file_content = text_data_processor(BytesIO(f.read().encode("utf8")))
        self.assertEqual(file_content, self.text_file_1)

    def test_text_file_2(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_downloaders", "text_file_2.txt"), "r") as f:
            file_content = text_data_processor(BytesIO(f.read().encode("utf8")))
        self.assertEqual(file_content, self.text_file_2)


class BasicDownloaderTests(unittest.TestCase):
    def test_txt_file_download(self):
        urls = [
            "https://www.w3.org/TR/PNG/iso_8859-1.txt",
            "https://facebook.com/robots.txt",
            "https://www.bing.com/robots.txt",
            "https://www.w3.org/robots.txt"
        ]

        coresponding_files = [
            os.path.join(BASE_DIR, "tests", "resources", "test_downloaders", "iso_8859-1.txt"),
            os.path.join(BASE_DIR, "tests", "resources", "test_downloaders", "fb_robots.txt"),
            os.path.join(BASE_DIR, "tests", "resources", "test_downloaders", "bing_robots.txt"),
            os.path.join(BASE_DIR, "tests", "resources", "test_downloaders", "w3c_robots.txt")
        ]

        file_contents = []
        for file_name in coresponding_files:
            with open(file_name, encoding="utf8") as f:
                file_contents.append("".join(f.readlines()))

        downloaded_data = BasicDownloader.download_urls(
            urls,
            text_data_processor,
            2
        )

        self.assertEqual(file_contents, downloaded_data)


if __name__ == '__main__':
    unittest.main()
