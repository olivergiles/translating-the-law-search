FROM python:3.8.12-buster

RUN python3 -m pip install pip --upgrade pip

#install google chrome
#RUN apt-get update && apt-get install -y curl unzip wget
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
#RUN apt-get -y update

COPY ./requirements.txt /requirements.txt

RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r /requirements.txt

COPY ./data /data
COPY ./streamlit /streamlit

ENTRYPOINT ["streamlit", "run"]

CMD ["/streamlit/app.py"]

EXPOSE 8501
