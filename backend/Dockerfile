FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/src
RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

RUN groupadd -r threatsys && useradd -r -g threatsys threatsys \
    && chown -R threatsys:threatsys /app
USER threatsys

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]