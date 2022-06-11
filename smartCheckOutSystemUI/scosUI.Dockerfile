FROM python:3-slim
WORKDIR /usr/src/app
COPY css .
COPY Images .
COPY js .
COPY sslKeys .
COPY index.html .
COPY location.html .
COPY login.html .
COPY qrcode.html .
COPY signup.html .
COPY ./server.py .
CMD [ "python", "./server.py" ]
