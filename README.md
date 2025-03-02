# Resume Analysis Project

## Environment Setup

1. Copy the example environment file:
   ```
   cp .env.example .env
   ```

2. Edit the `.env` file to set your database credentials:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=resumedb
   DB_USER=postgres
   DB_PASSWORD=postgres
   ```

3. Install requirements:
   ```
   pip install -r requirements.txt
   ```

## Database Management

### Docker (PostgreSQL)

The project uses Docker to provide a PostgreSQL database. Key commands:

```bash
# Build and start the database container
docker-compose up -d

# Stop the container
docker-compose down

# Stop the container and remove the volume (resets all data)
docker-compose down -v

# View container logs
docker-compose logs

# View logs and follow new entries
docker-compose logs -f

# Restart the container
docker-compose restart
```

### Database Initialization Scripts

The `init-scripts/` directory contains SQL scripts that run when the PostgreSQL container is first created:

- `01-init-extensions.sql`: Enables PostgreSQL extensions like uuid-ossp and contains placeholder for pgvector

These scripts run in alphabetical order and execute only on the first container startup. If you modify these scripts, you'll need to remove the volume to apply changes:

```bash
docker-compose down -v
docker-compose up -d
```

### Database Migrations (Alembic)

The project uses Alembic for database schema management:

1. Check database connection:
   ```
   python -m src.database.db_connection_checker
   ```

2. Apply migrations:
   ```
   alembic upgrade head
   ```

3. Create a new migration:
   ```
   alembic revision --autogenerate -m "description of changes"
   ```

4. Roll back one migration:
   ```
   alembic downgrade -1
   ```

5. View migration history:
   ```
   alembic history
   ```

Migrations are stored in `migrations/versions/` and are version-controlled. Always review auto-generated migrations before applying them.

### Database Seeding

Seed the database with test data:
```
python -m scripts.seed_candidates
```

## Project Structure

- `src/` - Application source code
  - `database/` - Database connection and utilities
  - `resume/` - Core application modules
    - `models.py` - Domain models (Pydantic)
    - `repository/` - Data access layer
      - `db_models.py` - Database models (SQLAlchemy)
  - `services/` - Business logic
- `migrations/` - Alembic migration scripts
- `init-scripts/` - PostgreSQL initialization scripts
- `scripts/` - Utility scripts for maintenance tasks

## Development Workflow

1. Start the database: `docker-compose up -d`
2. Apply migrations: `alembic upgrade head`
3. Seed test data if needed: `python -m scripts.seed_candidates`
4. Run your application 