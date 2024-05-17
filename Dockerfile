FROM python:3.10

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
# COPY . /app

RUN pip install -r requirements.txt

ADD . /app

CMD if [ -z "${SERVER_NAME}"]; then\
        python run_market_server.py; \
    else \
        python run_market_client.py --key ${OPENAI_API_KEY}; \
    fi