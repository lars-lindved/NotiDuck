# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 8000

# Create the instance folder
RUN mkdir -p /app/instance

# Set appropriate permissions
RUN chmod -R 755 /app/instance

# Run the command to start the Gunicorn server
CMD ["sh", "-c", "if [ $APP_ENV = 'production' ]; then gunicorn --workers 3 --bind 0.0.0.0:8000 run:app; else gunicorn --workers 1 --reload --bind 0.0.0.0:8001 run:app; fi"]

