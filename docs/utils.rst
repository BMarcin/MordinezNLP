Utils
===============

.. automodule:: MordinezNLP.utils.ngram_iterator
    :members:

Example usage:

.. code:: python

        from MordinezNLP.utils import ngram_iterator

        print(list(ngram_iterator("<hello>", 3))) # <- will print ['<he', 'hel', 'ell', 'llo', 'lo>']