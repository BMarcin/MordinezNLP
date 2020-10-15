FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python -m pip install --user --upgrade setuptools wheel && \
    python setup.py sdist bdist_wheel && \
    python -m pip install --user --upgrade twine