import io
import os
import threading
import time
from itertools import repeat
from multiprocessing import Pool
from pathlib import Path
from collections import Counter
from pprint import pprint

from typing import List, Iterable, Callable, Union

import requests
from tqdm.auto import tqdm
import base64

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
            sleep_time: float = 0,
            custom_headers: Iterable = repeat({}),
            streamable: Iterable = repeat(False),
            max_retries: int = 10,
            use_memory: bool = True
    ) -> list:
        """
        Function allows user to download files from provided URLs in list. Each file is downloaded as BytesIO using
        specified number of threads and then *file_type_handler* is used to convert file from BytesIO to specified
        format. Each file type should have its own *file_type_handler*.

        Sleep_time is used to prevent sites from detecting DDoS attacks. Before downloading file specified thread
        is going to sleep for specified amount of time.

        Function for each thread (and for each single URL) uses *download_to_bytes_io* function.

        Using *use_memory* user can decide if files will be downloaded to the memory or saved as a temporary files on a
        disk.

        Args:
            urls (List[str]): List of URLs of files to download
            file_type_handler (Callable): Function used to convert downloaded file to a specified format
            threads (int): Number of threads to download files
            sleep_time (int): Time used to prevent file downloads from being detected as DDoS attack
            max_retries (int): Refer to *download_to_bytes_io* function documentation.
            streamable (bool): Refer to *download_to_bytes_io* function documentation.
            custom_headers (int): Refer to *download_to_bytes_io* function documentation.
            use_memory (bool): Downloader can download files to memory or to the binary files. Use memory downloader
            when You know that You will download small amout of data, otherwise set this value to False.

        Returns:
            list: A list of downloaded and processed by *file_type_handler* function files.
        """
        # print('Got {} URLs to download. Starting...'.format(str(len(urls))))

        cc = Counter(urls)
        if any([True for url in cc.keys() if cc[url] != 1]):
            pprint([url for url in cc.keys() if cc[url] != 1])
            raise Exception("There are some duplicates in urls")

        temp_path = Path("./.temp/download-{}".format(time.strftime("%Y%m%d-%H%M%S")))
        if not use_memory:
            temp_path.mkdir(parents=True)
            t1 = threading.Thread(target=BasicDownloader.tqdm_downloading_progress, args=(
                temp_path.absolute(),
                len(urls)
            ))
            t1.start()

        with Pool(threads) as p:
            downloaded_strings = p.starmap(
                BasicDownloader.download_to_bytes_io, zip(
                    urls,
                    repeat(temp_path),
                    repeat(use_memory),
                    custom_headers,
                    streamable,
                    repeat(sleep_time),
                    repeat(max_retries)
                )
            )

        if use_memory:
            # return [file_type_handler(item) for item in downloaded_strings]
            for item in downloaded_strings:
                yield file_type_handler(item)
        else:
            t1.join()

            for file_name in downloaded_strings:
                with open(file_name, "rb") as f:
                    file_content = file_type_handler(f.read())
                os.remove(file_name)
                yield file_content

    @staticmethod
    def tqdm_downloading_progress(
            path: str,
            objects_total: int
    ):
        with tqdm(total=objects_total, desc="Downloading", smoothing=True) as progress:
            current_objects = 0
            while current_objects < objects_total:
                new_current_objects = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
                difference = new_current_objects - current_objects
                if difference > 0:
                    progress.update(difference)
                    current_objects = new_current_objects
                time.sleep(0.3)

    @staticmethod
    def download_to_bytes_io(
            url: str,
            temp_path: str,
            use_memory: bool,
            custom_headers: dict = {},
            streamable: bool = False,
            sleep_time: float = 0,
            max_retries: int = 10,
    ) -> Union[io.BytesIO, Path]:
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
            temp_path (str): A temporary path where downloaded files will be saved (argument used only during in memory download)
            use_memory (bool): When set to *True* script will download all data to the memory. Otherwise it will save
            downloaded data as temporary files on a disk.

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

                    if use_memory:
                        return io_data
                    else:
                        file_path = os.path.join(temp_path, base64.urlsafe_b64encode(url.encode("utf8")).decode("utf8"))
                        with open(file_path, 'wb') as f:
                            f.write(io_data.read())
                        return Path(file_path)
                else:
                    print('Response status code on {} is {}'.format(url, str(response.status_code)))

            except Exception as e:
                # something went wrong
                # log message and add url to list to try to download it once again
                print(
                    'Retry {retry}. There was an error with url: {url}. {error}. Retrying...'.format(retry=str(retries),
                                                                                                     url=url,
                                                                                                     error=str(e)))
                url_list.append(url)

        if use_memory:
            return io.BytesIO("".encode())
        else:
            file_path = os.path.join(temp_path, base64.urlsafe_b64encode(url.encode("utf8")).decode("utf8"))
            with open(file_path, 'wb') as f:
                f.write(b"")
            return Path(file_path)


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
