FROM python:3.9-slim

# Install system dependencies for compiling Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY ./project-code /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies from requirements.txt
# Pin Flask and Werkzeug to compatible versions in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask application port
EXPOSE 5000

# Use gunicorn for running the app in production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

