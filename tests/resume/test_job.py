import json
from pathlib import Path
from assertpy import assert_that
from pydantic import ValidationError
import pytest
from src.resume.models import Job
from tests.resume.job_assertions import job_assertions

def load_test_data(filename):
    data_dir = Path(__file__).parent.parent / 'data' / 'candidates'
    with open(data_dir / filename, 'r') as f:
        return json.load(f)

class TestJob:
    def test_create_job_with_all_fields(self):
        data = load_test_data('job_complete.json')
        job = Job(**data)

        print(job.model_dump_json(indent=2))

        assert_that(job)\
            .has_job_id()\
            .has_title("Software Engineer")\
            .has_company("Tech Corp")\
            .has_job_location("San Francisco, CA")\
            .has_required_skills("Python", "Java", "AWS")\
            .has_min_experience(3)\
            .has_job_type("Full-time")\
            .has_salary_range("$100,000 - $120,000")
        
    def test_create_job_with_required_fields_only(self):
        data = load_test_data('job_required_only.json')
        job = Job(**data)
        
        assert_that(job)\
            .has_job_id()\
            .has_title("Software Engineer")\
            .has_company("Tech Corp")\
            .has_job_location("San Francisco, CA")\
            .has_required_skills("Python", "Java", "AWS")\
            .has_min_experience(3)\
            .has_job_type("Full-time")
        
    def test_missing_title(self):
        data = load_test_data('job_required_only.json')
        del data['title']
        
        with pytest.raises(ValidationError) as exc_info:
            Job(**data)
        assert "Field required" in str(exc_info.value) and "title" in str(exc_info.value)

    def test_missing_company(self):
        data = load_test_data('job_required_only.json')
        del data['company']
        
        with pytest.raises(ValidationError) as exc_info:
            Job(**data)
        assert "Field required" in str(exc_info.value) and "company" in str(exc_info.value)

    def test_missing_location(self):
        data = load_test_data('job_required_only.json')
        del data['location']
        
        with pytest.raises(ValidationError) as exc_info:
            Job(**data)
        assert "Field required" in str(exc_info.value) and "location" in str(exc_info.value)

    def test_invalid_min_experience(self):
        data = load_test_data('job_required_only.json')
        data['min_experience'] = -1
        
        with pytest.raises(ValidationError) as exc_info:
            Job(**data)
        assert "greater than or equal to 0" in str(exc_info.value) and "min_experience" in str(exc_info.value)

    def test_missing_job_type(self):
        data = load_test_data('job_required_only.json')
        del data['job_type']
        
        with pytest.raises(ValidationError) as exc_info:
            Job(**data)
        assert "Field required" in str(exc_info.value) and "job_type" in str(exc_info.value)
        
        
        
        