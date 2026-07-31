FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     PIP_DISABLE_PIP_VERSION_CHECK=1     HOME=/tmp

WORKDIR /app

COPY services/model-service/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt     && groupadd --gid 10001 appuser     && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser

COPY --chown=10001:10001 services/model-service/app ./app

USER 10001:10001

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
