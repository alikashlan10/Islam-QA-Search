FROM python:3.11-slim

WORKDIR /app

# install dependencies first (layer caching — only rebuilds if requirements change)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# create logs directory (won't be used in production but keeps local runs clean)
RUN mkdir -p logs

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]