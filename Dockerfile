# Use the official lightweight Python 3.12 image
FROM python:3.12-slim

# Install system dependencies required for PostgreSQL client and building Python packages
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file to leverage Docker cache for dependencies
COPY requirements.txt .

# Install Python dependencies listed in requirements.txt without cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project source code into the container
COPY . .

# Expose port 8000 to allow external access to the Django development server
EXPOSE 8000

# Run the Django development server, binding to all interfaces inside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
