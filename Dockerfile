FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install curl for testing
RUN apt-get update && apt-get install -y curl

COPY . .

# Set the Python path to include the project root
ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]