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

# 5.1 Set Environment Variables
ENV PYTHONUNBUFFERED=1

# 6. Copy Entrypoint Script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 7. Excute Entrypoint Script - migrate database & Run Server
ENTRYPOINT ["/entrypoint.sh"]
