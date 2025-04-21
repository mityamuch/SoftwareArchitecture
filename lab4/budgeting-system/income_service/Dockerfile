FROM python:3.11-slim
WORKDIR /workspace
COPY . .
ENV PYTHONPATH=/workspace
EXPOSE 8003
COPY ./security ./security
COPY income_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "income_service/main.py"]