FROM python:3.9-slim

WORKDIR /home
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "/home/python_script.py"]