from sqlalchemy.orm import Session
from models import TeacherModel

from schemas import TeacherCreate, TeacherUpdate


def read_teachers(db: Session):
    return db.query(TeacherModel).all()


def find_teachers(db: Session, keyword: str):
    pattern = f"%{keyword}%"
    return (
        db.query(TeacherModel).filter(TeacherModel.specialization.ilike(pattern)).all()
    )

 
def read_teacher_by_id(db: Session, id: int):
    return db.query(TeacherModel).filter(TeacherModel.id == id).first()


def create_teacher(db: Session, teacher_in: TeacherCreate):
    teacher_orm = TeacherModel(**teacher_in.model_dump())
    db.add(teacher_orm)
    db.commit()
    db.refresh(teacher_orm)
    return teacher_orm


def update_teacher(db: Session, teacher_in: TeacherUpdate, teacher_id: int):
    teacher = read_teacher_by_id(db, teacher_id)

    if not teacher:
        return None

    update_data = teacher_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)
    return teacher


def delete_teacher(db: Session, teacher_id: int):
    teacher = read_teacher_by_id(db, teacher_id)

    if not teacher:
        return None

    db.delete(teacher)
    db.commit()
    return teacher
