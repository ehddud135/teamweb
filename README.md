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
```

### 🛠 2. `teamweb/seteamweb/.env` 파일 생성

아래 내용을 teamweb/seteamweb/.env 파일에 추가하세요.

```env
django_secret_key='your_django_secret_key'
```

## 🚀 프로젝트 실행 방법

### 1. 프로젝트 클론

다음 명령어를 사용하여 프로젝트를 클론하고 이동합니다.

```bash
git clone https://github.com/your-repository/teamweb.git
cd teamweb
```

### 2. 환경 변수 파일 설정

위에서 설명한 prod.env와 .env 파일을 생성합니다.


### 3. Docker를 사용하여 실행

Docker를 사용하는 경우 다음 명령어를 실행하세요.

```bash
# release
docker compose up --build -d

# debug
docker compose -f docker-compose-debug.yml up --build -d
```

## ⚠️ 추가 설정

### .gitignore 파일 업데이트

환경 변수 파일이 Git에 업로드되지 않도록 .gitignore에 다음 항목을 추가하세요.

```gitignore
# 환경 변수 파일
teamweb/prod.env
teamweb/seteamweb/.env
```
