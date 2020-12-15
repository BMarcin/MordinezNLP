Downloaders - CommonCrawl
==========================

.. automodule:: MordinezNLP.downloaders.CommonCrawlDownloader
   :members:

Example usage:

.. code:: python

        from MordinezNLP.downloaders import CommonCrawlDownloader

        ccd = CommonCrawlDownloader(
            [
                "reddit.com/r/space/*",
                "reddit.com/r/spacex/*",
            ]
        )
        ccd.download('./test_data')