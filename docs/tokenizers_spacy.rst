Tokenizers - SpacyTokenizer
==============================

.. automodule:: MordinezNLP.tokenizers.spacy_tokenizer
   :members:

Example usage:

.. code:: python

        from MordinezNLP.tokenizers import spacy_tokenizer

        nlp: Language = spacy.load("en_core_web_sm")
        nlp.tokenizer = spacy_tokenizer(nlp)

        test_doc = nlp('Hello today is <date>, tomorrow it will be <number> degrees of celcius.')

        for token in test_doc:
            print(token)

        # output
        # Hello
        # today
        # is
        # <date>
        # ,
        # tomorrow
        # it
        # will
        # be
        # <number>
        # degrees
        # of
        # celcius
        # .
