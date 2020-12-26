Downloaders - Elastic Search
==========================

.. automodule:: MordinezNLP.downloaders.ElasticSearchDownloader
   :members:

Example usage:

.. code:: python

        from MordinezNLP.downloaders import ElasticSearchDownloader

        es = ElasticSearchDownloader(
            ip='',
            port=9200,
            timeout=10
        )

        body = {}  # <- use your own elastic search query

        ' Your own processing function for a single element '
        def processing_func(data: dict) -> str:
            return data['my_key']['my_next_key'].replace("\r\n", "\n")


        ' Scroll the data '
        downloaded_elastic_search_data = es.scroll_data(
            'my_index_name',
            body,
            processing_func,
            threads=8
        )

        print(len(downloaded_elastic_search_data))