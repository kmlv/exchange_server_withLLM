FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD if [ -z "${SERVER_NAME}"]; then\
        python run_market_server.py; \
    else \
        python run_market_client.py ${OPENAI_API_KEY}; \
    fi