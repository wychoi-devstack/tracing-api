FROM python:3.10-bullseye

COPY ./ /
COPY ./etc/tracing-api/tracing-api.conf /etc/tracing-api/tracing-api.conf

WORKDIR /
RUN pip install -r requirements.txt

WORKDIR /tracing-api
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
