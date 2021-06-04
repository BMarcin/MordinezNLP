import os
from typing import List, Union, Generator, Tuple, Dict

import spacy
import stanza
from spacy.language import Language
from spacy.tokens import Token
from tqdm.auto import tqdm

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
        self.nlp_stanza = None

        self.language = language

        self.pos_replacement_list = pos_replacement_list
        self.token_replacement_list = token_replacement_list

        modules_to_disable = [
            # 'tok2vec',
            # 'parser',
            'ner',
            'attribute_ruler',
            'lemmatizer',
        ]

        for module in modules_to_disable:
            self.spacy_nlp.disable_pipe(module)

    def process(
            self,
            texts: List[str],
            tokenizer_threads: int = 8,
            tokenizer_batch_size: int = 50,
            pos_batch_size: int = 3000,
            pos_replacement_list: Union[Dict[str, str], None] = None,
            token_replacement_list: Union[Dict[str, str], None] = None,
            return_docs: bool = False,
            return_string_tokens: bool = False
    ) -> Union[Generator[Tuple[List[Union[Token, str]], List[str]], None, None], Generator[
        Tuple[List[List[Union[Token, str]]], List[List[str]]], None, None]]:
        """
        Main processing function. First step is to tokenize a list of input texts to sentences and then to the tokens.
        Then such input goes to the StanzaNLP.

        For the function List[str] object which comes as an input is a list of docs to process. Each item
        in a list is a document (SpaCy logic in pipelines). In such case You can specify if You want to
        return texts in structure documents[sentences[tokens]] or sentences[tokens] (removing the documents layer).

        Sometimes You want to force POS tagger to assign POS tag to a specified token or instead of other POS tag. For
        such cases You can use *pos_replacement_list* and *token_replacement_list*. You can import sample token and POS
        replacement lists from MordinezNLP.utils.pos_replacement_list and MordinezNLP.utils.token_replacement_list.

        If You want to use a special attributes for each tokens from SpaCy please pass *False* as a value of *return_string_tokens*
        argument.

        Each token parsed by SpaCy tokenizer will by converted to its normal version. For example each *n't* will be replaced
        by *not*.

        Args:
            texts (List[str]): an input texts, each item in a list is a document (SpaCy logic in pipelines)
            tokenizer_threads (int): How many threads You want to use in SpaCy tokenization
            tokenizer_batch_size (int): Batch size for SpaCy tokenizer
            pos_batch_size (int) = Batch size for Stanza POS tagger (if enabled). Be careful! It uses GPU if cuda is available in Your system.
            pos_replacement_list (Union[Dict[str, str], None]): If not None function will replace each POS tag
            with value set in value field of the dict. Each key is a POS tag to be replaced by its value.
            token_replacement_list: If not None function will replace each POS tag with the value set in value field of
            the dict. Each key is token, which will be replaced by its value.
            return_docs (bool): If True function will keep a "documents" layer on output.
            return_string_tokens (bool): Function can return tokens as SpaCy Token object (if You need to access token
            specified data such as norm_) or can return tokens as a string object. If True returns a string tokens.

        Returns:
            Union[Generator[Tuple[List[Union[Token, str]], List[str]], None, None], Generator[Tuple[List[List[Union[Token, str]]], List[List[str]]],
            None, None]]: a list of doc(if return docs is set) with list of sentences with list of tokens and its pos tags.
        """
        sentences: List[List[str]] = []
        sentence_to_doc_mapping: List[tuple] = []

        function_pos_replacement_list = self.pos_replacement_list if pos_replacement_list is None else pos_replacement_list
        function_token_replacement_list = self.token_replacement_list if token_replacement_list is None else token_replacement_list

        # stanza
        if self.nlp_stanza is None:
            self.nlp_stanza = stanza.Pipeline(
                lang=self.language,
                tokenize_pretokenized=True,
                processors='tokenize, pos',
                pos_batch_size=pos_batch_size,
                logging_level='CRITICAL'
            )

        # tokenize
        pipe = self.spacy_nlp.pipe(
            texts,
            n_process=tokenizer_threads,
            batch_size=tokenizer_batch_size
        )

        raw_sentences_with_tokens: List[List[Token]] = []

        for doc_num, doc in enumerate(tqdm(pipe, desc='Tokenizing', total=len(texts))):
            sent_begin_index = len(sentences)
            for sent_num, sent in enumerate(doc.sents):
                sentence = []
                raw_sentence_tokens = []

                for i, token in enumerate(sent):
                    if token.norm_ != 'not':
                        sentence.append(token.text)
                    else:
                        if i == 0:
                            sentence.append(token.text)
                        else:
                            sentence.append(token.norm_)

                    raw_sentence_tokens.append(token)

                sentences.append(sentence)
                raw_sentences_with_tokens.append(raw_sentence_tokens)
            sentence_to_doc_mapping.append((sent_begin_index, len(sentences)))

        poss: List[List[str]] = []

        # pos
        print('POS tagging data, it can take up to couple hours, but also it can take just a seconds, everything '
              'depends how much data You feed.')
        stanza_pipe = self.nlp_stanza(sentences)
        for sentence in stanza_pipe.sentences:
            sentence_pos = []
            for token in sentence.words:
                if str(token.text) in function_token_replacement_list.keys():
                    # print('tag replacement', token, function_token_replacement_list[token.text])
                    sentence_pos.append(function_token_replacement_list[token.text])
                else:
                    sentence_pos.append(function_pos_replacement_list[token.upos])
            poss.append(sentence_pos)

        if return_docs:
            for sentence_begin_index, sentence_end_index in sentence_to_doc_mapping:
                if return_string_tokens:
                    yield sentences[sentence_begin_index:sentence_end_index], poss[sentence_begin_index:sentence_end_index]
                else:
                    yield raw_sentences_with_tokens[sentence_begin_index:sentence_end_index], poss[sentence_begin_index:sentence_end_index]
        else:
            if return_string_tokens:
                for sentence_id, sentence in enumerate(sentences):
                    yield sentence, poss[sentence_id]
            else:
                for sentence_id, sentence in enumerate(raw_sentences_with_tokens):
                    yield sentence, poss[sentence_id]


if __name__ == '__main__':
    from helper import BASE_DIR

    nlp: Language = spacy.load('en_core_web_sm')
    nlp.tokenizer = spacy_tokenizer(nlp)

    # with open(os.path.join(BASE_DIR, "tests", "resources", "test_pipelines", "pos_1.txt"), encoding="utf8") as f1:
    #     f1_gt_content = f1.read()

    pos_tagger = PartOfSpeech(
        nlp,
        'en'
    )

    pos_output = pos_tagger.process(
        [
            "Hello today is <date>, tomorrow it will be <number> degrees of celcius. Remember, to dont touch the glass. It was Mike's car. Not now please.",
        ],
        4,
        30,
        return_docs=False
    )

    for out in pos_output:
        print(out[0], out[1])

    # pos_output = pos_tagger.process(
    #     [
    #         f1_gt_content,
    #     ],
    #     4,
    #     30,
    #     return_docs=True
    # )
    #
    # for out in pos_output:
    #     print(out[0], out[1])
