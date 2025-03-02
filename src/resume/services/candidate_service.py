from typing import List, Optional
from uuid import UUID
from src.resume.models import Candidate
from src.resume.repository.candidate_repository import CandidateRepository

class CandidateService:
    def __init__(self, repository: CandidateRepository):
        self.repository = repository
    
    def create_candidate(self, candidate: Candidate) -> Candidate:
        return self.repository.save(candidate)
    
    def get_candidate(self, id: UUID) -> Optional[Candidate]:
        return self.repository.find_by_id(id)
    
    def search_candidates(self, search_term: str) -> List[Candidate]:
        return self.repository.find_by_name_or_email(search_term)
    
    def find_candidates_with_skills(self, skills: List[str]) -> List[Candidate]:
        return self.repository.find_by_skills(skills) 