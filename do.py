# Import necessary modules
import duckdb
from utils import generate_sql

# Connect to DuckDB database
con = duckdb.connect("examples/nyc.duckdb")

# Sample question for SQL generation
question = "alter taxi table and add struct column with name test and keys a:int, b:double"

# Generate SQL, check validity, and print
# Assuming 'client' is optional or has a default in generate_sql
sql = generate_sql(question, con)
print(sql)
