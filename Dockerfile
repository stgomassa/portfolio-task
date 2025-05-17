# Use a slim Python image for smaller size
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file first (better for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire api directory to the container
COPY api /app/api

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expose the FastAPI default port
EXPOSE 8000

# Set the entrypoint to the shell script
ENTRYPOINT ["/app/entrypoint.sh"]
