# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "import pydantic; import langchain; import structlog; import packaging; print('Successfully imported pydantic, langchain, structlog, and packaging')"

# Copy the rest of the application's code into the container at /app
COPY . .

# (Optional) Specify a default command to run when the container starts
# For example, if you have a main script: CMD ["python", "your_main_script.py"]
# Or for a library project, you might not need a CMD or ENTRYPOINT,
# or you might set up a command that runs tests or a demo.
# For now, let's leave it commented out or omit it if not immediately clear.
