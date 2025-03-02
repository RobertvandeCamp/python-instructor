-- candidate_queries.sql
-- Example PostgreSQL queries for candidate data stored in JSONB format

-- Basic query to retrieve all candidates
SELECT id, data FROM candidates;

-- Extract specific fields from all candidates
SELECT 
    id,
    data->>'full_name' AS full_name,
    data->>'email' AS email,
    data->>'location' AS location,
    data->>'experience_years' AS experience_years
FROM candidates;

-- Filtering by text fields (case-insensitive)
-- Find candidates by name (partial match)
SELECT id, data->>'full_name' AS full_name, data->>'email' AS email
FROM candidates
WHERE data->>'full_name' ILIKE '%john%';

-- Find candidates by email domain
SELECT id, data->>'full_name' AS full_name, data->>'email' AS email
FROM candidates
WHERE data->>'email' ILIKE '%@gmail.com';

-- Find candidates by location
SELECT id, data->>'full_name' AS full_name, data->>'location' AS location
FROM candidates
WHERE data->>'location' ILIKE '%San Francisco%';

-- Filtering by numeric values
-- Find candidates with more than 5 years of experience
SELECT id, data->>'full_name' AS full_name, data->>'experience_years' AS experience
FROM candidates
WHERE (data->>'experience_years')::int > 5;

-- Find candidates with 3-7 years of experience
SELECT id, data->>'full_name' AS full_name, data->>'experience_years' AS experience
FROM candidates
WHERE (data->>'experience_years')::int BETWEEN 3 AND 7;

-- Filtering by array elements (skills)
-- Find candidates with specific skill
SELECT id, data->>'full_name' AS full_name, data->'skills' AS skills
FROM candidates
WHERE data->'skills' ? 'Python';

-- Find candidates with multiple skills (AND condition)
SELECT id, data->>'full_name' AS full_name, data->'skills' AS skills
FROM candidates
WHERE data->'skills' ? 'Python' AND data->'skills' ? 'AWS';

-- Find candidates with any of the skills (OR condition)
SELECT id, data->>'full_name' AS full_name, data->'skills' AS skills
FROM candidates
WHERE data->'skills' ? 'React' OR data->'skills' ? 'Angular';

-- Using the @> containment operator to check for multiple skills
SELECT id, data->>'full_name' AS full_name, data->'skills' AS skills
FROM candidates
WHERE data->'skills' @> '["Python", "AWS"]';

-- Count of candidates by job type preference
SELECT data->>'preferred_job_types' AS job_type, COUNT(*) 
FROM candidates, jsonb_array_elements(data->'preferred_job_types') AS job_type
GROUP BY job_type
ORDER BY COUNT(*) DESC;

-- Combining multiple conditions
-- Find senior Python developers in San Francisco
SELECT 
    id, 
    data->>'full_name' AS full_name, 
    data->>'email' AS email,
    data->>'location' AS location,
    data->>'experience_years' AS experience
FROM candidates
WHERE 
    data->'skills' ? 'Python' AND
    (data->>'experience_years')::int >= 5 AND
    data->>'location' ILIKE '%San Francisco%';

-- Order candidates by experience (descending)
SELECT id, data->>'full_name' AS full_name, data->>'experience_years' AS experience
FROM candidates
ORDER BY (data->>'experience_years')::int DESC;

-- Pagination example (10 candidates per page, page 1)
SELECT id, data 
FROM candidates
ORDER BY data->>'full_name'
LIMIT 10 OFFSET 0;

-- Pagination example (10 candidates per page, page 2)
SELECT id, data 
FROM candidates
ORDER BY data->>'full_name'
LIMIT 10 OFFSET 10;

-- Count of candidates by education level
SELECT data->>'education' AS education, COUNT(*) AS count
FROM candidates
GROUP BY data->>'education'
ORDER BY count DESC;

-- Skill distribution analysis
SELECT skill, COUNT(*) AS count
FROM candidates, jsonb_array_elements_text(data->'skills') AS skill
GROUP BY skill
ORDER BY count DESC;

-- Advanced: Weighted skill search
-- Returns candidates with weighted scores for matching skills
WITH skill_scores AS (
    SELECT 
        id, 
        data->>'full_name' AS full_name,
        CASE WHEN data->'skills' ? 'Python' THEN 3 ELSE 0 END +
        CASE WHEN data->'skills' ? 'AWS' THEN 2 ELSE 0 END +
        CASE WHEN data->'skills' ? 'Docker' THEN 1 ELSE 0 END AS score
    FROM candidates
)
SELECT id, full_name, score
FROM skill_scores
WHERE score > 0
ORDER BY score DESC;

-- Full-text search in multiple fields
SELECT id, data->>'full_name' AS full_name
FROM candidates
WHERE 
    data->>'full_name' ILIKE '%search_term%' OR 
    data->>'email' ILIKE '%search_term%' OR
    data->>'location' ILIKE '%search_term%';

-- Advanced: Find candidates with skills similar to a given candidate
WITH candidate_skills AS (
    SELECT data->'skills' AS skills
    FROM candidates
    WHERE id = '00000000-0000-0000-0000-000000000001'  -- replace with actual UUID
)
SELECT 
    c.id, 
    c.data->>'full_name' AS full_name,
    c.data->'skills' AS skills,
    -- Calculate similarity (intersection of skills / union of skills)
    (SELECT COUNT(*) FROM jsonb_array_elements_text(c.data->'skills') s1
     WHERE EXISTS (
         SELECT 1 FROM jsonb_array_elements_text(cs.skills) s2
         WHERE s1 = s2
     )) AS matching_skills
FROM candidates c, candidate_skills cs
WHERE c.id != '00000000-0000-0000-0000-000000000001'  -- exclude the reference candidate
ORDER BY matching_skills DESC
LIMIT 10;

-- Recommendations for creating indexes:
/*
-- Index for text search on full_name
CREATE INDEX idx_candidate_full_name ON candidates USING gin ((data->>'full_name') gin_trgm_ops);

-- Index for text search on email
CREATE INDEX idx_candidate_email ON candidates USING gin ((data->>'email') gin_trgm_ops);

-- Index for searching skills
CREATE INDEX idx_candidate_skills ON candidates USING gin ((data->'skills'));

-- Index for filtering by location
CREATE INDEX idx_candidate_location ON candidates USING gin ((data->>'location') gin_trgm_ops);

-- Index for sorting by experience
CREATE INDEX idx_candidate_experience ON candidates ((data->>'experience_years')::int);
*/ 