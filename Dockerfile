FROM python:3.12-slim as builder

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && pipenv install --system --deploy

COPY . .

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]