Pipelines - PartOfSpeech
==============================

.. automodule:: MordinezNLP.pipelines.PartOfSpeech
   :members:

Example usage:

.. code:: python

        from MordinezNLP.pipelines import PartOfSpeech
        from MordinezNLP.tokenizers import spacy_tokenizer
        import spacy

        nlp: Language = spacy.load("en_core_web_sm")
        nlp.tokenizer = spacy_tokenizer(nlp)

        docs_to_tag = [
            'Hello today is <date>, tomorrow it will be <number> degrees of celcius.'
        ]

        pos_tagger = PartOfSpeech(
            nlp,
            'en'
        )

        pos_output = pos_tagger.process(
            docs_to_tag,
            4,
            30,
            return_docs=True
        )
