FROM python:3.12

ENV PYTHONPATH="${PYTHONPATH}:/src"

WORKDIR /home

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]