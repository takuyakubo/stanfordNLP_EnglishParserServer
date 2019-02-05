FROM python:3.7.2

RUN mkdir /opt/app

WORKDIR /opt/app

RUN apt-get update && \
     apt-get install -y git && \
     git clone https://github.com/takuyakubo/stanfordNLP_EnglishParserServer.git && \
     cd stanfordNLP_EnglishParserServer && \
     git fetch && \
     git checkout -b feature/add-dockerfile origin/feature/add-dockerfile-univ && \
     pip install --upgrade pip && \
     pip install https://download.pytorch.org/whl/cpu/torch-1.0.0-cp37-cp37m-linux_x86_64.whl && \
     pip install torchvision && \
     pip install stanfordnlp && \
     pip install flask

WORKDIR /opt/app/stanfordNLP_EnglishParserServer

EXPOSE 5020

CMD ["sh", "-c", "python server.py $LANGUAGE"]
