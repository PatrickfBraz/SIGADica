FROM python:3.7.10-stretch

WORKDIR /home

COPY set_up_database.py /home/set_up_database.py
COPY querys/set_up_querys.sql /home/querys/set_up_querys.sql
COPY set_up_requirements.txt /home/set_up_requirements.txt

RUN pip install --upgrade pip && pip install -r /home/set_up_requirements.txt

CMD ["python", "set_up_database.py"]