# Use Python 3.10 as base image
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Prevent Python from writing pyc files and enable stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (needed for MySQL client)
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client

# Copy the rest of the app
COPY . /app/

# Expose Django's default port
EXPOSE 8000

# Run Django app
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
