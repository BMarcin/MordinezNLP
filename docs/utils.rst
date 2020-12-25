Utils
===============

.. automodule:: MordinezNLP.utils.ngram_iterator
    :members:

Example usage:

.. code:: python

        from MordinezNLP.utils import ngram_iterator

        print(list(ngram_iterator("<hello>", 3))) # <- will print ['<he', 'hel', 'ell', 'llo', 'lo>']

.. automodule:: MordinezNLP.utils.random_string
    :members:

Example usage:

.. code:: python

        from MordinezNLP.utils import random_string
        import string

        rs = random_string(32)
        print(rs)

        rs = random_string(10, string.digits)
        print(rs)
