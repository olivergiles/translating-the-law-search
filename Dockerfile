FROM python:3.8.12-buster

RUN python3 -m pip install pip --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r /requirements.txt

COPY ./streamlit /streamlit
COPY ./.streamlit /.streamlit

ENTRYPOINT ["streamlit", "run"]

CMD ["/streamlit/app.py"]

EXPOSE 8501
