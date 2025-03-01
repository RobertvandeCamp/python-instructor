import json
import pytest
from pathlib import Path
from pydantic import ValidationError
from assertpy import assert_that
from src.resume.models import Candidate
from tests.resume.assertions import candidate_assertions  # Import the assertions

# Helper to load test data
def load_test_data(filename):
    data_dir = Path(__file__).parent.parent / 'data' / 'candidates'
    with open(data_dir / filename, 'r') as f:
        return json.load(f)

class TestCandidate:
    def test_create_candidate_with_all_fields(self):
        """Test creating a candidate with all fields populated"""
        data = load_test_data('candidate_complete.json')
        candidate = Candidate(**data)

        assert_that(candidate)\
            .has_full_name("John Doe")\
            .has_email("john.doe@example.com")\
            .has_phone("+1-555-123-4567")\
            .has_location("New York, NY")\
            .has_experience_years(5)\
            .has_education("Master's in Computer Science")\
            .has_skills("Python", "Java", "AWS")\
            .has_preferred_job_types("Full-time", "Remote")\
            .has_id()
        
























    def test_create_candidate_with_required_fields_only(self):
        """Test creating a candidate with only required fields"""
        data = load_test_data('candidate_required_only.json')
        candidate = Candidate(**data)
        
        assert_that(candidate)\
            .has_full_name("Jane Smith")\
            .has_email("jane.smith@example.com")\
            .has_phone("+1-555-987-6543")\
            .has_education("Bachelor's in Software Engineering")\
            .has_id()\
            .has_skills()\
            .has_empty_location()\
            .has_preferred_job_types()\
            .has_experience_years(0)

    def test_invalid_email(self):
        """Test that invalid email raises ValidationError"""
        data = load_test_data('candidate_required_only.json')
        data['email'] = "invalid-email"
        
        with pytest.raises(ValidationError) as exc_info:
            Candidate(**data)
        assert "value is not a valid email address" in str(exc_info.value)

    def test_invalid_experience_years(self):
        """Test that negative experience years raises ValidationError"""
        data = load_test_data('candidate_complete.json')
        data['experience_years'] = -1
        
        with pytest.raises(ValidationError) as exc_info:
            Candidate(**data)
        assert "Input should be greater than or equal to 0" in str(exc_info.value)

    def test_missing_required_field(self):
        """Test that missing required field raises ValidationError"""
        data = load_test_data('candidate_required_only.json')
        del data['full_name']
        
        with pytest.raises(ValidationError) as exc_info:
            Candidate(**data)
        assert "Field required" in str(exc_info.value)

    def test_empty_phone_number(self):
        """Test that empty phone number raises ValidationError"""
        data = load_test_data('candidate_required_only.json')
        data['phone'] = "   "  # Empty or whitespace
        
        with pytest.raises(ValidationError) as exc_info:
            Candidate(**data)
        assert "Phone number is required" in str(exc_info.value) 