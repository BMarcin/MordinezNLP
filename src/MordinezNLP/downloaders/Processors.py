from io import BytesIO

from ..parsers import process_pdf


def text_data_processor(data: BytesIO) -> str:
    """
    Function can be used together with downloaders to convert BytesIO from text data to str.

    Args:
        data (BytesIO): input data which comes from downloader class/function

    Returns:
        string - which is parsed input
    """
    return data.read().decode('utf8').replace("\r", "")


def pdf_data_processor(data: BytesIO) -> str:
    """
    Function can be used together with downloaders to convert BytesIO from PDF files to str.

    Args:
        data (BytesIO): input data which comes from downloader class/function

    Returns:
        string - which is parsed input, more informations about parsing PDFs can be found in method
        MordinezNLP.parsers.process_pdf
    """
    return process_pdf(data)
