import asyncio
from typing import List, AsyncGenerator
import strawberry
from strawberry import Schema

from .models import College, Student
from ..database import get_db

@strawberry.type
class CollegeType:
    id: int
    name: str
    location: str

@strawberry.type
class StudentType:
    id: int
    name: str
    age: int
    college_id: int 