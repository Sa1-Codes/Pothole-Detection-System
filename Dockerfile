# Step 1: Use an official Python runtime as the base image
FROM python:3.9-slim

# Step 2: Install OpenGL dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory inside the container
WORKDIR /app

# Step 4: Copy the local files into the container's /app directory
COPY . /app

# Step 5: Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Expose the Flask app's port (8000)
EXPOSE 8000

# Step 7: Set the environment variable for Flask app
ENV FLASK_APP=app.py

# Step 8: Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
