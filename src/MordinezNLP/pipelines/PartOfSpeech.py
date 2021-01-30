import os
from pprint import pprint
from typing import List, Union, Generator, Tuple

import spacy
import stanza
from spacy.language import Language
from tqdm import tqdm

from helper import BASE_DIR
from src.MordinezNLP.tokenizers import spacy_tokenizer


class PartOfSpeech:
    def __init__(self, nlp: Language, language: str='en'):
        self.spacy_nlp = nlp
        self.nlp_stanza = stanza.Pipeline(
            lang=language,
            tokenize_pretokenized=True,
            processors='tokenize, pos'
        )

        self.pos_replacement_list = {
            "SYM": "SYM",
            "PUNCT": "PUNCT",
            "X": "X",
            "ADJ": "ADJ",
            "CCONJ": "CCONJ",
            "CONJ": "CONJ",
            "SCONJ": "SCONJ",
            "NUM": "NUM",
            "DET": "DET",
            "PRON": "PRON",
            "ADP": "ADP",
            "VERB": "VERB",
            "PROPN": "PROPN",
            "NOUN": "NOUN",
            "PART": "PART",
            "ADV": "ADV",
            "SPACE": "SPACE",
            "INTJ": "INTJ",
            "AUX": "AUX"
        }

    def process(
            self,
            texts: List[str],
            threads: int,
            batch_size: int,
            return_docs: bool
    ) -> Union[Generator[Tuple[List[str], List[str]], None, None], Generator[Tuple[List[List[str]], List[List[str]]], None, None]]:
        sentences: List[List[str]] = []
        sentence_to_doc_mapping: List[tuple] = []

        # tokenize
        pipe = self.spacy_nlp.pipe(texts, disable=['ner', 'tagger', 'textcat'], n_threads=threads, batch_size=batch_size)
        for doc_num, doc in enumerate(tqdm(pipe, desc='Tokenizing', total=len(texts))):
            sent_begin_index = len(sentences)
            for sent_num, sent in enumerate(doc.sents):
                sentence = [token.text for token in sent]
                sentences.append(sentence)
            sentence_to_doc_mapping.append((sent_begin_index, len(sentences)))

        poss: List[List[str]] = []

        # pos
        stanza_pipe = self.nlp_stanza(sentences)
        for sentence in tqdm(stanza_pipe.sentences, desc='POS tagging'):
            sentence_pos = []
            for token in sentence.words:
                sentence_pos.append(token.upos)
            poss.append(sentence_pos)

        if return_docs:
            for sentence_begin_index, sentence_end_index in sentence_to_doc_mapping:
                yield sentences[sentence_begin_index:sentence_end_index], poss[sentence_begin_index:sentence_end_index]
        else:
            for sentence_id, sentence in enumerate(sentences):
                yield sentence, poss[sentence_id]


if __name__ == '__main__':
    nlp: Language = spacy.load('en_core_web_sm')
    nlp.tokenizer = spacy_tokenizer(nlp)

    with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc2_gt.txt"), encoding="utf8") as f1:
        f1_gt_content = f1.read()

    with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc3_gt.txt"), encoding="utf8") as f2:
        f2_gt_content = f2.read()

    pos_tagger = PartOfSpeech(
        nlp,
        'en'
    )

    pos_output = pos_tagger.process(
        [
            f1_gt_content,
            f2_gt_content
        ],
        4,
        30,
        return_docs=False
    )

    for out in pos_output:
        print(out[0], out[1])

    pos_output = pos_tagger.process(
        [
            f1_gt_content,
            f2_gt_content
        ],
        4,
        30,
        return_docs=True
    )

    for out in pos_output:
        print(out[0], out[1])

