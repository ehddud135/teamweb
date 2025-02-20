# TeamWeb 프로젝트

이 프로젝트는 Django 기반의 웹 애플리케이션이며, PostgreSQL을 사용합니다.

## 📌 환경 변수 설정

프로젝트 실행을 위해 다음 환경 변수 파일을 설정해야 합니다.

### 🛠 1. `teamweb/prod.env` 파일 생성

아래 내용을 `teamweb/prod.env` 파일에 추가하세요.

```env
DEBUG=False
POSTGRES_DB=your_db_name
POSTGRES_USER=your_user_name
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
