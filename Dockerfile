# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Django will run on (8000 for gunicorn)
EXPOSE 8000

# Run database migrations and start Gunicorn to serve the app
CMD ["sh", "-c", "python manage.py migrate && gunicorn leadsmanager.wsgi:application --bind 0.0.0.0:8000"]