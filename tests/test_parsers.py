import os
import unittest
from io import BytesIO

from helper import BASE_DIR

try:
    from src.MordinezNLP.parsers import process_pdf, HTML_Parser
except:
    from MordinezNLP.parsers import process_pdf, HTML_Parser


class ProcessorsTests(unittest.TestCase):
    def test_doc_1(self):
        output = ["Miejsce wystawienia Internet Data wystawienia 08-11-2020 Data sprzedaży 08-11-2020 Sprzedawca " \
                  "Nabywca BMarcin Marcin Borzymowski NIP: 1231230841 NIP: 1231230841 Internetowa 12/3 Internetowa " \
                  "12/4 61-611 Poznań 61-612 Poznań Faktura VAT 01/11/2020 VAT VAT 1 1 2 1 3 1 4 1 W tym 54,68 " \
                  "Razem 54,68 Sposób płatności przelew w terminie 1 dzień Do zapłaty 54,68 PLN Termin płatności " \
                  "09-11-2020 Słownie pięćdziesiąt cztery 68/100 PLN Numer konta 123123123123123123123123 Uwagi: " \
                  "Brak uwag. BMarcin M. Borzymowski M. Borzymowski Podpis osoby upoważnionej do wystawienia Podpis " \
                  "osoby upoważnionej do odbioru Fakturowo.pl Strona 1 / 1"]
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "test_doc_1.pdf"), "rb") as f:
            pdf = BytesIO(f.read())
            pdf_out = process_pdf(pdf)
            self.assertEqual(pdf_out, output)

    def test_doc_2(self):
        output = ["PDF Test File Congratulations, your computer is equipped with a PDF (Portable Document Format) " \
                  "reader! You should be able to view any of the PDF documents and forms available on our site. PDF " \
                  "forms are indicated by these icons: or . Yukon Department of Education Box 2703 Whitehorse,Yukon" \
                  " Canada Y1A 2C6 Please visit our website at: http://www.education.gov.yk.ca/"]
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "test_doc_2.pdf"), "rb") as f:
            pdf = BytesIO(f.read())
            pdf_out = process_pdf(pdf)
            self.assertEqual(pdf_out, output)

    def test_doc_3(self):
        output = ["Example table This is an example of a data table. 5 1 4 5 2 3 5 4 1 3 3 0 "]
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "test_doc_3.pdf"), "rb") as f:
            pdf = BytesIO(f.read())
            pdf_out = process_pdf(pdf)
            self.assertEqual(pdf_out, output)

    def test_html_doc_1(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "html_doc_1_response.txt"), "r", encoding='utf8') as f:
            parsed_doc_ground_truth = f.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "html_doc_1.html"), "r", encoding='utf8') as f:
            parsed_doc = HTML_Parser(f.read())

        self.assertEqual(parsed_doc_ground_truth, parsed_doc)

    def test_html_doc_2(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "html_doc_2_response.txt"), "r", encoding='utf8') as f:
            parsed_doc_ground_truth = f.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "html_doc_2.html"), "r", encoding='utf8') as f:
            parsed_doc = HTML_Parser(f.read())

        self.assertEqual(parsed_doc_ground_truth, parsed_doc)

    def test_html_doc_3(self):
        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "html_doc_3_response.txt"), "r", encoding='utf8') as f:
            parsed_doc_ground_truth = f.read()

        with open(os.path.join(BASE_DIR, "tests", "resources", "test_parsers", "html_doc_3.html"), "r", encoding='utf8') as f:
            parsed_doc = HTML_Parser(f.read())

        self.assertEqual(parsed_doc_ground_truth, parsed_doc)

    # def test_html_doc_4(self):
    #     fake_html_tag = "<html><body>or la<te 80s, 01.03.4223 11-33-3222 or i don>'t know</body></html>"
    #
    #     parsed_html = HTML_Parser(fake_html_tag)
    #
    #     self.assertEqual(parsed_html, fake_html_tag)


if __name__ == '__main__':
    unittest.main()
