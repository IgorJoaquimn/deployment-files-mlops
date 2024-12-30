# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY generate_rules.py /app
COPY requirements.txt ./

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make the model directory if it doesn't exist (this will be the PVC mount path)
RUN mkdir -p /mnt/data

# Command to run the Python script (you can specify arguments later when the container is run)
CMD ["python", "generate_rules.py", "/mnt/data/2023_spotify_ds1.csv", "/mnt/data/rules.p"]
