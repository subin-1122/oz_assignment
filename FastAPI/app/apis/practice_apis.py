import re

from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


router = APIRouter(prefix="/practice_api", tags=["practice_api"])

user_list = [
    {
        "id": 1,
        "name": "홍길동",
        "age": 24,
        "email": "gildong24@example.com",
        "password": "Password1234!!",
    },
    {
        "id": 2,
        "name": "장문복",
        "age": 21,
        "email": "moonluck12@example.com",
        "password": "Check1321!",
    },
    {
        "id": 3,
        "name": "임우진",
        "age": 31,
        "email": "limousine33@example.com",
        "password": "lwsPAssword12@",
    },
]
_next_user_id = max(user["id"] for user in user_list) + 1


EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+$")
UPPERCASE_PATTERN = re.compile(r"[A-Z]")
LOWERCASE_PATTERN = re.compile(r"[a-z]")
SPECIAL_CHARACTER_PATTERN = re.compile(r"[^A-Za-z0-9]")


def validate_email(email: str) -> str:
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("올바른 이메일 형식이 아닙니다.")
    return email


def validate_password(password: str) -> str:
    if not UPPERCASE_PATTERN.search(password):
        raise ValueError("비밀번호에는 대문자가 1개 이상 포함되어야 합니다.")
    if not LOWERCASE_PATTERN.search(password):
        raise ValueError("비밀번호에는 소문자가 1개 이상 포함되어야 합니다.")
    if not SPECIAL_CHARACTER_PATTERN.search(password):
        raise ValueError("비밀번호에는 특수문자가 1개 이상 포함되어야 합니다.")
    return password


class UserResponse(BaseModel):
    id: int
    name: str
    age: int
    email: str


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=10)
    age: int = Field(ge=14)
    email: str = Field(max_length=30)
    password: str = Field(min_length=8, max_length=20)

    @field_validator("email")
    @classmethod
    def check_email(cls, email: str) -> str:
        return validate_email(email)

    @field_validator("password")
    @classmethod
    def check_password(cls, password: str) -> str:
        return validate_password(password)


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    age: int | None = Field(default=None, ge=14)
    email: str | None = Field(default=None, max_length=30)
    password: str | None = Field(default=None, min_length=8, max_length=20)

    @field_validator("age", "email", "password", mode="before")
    @classmethod
    def reject_explicit_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("입력한 항목은 null일 수 없습니다.")
        return value

    @field_validator("email")
    @classmethod
    def check_email(cls, email: str | None) -> str | None:
        if email is None:
            return email
        return validate_email(email)

    @field_validator("password")
    @classmethod
    def check_password(cls, password: str | None) -> str | None:
        if password is None:
            return password
        return validate_password(password)

    @model_validator(mode="after")
    def check_at_least_one_field(self) -> "UserUpdate":
        if not self.model_fields_set:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="수정할 항목을 하나 이상 입력해야 합니다.",
            )
        return self


def find_user(user_id: int) -> dict:
    for user in user_list:
        if user["id"] == user_id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="회원을 찾을 수 없습니다.",
    )


def ensure_unique_email(email: str, *, exclude_user_id: int | None = None) -> None:
    for user in user_list:
        if user["email"].lower() == email.lower() and user["id"] != exclude_user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 사용 중인 이메일입니다.",
            )


def generate_user_id() -> int:
    global _next_user_id

    user_id = _next_user_id
    _next_user_id += 1
    return user_id


@router.get("/users", response_model=list[UserResponse])
def get_users() -> list[dict]:
    """모든 회원의 공개 정보를 목록으로 조회합니다."""
    return user_list


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int) -> dict:
    """ID가 일치하는 회원의 공개 정보를 조회합니다."""
    return find_user(user_id)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(user_data: UserCreate) -> dict:
    """입력값을 검증하고 새 회원을 추가합니다."""
    ensure_unique_email(user_data.email)

    new_user = {"id": generate_user_id(), **user_data.model_dump()}
    user_list.append(new_user)
    return new_user


@router.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate) -> dict:
    """입력된 항목만 회원 정보에 반영합니다."""
    user = find_user(user_id)
    update_fields = user_data.model_dump(exclude_unset=True)

    if "email" in update_fields:
        ensure_unique_email(update_fields["email"], exclude_user_id=user_id)

    user.update(update_fields)
    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> Response:
    """ID가 일치하는 회원을 삭제합니다."""
    user = find_user(user_id)
    user_list.remove(user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
