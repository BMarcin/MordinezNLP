import os
import unittest

from helper import BASE_DIR
try:
    from src.MordinezNLP.processors import BasicProcessor
except:
    from MordinezNLP.processors import BasicProcessor


class TestProcessors(unittest.TestCase):
    bp = BasicProcessor()

    def test_doc_1_en(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc1.txt"), encoding="utf8") as f1:
            f1_content = f1.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc1_gt.txt"), encoding="utf8") as f2:
            f1_gt_content = f2.read()

        content_processed = self.bp.process(f1_content, language='en')

        self.assertEqual(content_processed, f1_gt_content)

    def test_doc_2_en(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc2.txt"), encoding="utf8") as f1:
            f1_content = f1.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc2_gt.txt"), encoding="utf8") as f2:
            f1_gt_content = f2.read()

        content_processed = self.bp.process(f1_content, language='en')

        self.assertEqual(content_processed, f1_gt_content)

    def test_doc_3_en(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc3.txt"), encoding="utf8") as f1:
            f1_content = f1.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc3_gt.txt"), encoding="utf8") as f2:
            f1_gt_content = f2.read()

        content_processed = self.bp.process(f1_content, language='en')

        self.assertEqual(content_processed, f1_gt_content)

    def test_doc_4_en(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc4.txt"), encoding="utf8") as f1:
            f1_content = f1.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc4_gt.txt"), encoding="utf8") as f2:
            f1_gt_content = f2.read()

        content_processed = self.bp.process(f1_content, language='en', no_emails=False, no_math=False, no_urls=False)

        self.assertEqual(content_processed, f1_gt_content)

    def test_doc_5_en(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc5.txt"), encoding="utf8") as f1:
            f1_content = f1.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc5_gt.txt"), encoding="utf8") as f2:
            f1_gt_content = f2.read()

        content_processed = self.bp.process(
            f1_content,
            language='en',
            no_multiple_chars=False,
            replace_with_date="<hereisdate>",
            replace_with_bracket="<hereisbracket>",
        )

        self.assertEqual(content_processed, f1_gt_content)

    def test_doc_list_en(self):
        texts_to_process = [
            "Hi! it is my first text written on saturday 16th january 2021",
            "And here is my e-mail: asdfe@sdff.pl",
            "Its a joke ofc",
            "123123 And the last one is 3rd place",
            "Punkt wir haben extra um 05:30 Uhr noch ein Event",
            "GAME FOR SALEIF U AINT GOT THOSE CDS^^^^^^^^^^^^ U better slap",
            "They've been there last year.",
            "ＬＯＵＤ　ＮＯＩＳＥＳ! annnnnnnnnd"
        ]
        texts_gt = [
            "Hi! it is my first text written on <date>",
            "And here is my email: <email>",
            "Its a joke ofc",
            "<number> And the last one is <number> place",
            "Punkt wir haben extra um <number> : <number> Uhr noch ein Event",
            "GAME FOR SALEIF U AINT GOT THOSE CDS U better slap",
            "They have been there last year.",
            "LOUD NOISES! and"
        ]

        processed_texts = self.bp.process(
            texts_to_process,
            language='en'
        )

        self.assertEqual(processed_texts, texts_gt)


if __name__ == '__main__':
    unittest.main()
