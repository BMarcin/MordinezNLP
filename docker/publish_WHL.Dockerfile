FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python -m pip install --user --upgrade twine && \
    python -m twine upload --repository=${PYPIREPO} whl_package/* --username=__token__ --password=${PYPIPASS}