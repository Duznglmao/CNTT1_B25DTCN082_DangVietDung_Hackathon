from pydantic import BaseModel, EmailStr, Field, ConfigDict


class TeacherBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=50)
    specialization: str = Field(min_length=1, max_length=20)
    email: EmailStr
    experience_years: int = Field(ge=0, le=60)


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=50)
    specialization: str | None = Field(default=None, min_length=1, max_length=20)
    email: EmailStr | None = None
    experience_years: int | None = Field(default=None, ge=0, le=60)
    model_config = ConfigDict(from_attributes=True)


class TeacherResponse(TeacherBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
