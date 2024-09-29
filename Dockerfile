# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for mysqlclient and Python build tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       default-libmysqlclient-dev \
       pkg-config \
       build-essential \
       libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY . .

# Expose the required port
EXPOSE 8080

# Command to run the application
CMD ["gunicorn", "leadsmanager.wsgi:application", "--bind", "0.0.0.0:8080", "--workers=3"]