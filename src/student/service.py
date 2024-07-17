import asyncio
from typing import List, AsyncGenerator
import strawberry
from strawberry import Schema

from .models import College, Student
from .schemas import CollegeType, StudentType
from ..database import get_db


@strawberry.type
class Query:
    @strawberry.field
    async def colleges(self) -> List[CollegeType]:
            db=get_db()
            colleges = db.query(College).all()
            return [CollegeType(id=college.id, name=college.name, location=college.location) for college in colleges]

    @strawberry.field
    async def students(self) -> List[StudentType]:
            db=get_db()
            students = db.query(Student).all()
            return [StudentType(id=student.id, name=student.name, age=student.age, college_id=student.college_id) for student in students]
        
        
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_college(self, name: str, location: str) -> CollegeType:
            db=get_db() 
            college = College(name=name, location=location)
            db.add(college)
            db.commit()
            db.refresh(college)
            return CollegeType(id=college.id, name=college.name, location=college.location)

    @strawberry.mutation
    async def create_student(self, name: str, age: int, college_id: int) -> StudentType:
            db=get_db()
            college = db.query(College).filter(College.id == college_id).first()
            if not college:
                raise ValueError("College not found")
            student = Student(name=name, age=age, college_id=college_id)
            db.add(student)
            db.commit()
            db.refresh(student)
            return StudentType(id=student.id, name=student.name, age=student.age, college_id=student.college_id)

@strawberry.type
class Subscription:
    @strawberry.subscription
    async def student_added(self, college_id: int) -> AsyncGenerator[StudentType, None]:
        async for student in student_stream(college_id):
            yield student

async def student_stream(college_id: int) -> AsyncGenerator[StudentType, None]:
    while True:
        await asyncio.sleep(5)  # Simulate real-time updates
        db=get_db() 
        student = db.query(Student).filter(Student.college_id == college_id).order_by(Student.id.desc()).first()
        if student:
            yield StudentType(id=student.id, name=student.name, age=student.age, college_id=student.college_id)
            
schema = Schema(query=Query, mutation=Mutation, subscription=Subscription)