# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential cmake git && rm -rf /var/lib/apt/lists/*

ENV CMAKE_ARGS="-DLLAMA_CUBLAS=OFF -DLLAMA_HIPBLAS=OFF -DLLAMA_CLBLAST=OFF"

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# (Optional) Specify a default command to run when the container starts
# For example, if you have a main script: CMD ["python", "your_main_script.py"]
# Or for a library project, you might not need a CMD or ENTRYPOINT,
# or you might set up a command that runs tests or a demo.

CMD ["python", "main.py"]
