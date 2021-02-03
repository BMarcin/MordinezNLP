import os
from typing import List, Union, Generator, Tuple, Dict

import spacy
import stanza
from spacy.language import Language
from tqdm import tqdm

try:
    from src.MordinezNLP.tokenizers import spacy_tokenizer
    from src.MordinezNLP.utils import pos_replacement_list, token_replacement_list
except:
    from ..tokenizers import spacy_tokenizer
    from ..utils import pos_replacement_list, token_replacement_list


class PartOfSpeech:
    """
    The aim of the class is to tag each token (which comes from MordinezNLP processors) with its POS tag.
    """

    def __init__(self, nlp: Language, language: str = 'en'):
        """
        Initializer of spacy and stanza models.

        Remember to download Stanza model with ```stanza.download('en')```
        Args:
            nlp (Language): a SpaCy Language object -> You have to load spacy model on Your own
            language (str): a language code from stanza -> see https://stanfordnlp.github.io/stanza/available_models.html
        """
        self.spacy_nlp = nlp
        self.nlp_stanza = stanza.Pipeline(
            lang=language,
            tokenize_pretokenized=True,
            processors='tokenize, pos'
        )

        self.pos_replacement_list = pos_replacement_list
        self.token_replacement_list = token_replacement_list

    def process(
            self,
            texts: List[str],
            threads: int,
            batch_size: int,
            pos_replacement_list: Union[Dict[str, str], None] = None,
            token_replacement_list: Union[Dict[str, str], None] = None,
            return_docs: bool = False
    ) -> Union[Generator[Tuple[List[str], List[str]], None, None], Generator[
        Tuple[List[List[str]], List[List[str]]], None, None]]:
        """
        Main processing function. First step is to tokenize a list of input texts to sentences and then to the tokens.
        Then such input goes to the StanzaNLP.

        For the function List[str] object which comes as an input is a list of docs to process. Each item
        in a list is a document (SpaCy logic in pipelines). In such case You can specify if You want to
        return texts in structure documents[sentences[tokens]] or sentences[tokens] (removing the documents layer).

        Args:
            texts (List[str]): an input texts, each item in a list is a document (SpaCy logic in pipelines)
            threads (int): How many threads You want to use in SpaCy tokenization
            batch_size (int): Batch size for SpaCy tokenizer
            pos_replacement_list (Union[Dict[str, str], None]): If not None function will replace each POS tag
            with value set in value field of the dict. Each key is a POS tag to be replaced by its value.
            token_replacement_list: If not None function will replace each POS tag with the value set in value field of
            the dict. Each key is token, which will be replaced by its value.
            return_docs (bool): If True function will keep a "documents" layer on output.

        Returns:
            Union[Generator[Tuple[List[str], List[str]], None, None], Generator[Tuple[List[List[str]], List[List[str]]],
            None, None]]: a list of doc(if return docs is set) with list of sentences with list of tokens and its pos tags.
        """
        sentences: List[List[str]] = []
        sentence_to_doc_mapping: List[tuple] = []

        function_pos_replacement_list = self.pos_replacement_list if pos_replacement_list is None else pos_replacement_list
        function_token_replacement_list = self.token_replacement_list if token_replacement_list is None else token_replacement_list

        # tokenize
        pipe = self.spacy_nlp.pipe(texts, disable=['ner', 'tagger', 'textcat'], n_threads=threads,
                                   batch_size=batch_size)
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
                if token in function_token_replacement_list.keys():
                    sentence_pos.append(function_token_replacement_list[str(token)])
                else:
                    sentence_pos.append(function_pos_replacement_list[token.upos])
            poss.append(sentence_pos)

        if return_docs:
            for sentence_begin_index, sentence_end_index in sentence_to_doc_mapping:
                yield sentences[sentence_begin_index:sentence_end_index], poss[sentence_begin_index:sentence_end_index]
        else:
            for sentence_id, sentence in enumerate(sentences):
                yield sentence, poss[sentence_id]


if __name__ == '__main__':
    from helper import BASE_DIR

    nlp: Language = spacy.load('en_core_web_sm')
    nlp.tokenizer = spacy_tokenizer(nlp)

    with open(os.path.join(BASE_DIR, "tests", "resources", "test_pipelines", "pos_1.txt"), encoding="utf8") as f1:
        f1_gt_content = f1.read()

    pos_tagger = PartOfSpeech(
        nlp,
        'en'
    )

    pos_output = pos_tagger.process(
        [
            f1_gt_content,
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
        ],
        4,
        30,
        return_docs=True
    )

    for out in pos_output:
        print(out[0], out[1])
