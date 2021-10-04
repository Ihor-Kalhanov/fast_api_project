FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOST=0.0.0.0
ENV PORT=8000



WORKDIR /code
COPY . /code/

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt



COPY . .

#CMD uvicorn app.main:app --host ${HOST} --port ${PORT}