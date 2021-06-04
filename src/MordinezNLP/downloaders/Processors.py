import gzip
from io import BytesIO

from ..parsers import process_pdf
# from src.MordinezNLP.parsers import process_pdf


def text_data_processor(data: BytesIO) -> str:
    """
    Function can be used together with downloaders to convert BytesIO from text data to str.

    Args:
        data (BytesIO): input data which comes from downloader class/function

    Returns:
        str: parsed input
    """
    return data.read().decode('utf8').replace("\r", "")


def pdf_data_processor(data: BytesIO) -> str:
    """
    Function can be used together with downloaders to convert BytesIO from PDF files to str.

    Args:
        data (BytesIO): input data which comes from downloader class/function

    Returns:
       str: parsed input, more informations about parsing PDFs can be found in method
        MordinezNLP.parsers.process_pdf
    """
    return "\n".join(process_pdf(data))


def gzip_to_text_data_processor(data: BytesIO) -> str:
    """
    Function can be used together with downloaders to covnert BytesIO to GZIP and unpack it to str.

    Args:
        data (BytesIO): input data which comes from downlaoder class/function

    Returns:
        str: parsed input
    """
    unzipped_file = gzip.GzipFile(fileobj=data)
    raw_data = unzipped_file.read()

    try:
        return raw_data.decode("utf8").replace('\r\n', '\n')
    except UnicodeDecodeError:
        try:
            return raw_data.decode("ascii").replace('\r\n', '\n')
        except UnicodeDecodeError:
            return ""
