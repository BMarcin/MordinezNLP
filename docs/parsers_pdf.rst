Parsers - PDF parser
====================

.. automodule:: MordinezNLP.parsers.process_pdf
   :members:

Example usage for TXT files:

.. code:: python

        from io import BytesIO
        from MordinezNLP.parsers import process_pdf

        with open("my_pdf_doc.pdf", "rb") as f:
               pdf = BytesIO(f.read())
           output = process_pdf(pdf)
           print(output)
