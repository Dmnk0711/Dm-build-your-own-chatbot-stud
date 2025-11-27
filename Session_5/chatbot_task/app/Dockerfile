# Use Python 3.11 slim as base
FROM python:3.11.10

# Set working directory 
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    sqlite3 libsqlite3-dev \
    curl \
    && apt-get clean

# Copy the requirements file first to leverage Docker cache
COPY requirements.lock /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.lock

# Copy application source code
COPY . /app

# Expose the application port
EXPOSE 5001 5678

# Run python debug server and streamlit with live reload enabled
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "-m", "streamlit", "run", "main.py", "--server.port=5001", "--server.address=0.0.0.0"]
