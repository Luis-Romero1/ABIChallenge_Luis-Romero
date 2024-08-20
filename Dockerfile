FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Specify the script that SageMaker should use as the entry point
ENV SAGEMAKER_PROGRAM main.py

# CMD specifies the command to run within the container
ENTRYPOINT ["python3", "-m", "sagemaker_training.entry_point"]

# This command will be run by default when the container is started
CMD []
