import json
import os
import unittest

import spacy
from spacy.language import Language

from helper import BASE_DIR

try:
    from src.MordinezNLP.pipelines import PartOfSpeech
    from src.MordinezNLP.tokenizers import spacy_tokenizer
except:
    from MordinezNLP.pipelines import PartOfSpeech
    from MordinezNLP.tokenizers import spacy_tokenizer

class TestPipelines(unittest.TestCase):
    nlp: Language = spacy.load("en_core_web_sm")
    nlp.tokenizer = spacy_tokenizer(nlp)

    def test_pos_pipeline_case1(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_pipelines", "pos_1.txt"), encoding="utf8") as f:
            to_process_content = f.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_pipelines", "pos_1_gt.json"), encoding="utf8") as f2:
            gt = json.loads(f2.read())

        pos_tagger = PartOfSpeech(
            self.nlp,
            'en'
        )

        pos_output = pos_tagger.process(
            [to_process_content],
            4,
            30,
            return_docs=False
        )

        outputs = []
        for sentence, sentence_pos in pos_output:
            outputs.append([sentence, sentence_pos])

        pos_output = pos_tagger.process(
            [to_process_content],
            4,
            30,
            return_docs=True
        )

        docs = []
        for doc in pos_output:
            docs.append(doc)

        gt_sentences = []
        gt_poss = []
        for sentence, sentence_pos in gt['sentences']:
            gt_sentences.append(sentence)
            gt_poss.append(sentence_pos)

        self.assertEqual([outputs, docs], [gt['sentences'], [(gt_sentences, gt_poss)]])


if __name__ == '__main__':
    unittest.main()
