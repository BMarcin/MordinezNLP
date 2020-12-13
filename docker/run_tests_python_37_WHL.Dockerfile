FROM python:3.7

WORKDIR /usr/src/app

COPY . .
RUN pip install whl_package/*.whl

CMD [ "python", "./test.py" ]