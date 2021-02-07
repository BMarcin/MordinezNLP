import os
from pprint import pprint

import spacy
import stanza
from spacy.language import Language

from helper import BASE_DIR
from src.MordinezNLP.tokenizers import spacy_tokenizer

if __name__ == '__main__':
    with open(os.path.join(BASE_DIR, "tests", "resources", "test_processors", "doc2_gt.txt"), encoding="utf8") as f2:
        f1_gt_content = f2.read()

    nlp: Language = spacy.load('en_core_web_sm')
    nlp.tokenizer = spacy_tokenizer(nlp)

    doc = nlp("And here is my email: <email>")

    tokens = [[str(token) for token in sentence] for sentence in doc.sents]
    pprint(tokens)

    nlp_stanza = stanza.Pipeline(lang='en', tokenize_pretokenized=True, processors='tokenize, pos')
    # nlp.tokenizer = spacy_tokenizer(nlp)
    #
    doc = nlp_stanza(tokens)

    for document in doc.sentences:
        for token in document.words:
            print(token.text, token.upos)