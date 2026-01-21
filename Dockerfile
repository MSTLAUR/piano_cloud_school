# Use Python 3.11-slim as the base image
FROM python:3.11-slim

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p static staticfiles media

# Copy requirements.txt into the image
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    DEBUG=True \
    SECRET_KEY="y!of7trj3l23btde6zfa74wdrbjb+1g0%1br@#u-q8lku6*3=i"

# Create the runner script with better error logging
RUN printf "#!/bin/bash\n\
set -e\n\
RUN_PORT=\"\${PORT:-8000}\"\n\
echo \"Running database migrations...\"\n\
python manage.py migrate --no-input\n\
echo \"Collecting static files...\"\n\
python manage.py collectstatic --no-input\n\
echo \"Starting Gunicorn...\"\n\
gunicorn cloudschool.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\" --log-level debug --error-logfile - --access-logfile - --capture-output\n" > ./paracord_runner.sh && \
    chmod +x paracord_runner.sh

# Remove unnecessary system packages to reduce image size
RUN apt-get remove --purge -y build-essential && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

# Start the application
CMD ["./paracord_runner.sh"]
