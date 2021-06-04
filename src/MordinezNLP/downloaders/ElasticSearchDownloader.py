from multiprocessing import Pool
from typing import List, Iterable, Callable, Any, Union

from elasticsearch import Elasticsearch
from tqdm.auto import tqdm

try:
    from src.MordinezNLP.parsers import HTML_Parser
except:
    from ..parsers import HTML_Parser


class ElasticSearchDownloader:
    """
    Class used to download elastic search data from specified index using multithreading
    todo make tests
    """

    def __init__(self, ip: str, port: int, api_key_1: str = None, api_key_2: str = None, timeout: int = 100):
        """
        Save elastic search connection data to class variables.

        Args:
            ip (str): elastic search IP
            port (int): elastic search port
            timeout (int): elastic search connection timeout
            api_key_1 (str): First api key generated in Elastic
            api_key_2 (str): Second api key generated in Elastic
        """
        self.ip: str = ip
        self.port: int = port

        self.api_key_1 = api_key_1
        self.api_key_2 = api_key_2

        self.client = ElasticSearchDownloader._get_es_connection(
            ip=ip,
            port=port,
            timeout=timeout,
            api_key=(
                self.api_key_1,
                self.api_key_2
            )
        )

    @staticmethod
    def _get_es_connection(ip: str, port: int, timeout: int, api_key: tuple) -> Elasticsearch:
        """
        Build elastic search connection.

        Args:
            ip (str): elastic search IP
            port (int): elastic search port
            timeout (int): elastic search connection timeout
            api_key (tuple): api_keys for elastic connection

        Returns:
            Elasticsearch: elasti search client connection
        """

        if api_key[0] is None and api_key[1] is None:
            return Elasticsearch(
                hosts=ip,
                port=port,
                timeout=timeout
            )
        else:
            return Elasticsearch(
                hosts=ip,
                port=port,
                api_key=api_key,
                timeout=timeout
            )

    def get_all_available_indexes(self) -> List[str]:
        """
        Get all available elastic search indexes.

        Returns:
            List[str]: a list of string where each element is a elastic search index name
        """
        return [
            index for index in self.client.indices.get_alias().keys()
        ]

    @staticmethod
    def _multithreaded_processing(
            processing_function: Callable[[dict], Any],
            args: Iterable,
            threads: int = 6
    ) -> List[any]:
        """
        A threading wrapper for processing list

        Args:
            processing_function (Callable[[dict], Any]): A function which will be used to process single document downloaded from elastic search
            args (Iterable): Arguments redirected to the *processing_function*
            threads (int): Number of threads to process documents

        Returns:
            Any: Returns a processed item according to a return type and item from *processing_function*
        """
        with Pool(threads) as p:
            return p.starmap(
                processing_function,
                args
            )

    def scroll_data(
            self,
            index_name: str,
            query: dict,
            processing_function: Callable[[dict], Any],
            threads: int = 6,
            scroll: str = '2m',
            scroll_size: int = 100

    ) -> List[any]:
        """
        A function that scrolls through an elastic search data from index and returns a multithreaded data processed with *processing_function*.
        It returns a List of types returned by a *processing_function*.

        Args:
            index_name (str): An index name to scroll/download the data
            query (dict): An elastic search query
            processing_function (Callable[[dict], Any]): A function that processes single item from elastic search index
            threads (int): A number of threads to run processing on
            scroll (str): A scroll value
            scroll_size (int): A size of scrolling items at once

        Returns:
            List[any]: Returns a list of processed items with type according to a *processing_function* or empty list if index doesn't exists.
        """
        if self.client.indices.exists(index_name):
            processed_docs = []

            total_docs = self.client.count(
                index=index_name,
                body=query
            )

            print('Found {} docs, processing...'.format(str(total_docs['count'])))
            progress = tqdm(desc='Processing', total=total_docs['count'])

            data = self.client.search(
                index=index_name,
                scroll=scroll,
                size=scroll_size,
                body=query
            )

            processed_docs += ElasticSearchDownloader._multithreaded_processing(
                processing_function=processing_function,
                args=zip(
                    data['hits']['hits']
                ),
                threads=threads
            )

            progress.update(scroll_size)

            scroll_id = data['_scroll_id']
            scroll_size = len(data['hits']['hits'])

            while scroll_size > 0:
                data = self.client.scroll(
                    scroll_id=scroll_id,
                    scroll=scroll
                )

                processed_docs += ElasticSearchDownloader._multithreaded_processing(
                    processing_function=processing_function,
                    args=zip(
                        data['hits']['hits']
                    ),
                    threads=threads
                )

                scroll_id = data['_scroll_id']
                scroll_size = len(data['hits']['hits'])

                progress.update(scroll_size)
            return processed_docs
        else:
            print('{} doesn\'t exists'.format(index_name))
            return []


if __name__ == '__main__':
    es = ElasticSearchDownloader(
        ip='',
        port=9200,
        timeout=10
    )

    print(es.get_all_available_indexes())

    body = {}

    ' Your own processing function for a single element '
    def processing_func(data: dict) -> str:
        if 'en' in data['_source']:
            if 'content' in data['_source']['en']:
                content = " ".join(part['content'] for part in data['_source']['en']['content'])
                parsed = HTML_Parser(content, separator='... \n')
                print(parsed)
                return parsed
        return ""


    ' Scroll the data '
    downloaded_elastic_search_data = es.scroll_data(
        '',
        body,
        processing_func,
        threads=8,
        scroll_size=300
    )

    print(len(downloaded_elastic_search_data))

    print(downloaded_elastic_search_data[:3])
