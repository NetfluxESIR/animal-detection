FROM python:3.10.11-bullseye
WORKDIR /app
COPY . .
RUN apt-get update && \
    apt install -y ffmpeg git curl gcc musl-dev &&  \
    pip install --no-cache-dir poetry==1.4.2 && \
    poetry config virtualenvs.create false --local && \
    poetry install && \
    pip uninstall -y poetry && \
    apt remove -y git curl gcc musl-dev && \
    rm -rf /root/.cache/ && \
    rm -rf /usr/local/src/*
ENTRYPOINT ["python", "app.py"]
