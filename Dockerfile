# Use Python 3.10-slim as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies for pyodbc
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    unixodbc-dev \
    gcc \
    g++ \
    curl \
    gnupg2

# Install the Microsoft ODBC driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Copy the application files
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
