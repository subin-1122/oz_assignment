from fastapi import FastAPI

from app.apis.practice_apis import router as practice_router


app = FastAPI(
    title="회원 관리 실습 API",
    description="GitHub Flow와 FastAPI를 연습하기 위한 인메모리 회원 관리 API입니다.",
    version="1.0.0",
)

app.include_router(practice_router)


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    return {"message": "FastAPI server is running."}
