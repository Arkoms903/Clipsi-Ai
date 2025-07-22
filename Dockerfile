# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for ffmpeg, etc.)
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Copy code to working directory
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
