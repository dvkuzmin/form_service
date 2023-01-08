FROM python:3.9


ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www/

ADD ./form_app/src/ /var/www/

RUN apt-get update && apt-get install -y vim && apt-get upgrade -y
RUN pip install --upgrade pip poetry

COPY ./pyproject.toml /pyproject.toml
COPY ./poetry.lock /poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry add gunicorn
RUN poetry install --no-dev

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "main:form_app", "--reload"]

EXPOSE 5000
