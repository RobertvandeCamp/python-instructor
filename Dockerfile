FROM postgres:17

# Environment variables for database configuration
ENV POSTGRES_DB=resumedb
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Add initialization scripts if needed
COPY ./init-scripts/ /docker-entrypoint-initdb.d/

# Expose PostgreSQL port
EXPOSE 5432

# Data volume
VOLUME ["/var/lib/postgresql/data"] 