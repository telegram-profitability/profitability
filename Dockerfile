FROM python:3.12

ENV PYTHONPATH="${PYTHONPATH}:/src"
ENV PYTHONUNBUFFERED=1

WORKDIR /home

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]