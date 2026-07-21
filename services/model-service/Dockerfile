FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY services/model-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/model-service/app ./app
RUN useradd --create-home --uid 10001 appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 8001
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8001"]
