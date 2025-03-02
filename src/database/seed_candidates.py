#!/usr/bin/env python3
"""
Database seeding script for candidate data.
Run with: python -m scripts.seed_candidates
"""

import uuid
import random
from datetime import datetime, timedelta
from typing import List
import os
from dotenv import load_dotenv

# Import your models and database setup
from src.resume.models import Candidate
from src.resume.repository.candidate_repository import CandidateRepository
from src.database.database import engine, SessionLocal
from src.database.db_connection_checker import check_db_connection

# Load environment variables
load_dotenv()

# Sample data for generating realistic candidates
FIRST_NAMES = ["John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Lisa", "William", "Maria"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
LOCATIONS = ["New York, NY", "San Francisco, CA", "Austin, TX", "Seattle, WA", "Chicago, IL", 
             "Boston, MA", "Los Angeles, CA", "Denver, CO", "Atlanta, GA", "Portland, OR"]
SKILLS_POOL = ["Python", "Java", "JavaScript", "React", "Angular", "Vue.js", "AWS", "Azure", 
               "GCP", "Docker", "Kubernetes", "CI/CD", "SQL", "NoSQL", "MongoDB", "PostgreSQL", 
               "Redis", "Machine Learning", "Data Analysis", "TensorFlow", "PyTorch", 
               "NLP", "Computer Vision", "Agile", "Scrum", "REST API", "GraphQL"]
EDUCATION_LEVELS = ["Bachelor's in Computer Science", "Master's in Computer Science", 
                    "PhD in Computer Science", "Bachelor's in Engineering", 
                    "Master's in Data Science", "Bachelor's in Mathematics",
                    "Self-taught", "Bootcamp Graduate", "Associate's Degree in IT"]
JOB_TYPES = ["Full-time", "Part-time", "Contract", "Freelance", "Remote"]

def generate_random_candidate() -> Candidate:
    """Generate a random candidate with realistic data."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    
    # Generate 3-7 random skills
    num_skills = random.randint(3, 7)
    skills = random.sample(SKILLS_POOL, num_skills)
    
    # Generate 1-3 preferred job types
    num_job_types = random.randint(1, 3)
    preferred_job_types = random.sample(JOB_TYPES, num_job_types)
    
    return Candidate(
        id=uuid.uuid4(),
        full_name=f"{first_name} {last_name}",
        email=f"{first_name.lower()}.{last_name.lower()}@example.com",
        phone=f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        location=random.choice(LOCATIONS),
        skills=skills,
        experience_years=random.randint(0, 15),
        education=random.choice(EDUCATION_LEVELS),
        preferred_job_types=preferred_job_types
    )

def seed_candidates(count: int = 10) -> List[Candidate]:
    """Generate and save random candidates to the database."""
    candidates = [generate_random_candidate() for _ in range(count)]
    
    # Create a database session
    session = SessionLocal()
    try:
        # Use the repository to save candidates
        repository = CandidateRepository(session)
        
        saved_candidates = []
        for candidate in candidates:
            saved = repository.save(candidate)
            saved_candidates.append(saved)
            print(f"Added candidate: {saved.full_name} ({saved.email})")
        
        return saved_candidates
    finally:
        session.close()

if __name__ == "__main__":
    # Check database connection first
    if not check_db_connection():
        print("Database connection failed. Aborting seed operation.")
        exit(1)
    
    print("Seeding database with test candidates...")
    candidates = seed_candidates(10)
    print(f"Added {len(candidates)} candidates to the database.")