from fastapi import FastAPI, status, Depends, Response
from typing import Annotated
from sqlalchemy.orm import Session
import uvicorn

from database import Base, get_db, engine
from responses import StandardResponse
from services import (
    read_teachers,
    find_teachers,
    read_teacher_by_id,
    create_teacher,
    update_teacher,
    delete_teacher,
)
from schemas import TeacherCreate, TeacherUpdate, TeacherResponse

app = FastAPI(title="Đề 3", description="Bài kiểm tra giữa môn", version="final")

Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def check():
    return StandardResponse(
        statusCode=status.HTTP_200_OK, error=None, message="API đang chạy", data=None
    )


@app.get("/teachers")
def read_teachers_endpoint(db: db_dependency):
    teacher_list = read_teachers(db)
    return StandardResponse(
        statusCode=status.HTTP_200_OK,
        error=None,
        message="Lấy danh sách giáo viên thành công",
        data=[TeacherResponse.model_validate(t) for t in teacher_list],
    )


@app.get("/teachers/search")
def find_teachers_endpoint(db: db_dependency, keyword: str):
    teacher_list = find_teachers(db, keyword)
    return StandardResponse(
        statusCode=status.HTTP_200_OK,
        error=None,
        message="Lấy danh sách giáo viên thành công",
        data=[TeacherResponse.model_validate(t) for t in teacher_list],
    )


@app.post("/teachers")
def create_teacher_endpoint(
    db: db_dependency, teacher_in: TeacherCreate, response: Response
):
    teacher = create_teacher(db, teacher_in)
    response.status_code = status.HTTP_201_CREATED
    return StandardResponse(
        statusCode=status.HTTP_201_CREATED,
        error=None,
        message="Thêm giáo viên thành công",
        data=TeacherResponse.model_validate(teacher),
    )


@app.get("/teachers/{teacher_id}")
def read_teacher_by_id_endpoint(db: db_dependency, teacher_id: int, response: Response):
    teacher = read_teacher_by_id(db, teacher_id)
    if not teacher:
        response.status_code = status.HTTP_404_NOT_FOUND
        return StandardResponse(
            statusCode=status.HTTP_404_NOT_FOUND,
            error="Not Found",
            message="Không tìm thấy giảng viên",
            data=None,
        )
    return StandardResponse(
        statusCode=status.HTTP_200_OK,
        error=None,
        message=f"Lấy thành công giáo viên có id {teacher_id}",
        data=TeacherResponse.model_validate(teacher),
    )


@app.put("/teachers/{teacher_id}")
def update_teacher_endpoint(
    db: db_dependency,
    teacher_in: TeacherUpdate,
    teacher_id: int,
    response: Response,
):
    teacher = update_teacher(db, teacher_in, teacher_id)
    if teacher is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return StandardResponse(
            statusCode=status.HTTP_404_NOT_FOUND,
            error="Not Found",
            message="Không tìm thấy giảng viên",
            data=None,
        )

    return StandardResponse(
        statusCode=status.HTTP_200_OK,
        error=None,
        message=f"Cập nhật giáo viên có id {teacher_id} thành công",
        data=TeacherResponse.model_validate(teacher),
    )


@app.delete("/teachers/{teacher_id}")
def delete_teacher_endpoint(db: db_dependency, teacher_id: int, response: Response):
    teacher = delete_teacher(db, teacher_id)
    if not teacher:
        response.status_code = status.HTTP_404_NOT_FOUND
        return StandardResponse(
            statusCode=status.HTTP_404_NOT_FOUND,
            error="Not Found",
            message="Không tìm thấy giảng viên",
            data=None,
        )

    return StandardResponse(
        statusCode=status.HTTP_200_OK,
        error=None,
        message=f"Xóa giáo viên có id {teacher_id} thành công",
        data=None,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
