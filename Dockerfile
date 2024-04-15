FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD if [ -z "${SERVER_NAME}"]; then\
        python run_exchange_server.py; \
    else \
        python cda_client.py ${SERVER_NAME}; \
    fi