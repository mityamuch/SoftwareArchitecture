FROM python:3.12-slim
WORKDIR /workspace
COPY . .
ENV PYTHONPATH=/workspace
EXPOSE 8002
COPY ./security ./security
EXPOSE 5432
COPY user_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "user_service/main.py"]