Downloaders - Basic
========================

.. automodule:: MordinezNLP.downloaders.Basic
   :members:

Example usage for TXT files:

.. code:: python

        from MordinezNLP.downloaders import BasicDownloader
        from MordinezNLP.downloaders.Processors import text_data_processor

        downloaded_elements = BasicDownloader.download_urls(
            [
                "https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/requirements.txt",
                "https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/LICENSE"
            ],
            lambda x: text_data_processor(x),
        )

        print(downloaded_elements) # <- will display a list with elements where each is a content of a downloaded files

Example usage for PDF files:

.. code:: python

        from MordinezNLP.downloaders import BasicDownloader
        from MordinezNLP.downloaders.Processors import pdf_data_processor

        downloaded_pdfs = BasicDownloader.download_urls(
            [
                "https://docs.whirlpool.eu/_doc/19514904100_PL.pdf",
                "https://mpm.pl/docs/_instrukcje/WA-6040S_instrukcja.pdf",
            ],
            lambda x: pdf_data_processor(x)
        )

        print(downloaded_pdfs) # <- will display a list with elements where each is a content of a downloaded files