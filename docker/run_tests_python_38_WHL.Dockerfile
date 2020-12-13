FROM python:3.8

WORKDIR /usr/src/app

COPY . .
RUN pip install whl_package/*.whl

CMD [ "python", "./test.py" ]