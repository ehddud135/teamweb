# 1. Set Base Image
FROM python:3.11

# 2. Set Working Directory
WORKDIR /app

# 3. Install Required System Packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy Dependency File and Install Packages
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Project Files
COPY . /app/

# 6. Run Django Server
CMD ["gunicorn", "--chdir", "/app/seteamweb", "--bind", "0.0.0.0:8000", "core.wsgi:application"]