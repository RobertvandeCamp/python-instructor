from assertpy import add_extension
from src.resume.models import Job

def job_assertions():
    @add_extension
    def is_job(self):
        if not isinstance(self.val, Job):
            self.error(f"Expected a Job but got {type(self.val).__name__}")
        return self
    
    @add_extension
    def has_job_id(self):
        self.is_job()
        if self.val.id is None:
            self.error("Job ID is required")
        return self
    
    @add_extension
    def has_title(self, expected):
        self.is_job()
        if self.val.title != expected:
            self.error(f"Expected title to be '{expected}' but was '{self.val.title}'")
        return self
    
    @add_extension
    def has_company(self, expected):
        self.is_job()
        if self.val.company != expected:
            self.error(f"Expected company to be '{expected}' but was '{self.val.company}'")
        return self;

    @add_extension
    def has_job_location(self, expected):
        self.is_job()
        if self.val.location != expected:
            self.error(f"Expected location to be '{expected}' but was '{self.val.location}'")
        return self;

    @add_extension
    def has_required_skills(self, *expected_skills):
        self.is_job()
        missing_skills = [skill for skill in expected_skills if skill not in self.val.required_skills]
        unexpected_skills = [skill for skill in self.val.required_skills if skill not in expected_skills]

        if missing_skills or unexpected_skills:
            error_msg = []
            if missing_skills:
                error_msg.append(f"Expected skills {missing_skills} were missing")
            if unexpected_skills:
                error_msg.append(f"Unexpected skills {unexpected_skills} were present")
            self.error(". ".join(error_msg))
        return self
    
    @add_extension
    def has_min_experience(self, expected):
        self.is_job()
        if self.val.min_experience != expected:
            self.error(f"Expected minimum experience to be {expected} but was {self.val.min_experience}")
        return self
    
    @add_extension
    def has_job_type(self, expected):
        self.is_job()
        if self.val.job_type != expected:
            self.error(f"Expected job type to be '{expected}' but was '{self.val.job_type}'")
        return self
    
    @add_extension
    def has_salary_range(self, expected):
        self.is_job()
        if self.val.salary_range != expected:
            self.error(f"Expected salary range to be '{expected}' but was '{self.val.salary_range}'")
        return self 
    
    @add_extension
    def has_empty_salary_range(self):
        self.is_job()
        if self.val.salary_range:
            self.error("Salary range should be empty")
        return self
    
# Register the extensions - this needs to be OUTSIDE the function definition
job_assertions()