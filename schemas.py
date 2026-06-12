from pydantic import BaseModel

# Base schema
class StudentBase(BaseModel):
    name: str
    email: str


# Create schema
class StudentCreate(StudentBase):
    pass


# Profile base schema
class StudentProfileBase(BaseModel):
    address: str
    phone: str


# Profile create schema
class StudentProfileCreate(StudentProfileBase):
    pass


# Profile response schema
class StudentProfileResponse(StudentProfileBase):
    id: int

    class Config:
        from_attributes = True


# Student response schema
class StudentResponse(StudentBase):
    id: int
    profile: StudentProfileResponse | None = None

    class Config:
        from_attributes = True