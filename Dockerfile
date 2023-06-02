FROM python:3.9-slim-buster

WORKDIR /app

# Copie du code source
COPY . .

# Installation des dépendances
RUN apt-get update && \
    apt install -y ffmpeg git curl gcc musl-dev &&  \
    pip install --no-cache-dir poetry==1.4.2 && \
    poetry config virtualenvs.create false --local && \
    poetry install && \
    poetry install opencv-python-headless==4.5.4.58 \
    poetry install numpy==1.19.5 \
    pip uninstall -y poetry && \
    apt remove -y git curl gcc musl-dev && \
    rm -rf /root/.cache/ && \
    rm -rf /usr/local/src/*


# Exécution du script
CMD python detect_animals_v3.py 
