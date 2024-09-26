# Stage 1: Build Stage (Install dependencies and build)
FROM python:3.10-slim as build

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Collect static files (for later versions of leadsmanager01)
# RUN python manage.py collectstatic --noinput

# Stage 2: Runtime Stage (Smaller image for production use)
FROM python:3.10-slim

# Create non-root user and group
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Set the working directory
WORKDIR /app

# Copy only necessary files from build stage
COPY --from=build /app /app

# Change ownership of the application files to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "leadsmanager.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=3"]