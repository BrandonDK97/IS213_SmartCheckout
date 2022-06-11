FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./add_to_cart.py .
COPY ./invokes.py .
CMD [ "python", "./add_to_cart.py" ]
