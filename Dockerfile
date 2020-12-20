FROM python:3.7-alpine
COPY . /app
WORKDIR /app
RUN apk update && apk add python3-dev \
                        gcc \
                        libc-dev \
                        libffi-dev \
                        libressl-dev \
                        musl-dev
RUN pip install -r requirements.txt
CMD python -u ./updater.py