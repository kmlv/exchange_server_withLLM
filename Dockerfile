FROM node:22-alpine

WORKDIR /app

COPY user-interface/package.json .

RUN npm install

COPY user-interface/. .

RUN npm run build

EXPOSE 8080

CMD [ "npm", "run", "preview" ]



# FROM python:3.10

# WORKDIR /app

# COPY . /app

# RUN pip install -r requirements.txt

# CMD if [ -z "${SERVER_NAME}"]; then\
#         python run_exchange_server.py; \
#     else \
#         python cda_client.py ${SERVER_NAME}; \
#     fi