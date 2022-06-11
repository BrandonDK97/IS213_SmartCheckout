FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./activity_log.py .
COPY ./error.py .
COPY ./amqp_setup.py .
COPY ./my_wrapper_script.sh .
CMD ./my_wrapper_script.sh