# 1. استفاده از پایتون نسخه اسلیم
FROM python:3.11-slim

# 2. تنظیم متغیرهای محیطی
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    DATABASE_PATH=/data/bot_database.db \
    PORT=5000

# 3. نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. تعیین پوشه کاری
WORKDIR /app

# 5. نصب کتابخانه‌های پایتون
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. کپی کردن کدها
COPY . .

# 7. ایجاد پوشه دیتابیس در روت (خارج از /app برای پایداری بیشتر)
# ما یوزر app را حذف کردیم تا با دسترسی روت اجرا شود و مشکل Permission حل شود
RUN mkdir -p /data /app/logs && \
    chmod -R 777 /data /app/logs

# 8. اکسپوز پورت
EXPOSE 5000

# 9. هلث چک (با استفاده از پورت داینامیک ریل‌وی)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["sh", "-c", "curl -f http://localhost:${PORT:-5000}/api/stats || exit 1"]

# 10. اجرای برنامه
CMD ["python", "start_bot.py", "start"]