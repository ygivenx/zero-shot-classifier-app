FROM python:3.9-slim-buster
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml /app
COPY poetry.lock /app
RUN poetry config virtualenvs.create false --local
RUN poetry install
COPY . /app
EXPOSE 8501

CMD ["streamlit", "run", "app.py"]