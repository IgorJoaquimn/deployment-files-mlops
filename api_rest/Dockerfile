# Use a lightweight Python image
FROM python:3.11-slim-bullseye

# Set environment variables for Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=52031

# Create and set a working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py ./

# Expose the Flask port
EXPOSE 52031

# Set the default command to run Flask on the correct port
CMD ["flask", "run"]
