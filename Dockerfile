# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY pyproject.toml poetry.lock /app/
COPY crazybot /app

# Install any needed packages
RUN pip install poetry
RUN poetry lock
RUN poetry install

COPY run.sh ./
#RUN chmod a+x run.sh

# Start and enable SSH
RUN apt-get update \
    && apt-get install -y --no-install-recommends dialog \
    && apt-get install -y --no-install-recommends openssh-server \
    && echo "root:Docker!" | chpasswd \
    && chmod u+x "./run.sh"
COPY sshd_config /etc/ssh/

EXPOSE 80 2222

# Run app.py when the container launches
ENTRYPOINT ["./run.sh"]
