FROM python:3.12-slim-bullseye

WORKDIR /app

COPY requirements.txt .

RUN useradd -m myuser && pip install --no-cache-dir -r requirements.txt && \
    mkdir logs qr_codes && chown myuser:myuser logs qr_codes

USER myuser

ENTRYPOINT ["python", "main.py"]

CMD ["--url", "https://hub.docker.com/repository/docker/tdeans/qr-generator/general"]