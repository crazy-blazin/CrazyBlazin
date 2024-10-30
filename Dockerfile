# Use an official Python runtime as a parent image
FROM python:3.10-slim
EXPOSE 80

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY pyproject.toml poetry.lock /app/
COPY crazybot /app

# Install any needed packages
RUN pip install poetry
RUN poetry install

# Run app.py when the container launches
ENTRYPOINT [ "poetry", "run", "python", "main.py" ]
