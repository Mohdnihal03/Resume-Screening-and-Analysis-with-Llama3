FROM python:3.8-slim

WORKDIR /app


COPY . .

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt

EXPOSE 5000

CMD ["streamlit", "run", "app.py"]