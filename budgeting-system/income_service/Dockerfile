FROM python:3.11-slim
WORKDIR /workspace
COPY . .
EXPOSE 8003
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "income-service.py"]