FROM python:3.7.12-slim-buster

WORKDIR /home

COPY scraperCurso.py /home/scraperCurso.py
COPY scraper_executor.py /home/scraper_executor.py
COPY requirements.txt /home/requirements.txt

RUN pip install -r /home/requirements.txt

CMD ["python", "scraper_executor.py"]