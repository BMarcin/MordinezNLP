FROM python:3.6

WORKDIR /usr/src/app

COPY . .
RUN pip install -r whl_package/*.whl

CMD [ "python", "./test.py" ]