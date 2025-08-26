from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Dict

END_KEYWORDS = {"quit","exit","stop","end","goodbye"}

class Candidate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(..., min_length=6, max_length=25)
    experience_years: float
    positions: List[str]
    location: str
    tech_stack: List[str]
    answers: Dict[str, List[str]] = {}

    @validator("positions", "tech_stack", pre=True)
    def split_list(cls, v):
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v
