FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

COPY model/ /model/
RUN cd / && python /model/train.py

EXPOSE 5000

CMD ["python", "app.py"]
