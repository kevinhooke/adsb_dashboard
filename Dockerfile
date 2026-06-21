# From https://www.docker.com/blog/how-to-dockerize-django-app/
# Use the official Python runtime image
FROM python:3.13  
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
#COPY requirements.txt  /app/
 
# run this command to install all dependencies 
#RUN pip install --no-cache-dir -r requirements.txt

# Install poetry
RUN apt update

# for postgres psycopg2 dependency support
RUN apt install -y gcc libpq-dev python3-psycopg2

RUN pip install poetry

# Copy the Django project to the container
COPY . /app/

# install deps
RUN poetry install --no-root

# Expose the Django port
EXPOSE 8001
 
# Run Django’s development server
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8001"]