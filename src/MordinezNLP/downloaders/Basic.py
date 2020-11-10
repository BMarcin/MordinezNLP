import io
import time
import urllib
from itertools import repeat
from multiprocessing import Pool

from typing import List

import requests

from src.MordinezNLP.downloaders import text_data_processor, pdf_data_processor


class BasicDownloader:
    def __init__(self):
        pass

    def download_urls(self, urls: List[str], file_type_handler, threads: int = 8, sleep_time: int = 0) -> list:
        with Pool(threads) as p:
            downloaded_strings = p.starmap(BasicDownloader.download_to_bytes_io, zip(urls, repeat(sleep_time)))
            return [file_type_handler(item) for item in downloaded_strings]

    @staticmethod
    def download_to_bytes_io(
            url: str,
            custom_headers: dict = {},
            streamable: bool = False,
            sleep_time: int = 0,
            max_retries: int = 10
    ) -> io.BytesIO:
        """
        Function makes GET request to a specified URL. If there is an exception function will try to download
        file untill it will be successful.

        Args:
            url (str): valid HTTP/HTTPS URL

        Returns: downloaded file as a string

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
    bd = BasicDownloader()
    # print(bd.download_to_bytes_io("https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/requirements.txt", lambda x: x.read().decode('utf8')))
    downloaded_elements = bd.download_urls(
        [
            "https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/requirements.txt",
            "https://raw.githubusercontent.com/BMarcin/MordinezNLP/main/LICENSE"
        ],
        lambda x: text_data_processor(x),
    )

    downloaded_pdfs = bd.download_urls(
        [
            "https://docs.whirlpool.eu/_doc/19514904100_PL.pdf",
            "https://mpm.pl/docs/_instrukcje/WA-6040S_instrukcja.pdf",
        ],
        lambda x: pdf_data_processor(x)
    )

    print(downloaded_elements)
    print(downloaded_pdfs)
