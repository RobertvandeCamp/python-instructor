SELECT id, data FROM candidates;

SELECT 
    id,
    data->>'full_name' AS full_name,
    data->>'email' AS email,
    data->>'location' AS location,
    data->>'experience_years' AS experience_years
FROM candidates;