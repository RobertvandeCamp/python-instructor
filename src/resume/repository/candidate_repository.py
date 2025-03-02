from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from src.resume.models import Candidate
from src.resume.repository.db_models import CandidateRecord
from src.resume.utils.json_utils import model_to_dict, dict_to_model

class CandidateRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, candidate: Candidate) -> Candidate:
        # Convert Pydantic model to dict for JSON storage with proper type handling
        candidate_data = model_to_dict(candidate)
        
        # Check if record exists
        db_record = self.session.query(CandidateRecord).filter(
            CandidateRecord.id == candidate.id
        ).first()
        
        if db_record:
            # Update existing record
            db_record.data = candidate_data
        else:
            # Create new record
            db_record = CandidateRecord(
                id=candidate.id,
                data=candidate_data
            )
            self.session.add(db_record)
            
        self.session.commit()
        return candidate
    
    def find_by_id(self, id: UUID) -> Optional[Candidate]:
        db_record = self.session.query(CandidateRecord).filter(
            CandidateRecord.id == id
        ).first()
        
        if not db_record:
            return None
            
        # Convert JSON data back to Pydantic model
        return dict_to_model(db_record.data, Candidate)
    
    def find_by_name_or_email(self, search_term: str) -> List[Candidate]:
        """Search candidates by name or email using JSONB operators"""
        records = self.session.query(CandidateRecord).filter(
            or_(
                func.lower(CandidateRecord.data['full_name'].astext).like(f"%{search_term.lower()}%"),
                func.lower(CandidateRecord.data['email'].astext).like(f"%{search_term.lower()}%")
            )
        ).all()
        
        return [Candidate.model_validate(record.data) for record in records]
    
    def find_by_skills(self, skills: List[str]) -> List[Candidate]:
        """Find candidates with specific skills using JSON querying"""
        records = self.session.query(CandidateRecord).filter(
            # PostgreSQL JSONB containment operator @>
            CandidateRecord.data['skills'].contains(skills)
        ).all()
        
        return [Candidate.model_validate(record.data) for record in records] 