FROM python:3.10.12-slim
WORKDIR /app

COPY Pipfile .

RUN \
  apt update && \
  pip install --upgrade pip && \
  apt install pipenv -y && \
  pipenv install -d && \
  apt autoremove && apt autoclean

ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TZ=Asia/Jakarta

COPY . .