FROM python:3.7.10-stretch

WORKDIR /home

COPY main.py /home/main.py
COPY __init__.py /home/__init__.py
COPY src/* /home/src/
COPY src/models/* /home/src/models/
COPY crud_api_requirements.txt /home/crud_api_requirements.txt

RUN pip install -r /home/crud_api_requirements.txt

EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]