-- Enable PostgreSQL extensions
-- This file is designed to be extended with pgvector and other extensions as needed

-- Basic PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";     -- For UUID generation

-- Set timezone to UTC
ALTER DATABASE resumedb SET timezone TO 'UTC';

-- Placeholder for pgvector extension
-- Uncomment this line when you're ready to use pgvector
-- CREATE EXTENSION IF NOT EXISTS "vector";

-- Comment explaining what this database is for
COMMENT ON DATABASE resumedb IS 'Database for storing and managing resume data';

-- Note: Let Alembic handle the actual table schema migrations 