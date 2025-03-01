FROM postgres:17

# Environment variables for database configuration
ENV POSTGRES_DB=myappdb
ENV POSTGRES_USER=appuser
ENV POSTGRES_PASSWORD=apppassword

# Add initialization scripts if needed
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Data volume
VOLUME ["/var/lib/postgresql/data"] 