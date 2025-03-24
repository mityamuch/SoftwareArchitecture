FROM python:3.11-slim
WORKDIR /workspace
COPY . .
ENV PYTHONPATH=/workspace/budgeting-system/income_service
EXPOSE 8003
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]