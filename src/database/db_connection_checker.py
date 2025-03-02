#!/usr/bin/env python3
import psycopg2
import sys
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_db_connection(host=None, 
                        port=None, 
                        dbname=None, 
                        user=None, 
                        password=None,
                        max_retries=5,
                        retry_delay=2):
    """
    Check connection to PostgreSQL database.
    
    Uses environment variables from .env by default.
    """
    # Use parameters if provided, otherwise use environment variables
    host = host or os.getenv("DB_HOST", "localhost")
    port = port or os.getenv("DB_PORT", "5432")
    dbname = dbname or os.getenv("DB_NAME", "resumedb")
    user = user or os.getenv("DB_USER", "postgres")
    password = password or os.getenv("DB_PASSWORD", "postgres")
    
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # In Java, you would use DriverManager.getConnection(url, user, password)
            # Python uses a simpler direct connection approach
            print(f"Attempting to connect to database (attempt {retry_count + 1})...")
            
            # Python's with statement is similar to Java's try-with-resources
            with psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            ) as conn:
                
                # In Java: conn.createStatement().executeQuery("SELECT version()")
                with conn.cursor() as cur:
                    cur.execute("SELECT version();")
                    version = cur.fetchone()
                    print(f"Connected to PostgreSQL: {version[0]}")
                
                # Connection successful, no need to retry
                print("Database connection successful!")
                return True
                
        except psycopg2.OperationalError as e:
            retry_count += 1
            print(f"Connection failed: {e}")
            if retry_count < max_retries:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False
    
    print("Max retries reached. Could not connect to the database.")
    return False

if __name__ == "__main__":
    # When run directly, check the database connection
    success = check_db_connection()
    if not success:
        sys.exit(1)