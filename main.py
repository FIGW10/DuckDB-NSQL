# Import necessary modules
import duckdb
from examples.utils import generate_sql
from llama_cpp import Llama
from wurlitzer import pipes  # Though not used in the final Llama init, imported as requested
import requests
import os
import time # Added for timing

# Define model URL and path
MODEL_URL = "https://huggingface.co/motherduckdb/DuckDB-NSQL-7B-v0.1-GGUF/resolve/main/DuckDB-NSQL-7B-v0.1-q8_0.gguf"
MODEL_PATH = "/app/DuckDB-NSQL-7B-v0.1-q8_0.gguf"

# Function to download the model
def download_model(url, path):
    if os.path.exists(path):
        print(f"Model already exists at {path}. Skipping download.")
        return
    
    print(f"Downloading model from {url} to {path}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes
        with open(path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("Model downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading model: {e}")
        # Attempt to remove partially downloaded file if it exists
        if os.path.exists(path):
            os.remove(path)
        raise # Re-raise the exception to be caught by the main try-except block
    except IOError as e:
        print(f"Error writing model file: {e}")
        if os.path.exists(path):
            os.remove(path)
        raise

# Main script execution
try:
    # Download the model
    download_model(MODEL_URL, MODEL_PATH)

    # Initialize Llama client
    print("Initializing Llama client...")
    client = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
    )
    print("Llama client initialized.")

    # Connect to DuckDB database
    print("Connecting to DuckDB...")
    con = duckdb.connect("examples/nyc.duckdb")
    print("Connected to DuckDB.")

    # Sample question for SQL generation
    question = "alter taxi table and add struct column with name test and keys a:int, b:double"
    print(f"Generating SQL for question: \"{question}\"")

    # Time the generate_sql call
    start_time = time.perf_counter()
    sql = generate_sql(question, con, client)
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    print("Generated SQL:")
    print(sql)
    print(f"Time taken for generate_sql: {duration:.4f} seconds")


except Exception as e:
    print(f"An unexpected error occurred: {e}")
