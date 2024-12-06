FROM tiangolo/uvicorn-gunicorn:python3.10

LABEL maintainer="duborgis"

RUN apt-get update && apt-get upgrade -y

RUN pip install --upgrade pip==23.3.0

RUN pip install uv

COPY requirements.txt /tmp/requirements.txt

RUN uv pip install --system --no-cache-dir -r /tmp/requirements.txt

COPY ./src /src

WORKDIR /

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
