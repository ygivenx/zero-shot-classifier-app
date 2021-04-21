FROM python:3.9-slim-buster
WORKDIR /app
RUN pip install poetry
COPY poetry.lock /app
RUN poetry config virtualenvs.create false --local
COPY . /app
RUN poetry install
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]