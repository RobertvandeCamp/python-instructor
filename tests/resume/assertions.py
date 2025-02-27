from assertpy import assert_that, add_extension
from src.resume.models import Candidate

def candidate_assertions():
    """Register custom assertions for Candidate objects"""
    @add_extension
    def is_candidate(self):
        """Check if value is a Candidate"""
        if not isinstance(self.val, Candidate):
            self.error(f"Expected a Candidate but got {type(self.val).__name__}")
        return self
    
    def has_email(self, expected):
        """Assert candidate has specific email"""
        self.is_candidate()
        if self.val.email != expected:
            self.error(f"Expected email to be '{expected}' but was '{self.val.email}'")
        return self
    
    @add_extension
    def has_full_name(self, expected):
        """Assert candidate has specific full name"""
        self.is_candidate()
        if self.val.full_name != expected:
            self.error(f"Expected full_name to be '{expected}' but was '{self.val.full_name}'")
        return self
    
    @add_extension
    def has_phone(self, expected):
        """Assert candidate has specific phone"""
        self.is_candidate()
        if self.val.phone != expected:
            self.error(f"Expected phone to be '{expected}' but was '{self.val.phone}'")
        return self
    
    @add_extension
    def has_location(self, expected):
        """Assert candidate has specific location"""
        self.is_candidate()
        if self.val.location != expected:
            self.error(f"Expected location to be '{expected}' but was '{self.val.location}'")
        return self
    
    @add_extension  
    def has_empty_location(self):
        """Assert candidate has empty location"""
        self.is_candidate()
        if self.val.location:
            self.error("Expected location to be empty but it was not")
        return self
    
    @add_extension
    def has_experience_years(self, expected):
        """Assert candidate has specific experience years"""
        self.is_candidate()
        if self.val.experience_years != expected:
            self.error(f"Expected experience_years to be {expected} but was {self.val.experience_years}")
        return self
    
    @add_extension
    def has_education(self, expected):
        """Assert candidate has specific education"""
        self.is_candidate()
        if self.val.education != expected:
            self.error(f"Expected education to be '{expected}' but was '{self.val.education}'")
        return self
    
    @add_extension
    def has_skills(self, *expected_skills):
        """Assert candidate has all the specified skills"""
        self.is_candidate()
        missing_skills = [skill for skill in expected_skills if skill not in self.val.skills]
        unexpected_skills = [skill for skill in self.val.skills if skill not in expected_skills]
        
        if missing_skills or unexpected_skills:
            error_msg = []
            if missing_skills:
                error_msg.append(f"Expected skills {missing_skills} were missing")
            if unexpected_skills:
                error_msg.append(f"Unexpected skills {unexpected_skills} were present")
            self.error(". ".join(error_msg))
        return self
    
    @add_extension
    def has_id(self):
        """Assert candidate has an ID (not None)"""
        self.is_candidate()
        if self.val.id is None:
            self.error("Expected candidate to have an ID but it was None")
        return self
    
    @add_extension
    def has_preferred_job_types(self, *expected_types):
        """Assert candidate has all the specified preferred job types"""
        self.is_candidate()
        missing_types = [job_type for job_type in expected_types if job_type not in self.val.preferred_job_types]
        unexpected_types = [job_type for job_type in self.val.preferred_job_types if job_type not in expected_types]    
        
        if missing_types or unexpected_types:
            error_msg = []
            if missing_types:
                error_msg.append(f"Expected preferred job types to include {missing_types} but they were missing")
            if unexpected_types:
                error_msg.append(f"Unexpected preferred job types {unexpected_types} were present")
            self.error(". ".join(error_msg))
        return self

# Register the extensions
candidate_assertions() 