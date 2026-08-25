# FastAPI 회원 관리 실습

인메모리 `user_list`를 사용하는 회원 조회·생성·수정·삭제 API입니다.

## 설치 및 실행

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

서버 실행 후 다음 주소에서 확인할 수 있습니다.

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

## API 목록

| Method | Endpoint | 설명 |
| --- | --- | --- |
| `GET` | `/practice_api/users` | 모든 회원 조회 |
| `GET` | `/practice_api/users/{user_id}` | 특정 회원 조회 |
| `POST` | `/practice_api/users` | 회원 생성 |
| `PATCH` | `/practice_api/users/{user_id}` | 입력된 회원 정보만 수정 |
| `DELETE` | `/practice_api/users/{user_id}` | 특정 회원 삭제 |

## 테스트

```bash
pytest -q
```

> 이 프로젝트는 학습용이므로 데이터를 메모리에 저장합니다. 서버를 다시 시작하면 데이터가 초기화됩니다. 실제 서비스에서는 비밀번호를 평문으로 보관하지 말고 반드시 안전한 방식으로 해시한 뒤 데이터베이스에 저장해야 합니다.
