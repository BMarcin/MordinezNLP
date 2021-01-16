import io
import time
from itertools import repeat
from multiprocessing import Pool

from typing import List, Iterable, Callable

import requests

try:
    from src.MordinezNLP.downloaders.Processors import text_data_processor, pdf_data_processor
except:
    from .Processors import text_data_processor, pdf_data_processor


class BasicDownloader:
    """
    Class helps to download multiple files from list of provided links using multithreading.
    """

    def __init__(self):
        pass

    @staticmethod
    def download_urls(
            urls: List[str],
            file_type_handler: Callable,
            threads: int = 8,
            sleep_time: int = 0,
            custom_headers: Iterable = repeat({}),
            streamable: Iterable = repeat(False),
            max_retries: int = 10
    ) -> list:
        """
        Function allows user to download files from provided URLs in list. Each file is downloaded as BytesIO using
        specified number of threads and then *file_type_handler* is used to convert file from BytesIO to specified
        format. Each file type should have its own *file_type_handler*.

        Sleep_time is used to prevent sites from detecting DDoS attacks. Before downloading file specified thread
        is going to sleep for specified amount of time.

        Function for each thread (and for each single URL) uses *download_to_bytes_io* function.

        Args:
            urls (List[str]): List of URLs of files to download
            file_type_handler (Callable): Function used to convert downloaded file to a specified format
            threads (int): Number of threads to download files
            sleep_time (int): Time used to prevent file downloads from being detected as DDoS attack
            max_retries (int): Refer to *download_to_bytes_io* function documentation.
            streamable (bool): Refer to *download_to_bytes_io* function documentation.
            custom_headers (int): Refer to *download_to_bytes_io* function documentation.

        Returns:
            list: A list of downloaded and processed by *file_type_handler* function files.
        """
        with Pool(threads) as p:
            downloaded_strings = p.starmap(
                BasicDownloader.download_to_bytes_io, zip(
                    urls,
                    custom_headers,
                    streamable,
                    repeat(sleep_time),
                    repeat(max_retries)
                )
            )
            return [file_type_handler(item) for item in downloaded_strings]

    @staticmethod
    def download_to_bytes_io(
            url: str,
            custom_headers: dict = {},
            streamable: bool = False,
            sleep_time: int = 0,
            max_retries: int = 10,
    ) -> io.BytesIO:
        """
        Function defines how to download single URL. It is used by *download_urls* function to use Threading for
        multithread downloading.

        Function makes GET request to a specified URL. If there is an exception, the function will try to download
        file untill it will be successful or until it reaches 10 unsucessful downloads

        Args:
            max_retries (int): How many retries function will make until it marks a file undownloadable
            sleep_time (int): A sleep time in seconds that is used to prevent sites from detecting downloading as a DDoS attack
            streamable (bool): Sets a *request*'s *stream* parameter. More info https://2.python-requests.org/en/v2.8.1/user/advanced/#body-content-workflow
            custom_headers (bool): Custom headers used in each request
            url (str): valid HTTP/HTTPS URL

        Returns:
            io.BytesIO: downloaded file as a bytes
        """
        # make list from one URL
        url_list = [url]
        retries = 0

        # sleep
        time.sleep(sleep_time)

        # loop until len of list in more than 0
        # it is a loop that try to download file untill it will be successful
        while len(url_list) > 0 and retries < max_retries:
            url_list.pop()

            try:
                retries += 1
                response = requests.get(url, headers=custom_headers, stream=streamable)

                if response.status_code == 200 or response.status_code == 206:
                    io_data = io.BytesIO(response.content)
                    return io_data

            except Exception as e:
                # something went wrong
                # log message and add url to list to try to download it once again
                print(
                    'Retry {retry}. There was an error with url: {url}. {error}. Retrying...'.format(retry=str(retries),
                                                                                                     url=url,
                                                                                                     error=str(e)))
                url_list.append(url)
        return io.BytesIO("".encode())


if __name__ == '__main__':
    # bd = BasicDownloader()

    downloaded_elements = BasicDownloader.download_urls(
        [
            "https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/requirements.txt",
            "https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/LICENSE"
        ],
        lambda x: text_data_processor(x),
    )

    downloaded_pdfs = BasicDownloader.download_urls(
        [
            "https://docs.whirlpool.eu/_doc/19514904100_PL.pdf",
            "https://mpm.pl/docs/_instrukcje/WA-6040S_instrukcja.pdf",
        ],
        lambda x: pdf_data_processor(x)
    )

    print(downloaded_elements)
    print(downloaded_pdfs)
