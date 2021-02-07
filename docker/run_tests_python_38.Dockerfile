FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# spacy
RUN python -m spacy download en_core_web_sm
RUN python -m spacy download de_core_news_sm

CMD [ "python", "./test.py" ]