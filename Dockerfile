FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9


WORKDIR /api

RUN pip install poetry
COPY . /api
COPY ./pyproject.toml ./poetry.lock* /api/

RUN poetry config virtualenvs.create false
RUN poetry env use system
RUN poetry install

WORKDIR /api/api
#CMD uvicorn main:app --host 0.0.0.0 --port $PORT
