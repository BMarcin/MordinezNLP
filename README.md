<h1 align="center">
MordinezNLP
<h1>

<p align="center">
    <a href="https://github.com/BMarcin/MordinezNLP/blob/main/.github/workflows/tests.yml">
        <img alt="GitHub" src="https://img.shields.io/github/workflow/status/BMarcin/MordinezNLP/Test%20and%20build%20WHL">
    </a>
    <a href="https://github.com/BMarcin/MordinezNLP/blob/main/LICENSE">
        <img alt="GitHub" src="https://img.shields.io/github/license/BMarcin/MordinezNLP">
    </a>
    <a href="https://github.com/BMarcin/MordinezNLP/stargazers">
        <img alt="GitHub" src="https://img.shields.io/github/stars/BMarcin/MordinezNLP?style=social">
    </a>
</p>

<h3 align="center">
    Useful toolkit for NLP projects
</h3>

<p>
MordinezNLP provides tools to download the data from the web, CommonCrawl and ElasticSearch using multiprocessing and custom file processing functions

MordinezNLP has is a powerful tool to clean up dirty texts to make use of them in Neural Networks with better performance.

Use MordinezNLP to extract text data from PDFs (tables ommiting) and from HTMLs.

MordinezNLP is build on top of the SpaCy and Stanza.
</p>

<h3 align="center">Quick tour</h3>
Text cleaning and POS tagging

```python
from MordinezNLP.processors import BasicProcessor
from MordinezNLP.pipelines import PartOfSpeech
from MordinezNLP.tokenizers import spacy_tokenizer
import spacy

nlp = spacy.load("en_core_web_sm")
nlp.tokenizer = spacy_tokenizer(nlp)

bp = BasicProcessor()
post_process = bp.process("this is my text to process by a funcion", language='en')

pos_tagger = PartOfSpeech(
    nlp,
    'en'
)

pos_output = pos_tagger.process(
    [post_process],
    4,
    30,
)
```

CommonCrawl downloader

```python
from MordinezNLP.downloaders import CommonCrawlDownloader

ccd = CommonCrawlDownloader(
    [
        "reddit.com/r/space/*",
        "reddit.com/r/spacex/*",
    ]
)
ccd.download('./test_data')
```

PDF parser

```python
from io import BytesIO
from MordinezNLP.parsers import process_pdf

with open("my_pdf_doc.pdf", "rb") as f:
       pdf = BytesIO(f.read())
   output = process_pdf(pdf)
   print(output)
```


<h3 align="center">
Installation
</h3>

<h4>With pip</h4>

```bash
pip install MordinezNLP
```

<h3 align="center">
URLs
</h3>

- [Docs](https://mordineznlp.readthedocs.io/en/latest/)
- [GitHub](https://github.com/BMarcin/MordinezNLP)
