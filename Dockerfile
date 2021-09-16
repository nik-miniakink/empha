FROM python:3.8.5
RUN mkdir /code
COPY requirements.txt /code
RUN pip3 install -r /code/requirements.txt
COPY . /code
RUN python /code/app/manage.py migrate
CMD python /code/app/manage.py runserver 0:8000