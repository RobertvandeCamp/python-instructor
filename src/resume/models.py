from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field, field_validator

class Candidate(BaseModel):
    """Represents a job seeker's profile."""
    id: UUID = Field(default_factory=uuid4)  # Auto-generates UUID (like @GeneratedValue in JPA)
    full_name: str = Field(..., min_length=1)  # ... means required (like @NotNull in Java)
    email: EmailStr  # Required by default
    phone: str
    location: Optional[str] = None
    skills: List[str] = Field(default_factory=list)  # Empty list by default
    experience_years: int = Field(ge=0, default=0)
    education: str
    preferred_job_types: List[str] = Field(default_factory=list)

    @field_validator('phone')
    def validate_phone(cls, v):
        """Validate phone number (basic example)"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Phone number is required')
        return v.strip()

class Job(BaseModel):
    """Represents a job posting."""
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1)
    company: str = Field(..., min_length=1)
    location: str = Field(..., min_length=1)
    required_skills: List[str] = Field(default_factory=list)
    min_experience: int = Field(ge=0)
    job_type: str = Field(..., min_length=1)
    salary_range: Optional[str] = None  # Optional field (similar to Optional<String> in Java)

class Experience(BaseModel):
    """Represents a single work experience entry."""
    company: str
    role: str
    years: float

class Education(BaseModel):
    """Represents a single education entry."""
    degree: str
    university: str
    year: int

class Resume(BaseModel):
    """Stores structured resume data."""
    id: UUID
    candidate_id: UUID
    raw_text: str
    structured_experience: List[Experience]  # Nested Pydantic models (similar to @Embedded in JPA)
    structured_education: List[Education]
    extracted_skills: List[str]
    last_updated: datetime 