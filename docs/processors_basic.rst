Processors - Basic
========================

.. automodule:: MordinezNLP.processors.Basic
   :members:

Example usage:

.. code:: python

        from MordinezNLP.processors import BasicProcessor

        bp = BasicProcessor()
        post_process = bp.process("this is my text to process by a funcion", language='en')
        print(post_process)