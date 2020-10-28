FROM python:3.8

WORKDIR /

COPY requirements.txt .

RUN pip install --user -r requirements.txt

COPY . /

ENTRYPOINT [ "python" ]

CMD ["app.py"]