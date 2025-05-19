FROM python:3.11-slim-bullseye

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

# Command to run the server
CMD ["streamlit", "run", "app.py"] 