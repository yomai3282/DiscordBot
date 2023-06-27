FROM python:3.9 as builder
WORKDIR /bot
RUN apt update -y && \
    apt upgrade -y
COPY ./app/Pipfile ./app/Pipfile.lock /bot/
RUN pip install pipenv==2022.10.25 pytest && \
    pipenv install --system

FROM python:3.9-slim
WORKDIR /bot
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y nodejs npm curl && \
    npm install -g n && \
    n stable && \
    apt purge -y nodejs npm && \
    apt install -y ffmpeg && \
    apt autoremove -y
RUN npm install -g nodemon

ENV PYTHONBUFFERED=1
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

COPY . /bot
