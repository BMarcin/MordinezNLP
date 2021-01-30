FROM python:3.7

WORKDIR /usr/src/app

COPY . .
RUN pip install whl_package/*.whl

# spacy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm

CMD [ "python", "./test.py" ]