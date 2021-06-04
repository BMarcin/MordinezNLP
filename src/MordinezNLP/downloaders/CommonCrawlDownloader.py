import io
import json
import os
import time
import urllib.parse
from io import BytesIO
from itertools import repeat
from typing import List
from tqdm.auto import tqdm

try:
    from src.MordinezNLP.downloaders.Processors import text_data_processor, gzip_to_text_data_processor
    from src.MordinezNLP.downloaders import BasicDownloader
except:
    from .Basic import BasicDownloader
    from .Processors import text_data_processor, gzip_to_text_data_processor


class CommonCrawlDownloader:
    """
    Class used to download common crawl data using Basic multithreaded downloader.
    """

    def __init__(
            self,
            links_to_search: List[str],
            index_name: str = "CC-MAIN-2020-24",
            base_index_url: str = "http://index.commoncrawl.org",
            search_for_mime: str = 'text/html',
            search_for_language: str = 'eng',
            threads: int = 8
    ):
        """
        Common Crawl initializer. Downloading data is divided in to two stages.

        Stage 1: Collect metadata that describes which GZIP archives and from to which byte contains a text data for which
        we are looking for

        Stage 2: Download bytes (from start byte to end byte) of GZIP archive and parse it to the text.

        Initializer starts first stage.

        Args:
            links_to_search (List[str]): a list of string which are a URL to search in common crawl search index. For example You can search for a https://reddit.com/spacex/* and * matches all cases.
            index_name (str): a common crawl index name for example: CC-MAIN-2020-24 (default value)
            base_index_url (str): a common crawl index url for example: http://index.commoncrawl.org (default value)
            search_for_mime (str): a mimetype we are searching for (default is: text/html)
            search_for_language (str): a language we are searching for (default is: 'eng'). Please follow CC documentation to find a right language string
            threads (int): number of threads to run the BaseDownloader on
        """
        self.links_to_search: List[str] = links_to_search
        self.index_name: str = index_name
        self.base_index_url: str = base_index_url
        self.search_for_mime: str = search_for_mime
        self.search_for_language: str = search_for_language
        self.threads: int = threads

        self.entries_to_download: List[dict] = self._get_sources_for_urls()

    def _get_sources_for_urls(self) -> List[dict]:
        """
        This is stage 1 of CommonCrawl Downloader. Function gets metadata from CommonCrawl for source GZIP files

        Returns:
            List[dict]: Each dict is a CC metadata.
        """
        # preprocess links to use BasicDownloader
        post_processed_urls = []
        for url in self.links_to_search:
            pre_url = urllib.parse.quote(url, safe='')
            post_url = "{base_url}/{index_name}-index?url={pre_url}&output=json".format(
                base_url=self.base_index_url,
                index_name=self.index_name,
                pre_url=pre_url
            )
            post_processed_urls.append(post_url)

        # use basic downloader to download CommonCrawl Indexes
        bd = BasicDownloader()
        downloaded_content = bd.download_urls(
            post_processed_urls,
            text_data_processor,
            use_memory=True,
            sleep_time=0.4,
            threads=2
        )

        # parse downloaded contents
        entries_to_download = []
        for response_content in tqdm(downloaded_content, desc="Processing URLs to download",
                                     total=len(post_processed_urls)):
            for line in response_content.split("\n"):
                if len(line) > 10:
                    parsed_item = json.loads(line)
                    if 'mime-detected' in parsed_item.keys() and 'status' in parsed_item.keys() and \
                            'languages' in parsed_item.keys():
                        if parsed_item['mime-detected'] == self.search_for_mime and (parsed_item['status'] == "200"
                                                                                     or parsed_item[
                                                                                         'status'] == "301") and \
                                parsed_item['languages'] == self.search_for_language:
                            entries_to_download.append(parsed_item)
        return entries_to_download

    @staticmethod
    def _common_crawl_gzip_to_text_processor(data_in: bytes) -> str:
        """
        Function is a wrapper for *gzip_to_text_data_processor*. For CC gzips we need to remove crawler metadata, so function strips, splits data and returs just a crawled html source.

        Args:
            data_in (bytes): a downloaded bytes

        Returns:
            str: Source html of crawled site.
        """
        gzipped_data = gzip_to_text_data_processor(io.BytesIO(data_in))
        try:
            return gzipped_data.strip().split("\n\n", 2)[2]
        except IndexError:
            return ""

    def download(self, save_to: str, base_url: str = "https://commoncrawl.s3.amazonaws.com", sleep_time: float = 0):
        """
        Main function used to download CC data using multithreaded Base Downloader.

        Args:
            save_to (str): path to a folder where the data will be downloaded. Each file is a HTML document downloaded from CC.
            base_url (str):  base CC URL for example: https://commoncrawl.s3.amazonaws.com
            sleep_time (int):  A sleep time in seconds that is used to prevent sites from detecting downloading as a DDoS attack
        """
        entries_to_download = []
        urls = []

        for entry in tqdm(self.entries_to_download, desc="Extracting metadata of source URLs"):
            filename = entry['filename']
            offset = int(entry['offset'])
            length = int(entry['length'])

            offset_end = offset + length - 1

            headers = {
                "Range": "bytes={start}-{end}".format(start=str(offset), end=str(offset_end))
            }

            filename_to_save_entry = "{filename}-{offset}-{offset_end}.txt".format(
                filename=filename.split("/")[-1].split(".")[0],
                offset=offset,
                offset_end=offset_end
            )

            entry_dict = {
                'url': "{}/{}".format(base_url, filename),
                'headers': headers,
                'save_to': filename_to_save_entry
            }

            if entry_dict['url'] not in urls:
                entries_to_download.append(entry_dict)
                urls.append(entry_dict['url'])

        if not os.path.exists(save_to):
            os.mkdir(save_to)

        ' download data '
        bd = BasicDownloader()
        downloaded_content = bd.download_urls(
            urls,
            CommonCrawlDownloader._common_crawl_gzip_to_text_processor,
            custom_headers=[entry['headers'] for entry in entries_to_download],
            streamable=repeat(True),
            sleep_time=sleep_time,
            threads=self.threads,
            use_memory=False
        )

        # with tqdm(desc='Saving', total=len(urls)) as progress:
        for filename, entry in zip([entry['save_to'] for entry in entries_to_download], downloaded_content):
            with open(os.path.join(save_to, filename), "w", encoding="utf8") as f:
                f.write(entry)
                # progress.update()


if __name__ == '__main__':
    ccd = CommonCrawlDownloader(
        [
            "en.wikipedia.org/*",
            "reddit.com/r/space/*",
            "reddit.com/r/spacex/*",
            "medium.com/*",
            "steemit.com/*",
            "quora.com/*",
            "write.as/*",
            "newsbreak.com/*",
            "hubpages.com/*",
            "amazon.com/*",
            "*.blog/*",
            "cnn.com/*",
            "*.cnn.com",
            "bbc.com/*",
            "nytimes.com/*",
            "dailymail.co.uk/*",
            "theguardian.com/*",
            "foxnews.com/*",
            "washingtonpost.com/*",
            "cnbc.com/*",
            "forbes.com/*",
            "telegraph.co.uk/*",
            "independent.co.uk/*",
            "mirror.co.uk/*",
            "thesun.co.uk/*",
            "metro.co.uk/*",
            "ebay.com/*",
            "thelondoner.me/*",
            "deliciouslyella.com/*",
            'bbc.co.uk/*',
            'worldofwanderlust.com/*',
            'handluggageonly.co.uk/*',
            'ef.com/*',
            'emilyluxton.co.uk/*',
            'avoirthere.com/*',
            'luxurycolumnist.com/*',
            'thetravelhack.com/*',
            'globalhelpswap.com/*',
            'thisbatteredsuitcase.com/*',
            'theblondeabroad.com/*',
            'twowanderingsoles.com/*',
            'prusa3d.com/*',
            'arxiv.org/*',
            'pizzahut.com/*',
            'design-milk.com/*',
            'moderndogmagazine.com/*',
            'pupstyle.com/*',
            '*.co.uk',
            '*.blog',
            '*blog*',
            'reddit.com/r/spacex/*',
            'reddit.com/r/medicine/*',
            'reddit.com/r/space/*',
            'reddit.com/r/biology/*',
            'reddit.com/r/Physics/*'
        ],
        threads=32,
        index_name='CC-MAIN-2021-21'
    )
    ccd.download('./test_data', sleep_time=0.05)
