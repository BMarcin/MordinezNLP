import json
import os
import urllib.parse
from io import BytesIO
from itertools import repeat
from typing import List

try:
    from src.MordinezNLP.downloaders.Processors import text_data_processor, gzip_to_text_data_processor
    from src.MordinezNLP.downloaders import BasicDownloader
except:
    from .Basic import BasicDownloader
    from .Processors import text_data_processor


# todo add docs
class CommonCrawlDownloader:
    def __init__(
            self,
            links_to_search: List[str],
            index_name: str = "CC-MAIN-2020-24",
            base_index_url: str = "http://index.commoncrawl.org",
            search_for_mime: str = 'text/html',
            search_for_language: str = 'eng',
            threads=8
    ):
        self.links_to_search = links_to_search
        self.index_name = index_name
        self.base_index_url = base_index_url
        self.search_for_mime = search_for_mime
        self.search_for_language = search_for_language
        self.threads = threads

        self.entries_to_download = self._get_sources_for_urls()

    def _get_sources_for_urls(self):
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
            text_data_processor
        )

        # parse downloaded contents
        entries_to_download = []
        for response_content in downloaded_content:
            for line in response_content.split("\n"):
                if len(line) > 10:
                    parsed_item = json.loads(line)
                    if 'mime-detected' in parsed_item.keys() and 'status' in parsed_item.keys() and \
                            'languages' in parsed_item.keys():
                        if parsed_item['mime-detected'] == self.search_for_mime and parsed_item['status'] == "200" \
                                and parsed_item['languages'] == self.search_for_language:
                            entries_to_download.append(parsed_item)
        return entries_to_download

    @staticmethod
    def _custom_gzip_to_text_processor(data_in: BytesIO) -> str:
        return gzip_to_text_data_processor(data_in).strip().split("\r\n\r\n", 2)[2]

    def download(self, save_to: str, base_url: str = "https://commoncrawl.s3.amazonaws.com", sleep_time: int = 0):
        entries_to_download = []

        for entry in self.entries_to_download:
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

            entries_to_download.append(entry_dict)

        ' download data '
        bd = BasicDownloader()
        downloaded_content = bd.download_urls(
            [entry['url'] for entry in entries_to_download],
            CommonCrawlDownloader._custom_gzip_to_text_processor,
            custom_headers=[entry['headers'] for entry in entries_to_download],
            streamable=repeat(True)
        )

        if not os.path.exists(save_to):
            os.mkdir(save_to)

        for filename, entry in zip([entry['save_to'] for entry in entries_to_download], downloaded_content):
            with open(os.path.join(save_to, filename), "w", encoding="utf8") as f:
                f.write(entry)


if __name__ == '__main__':
    ccd = CommonCrawlDownloader(
        [
            "reddit.com/r/space/*",
            "reddit.com/r/spacex/*",
        ]
    )
    ccd.download('./test_data')
