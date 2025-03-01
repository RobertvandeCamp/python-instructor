#!/usr/bin/env python3
import psycopg2
import sys
import time

def check_db_connection(host='localhost', 
                        port=5432, 
                        dbname='myappdb', 
                        user='appuser', 
                        password='apppassword',
                        max_retries=5,
                        retry_delay=2):
    """
    Check connection to PostgreSQL database.
    
    Similar to Java's try-with-resources pattern but using Python's context manager.
    """
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
    # Parse command line arguments - similar to Java args[]
    # Default values from above function will be used if not provided
    
    # Successful connection = exit code 0, failed = exit code 1
    # Similar to System.exit(0) or System.exit(1) in Java
    if check_db_connection():
        sys.exit(0)
    else:
        sys.exit(1)