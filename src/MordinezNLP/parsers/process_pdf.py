from io import BytesIO
from typing import List

import pdfplumber
import re


def process_pdf(pdf_input: BytesIO) -> List[str]:
    """
    A function can read strings from PDF docs handled in the BytesIO object. It extracts whole text and removes text
    that occurs in tables. The reason for that is that tables have mainly messy data for NLP tasks.

    Function is divided into two parts. First removes tokens by exact match and the same number of occurences in text
    and tables. First part uses list of tokens, second uses tokens joined with space.

    Args:
        pdf_input (BytesIO): A PDF as a BytesIO object

    Returns:
        List[str]: Parsed text without texts found in tables
    """
    doc_output = []
    with pdfplumber.open(pdf_input) as pdf:
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            tables = page.extract_tables()

            ' extract words from PDF '
            ' dont use extract_text method because of overlapping '
            ' horizontal and vertical characters '
            text = [item['text'] for item in page.extract_words()]

            table_tokens = []
            ' remove text which is in tables '
            ' first, store texts from table as string '
            for table in tables:
                for row in table:
                    for col in row:
                        if col != ' ' and col != '' and col is not None:
                            for item in col.split("\n"):
                                if len(set(item)) > 1:
                                    table_tokens.append(item)

            unique_table_tokens = list(set(table_tokens))

            # instead of .copy() use [:]
            original_text = text[:]

            ' First part - remove based on token list '
            for token in unique_table_tokens:
                if original_text.count(token) + \
                        original_text.count(token.strip()) == table_tokens.count(token) + \
                        table_tokens.count(token.strip()):
                    original_text = [original_token for original_token in original_text if
                                     token.strip() != original_token.strip()]
                # else:
                #     print(token, original_text.count(token), original_text.count(token.strip()),
                #           table_tokens.count(token), table_tokens.count(token.strip()))

            ' Second part - remove on a str object '
            ' it is good on string that contains several tokens '
            original_text_str = " ".join(original_text)

            for token in unique_table_tokens:
                # print(token, original_text_str.count(token.strip()), table_tokens.count(token.strip()),
                #       table_tokens.count(token))
                if original_text_str.count(token.strip()) == table_tokens.count(token.strip()) or \
                        original_text_str.count(token.strip()) == table_tokens.count(token):
                    original_text_str = original_text_str.replace(token.strip(), " ")

            spaces_regex = re.compile("[\s]{2,}")
            original_text = re.sub(spaces_regex, r" ", original_text_str)

            doc_output.append(original_text)
    return doc_output


if __name__ == '__main__':
    with open("../../../tests/resources/test_parsers/test_doc_3+.pdf", "rb") as f:
        pdf = BytesIO(f.read())
    output = process_pdf(pdf)
    print(output)
