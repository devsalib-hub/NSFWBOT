# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# --- بخش اصلاح شده برای پایداری در Railway ---
# ایجاد یوزر و پوشه‌ها
RUN useradd --create-home --shell /bin/bash --uid 1000 app && \
    mkdir -p /app/data /app/logs

# تنظیم دسترسی بسیار آزاد برای پوشه دیتابیس 
# این خط باعث می‌شود حتی اگر Volume روت باشد، یوزر app بتواند در آن بنویسد
RUN chown -R app:app /app && \
    chmod -R 777 /app/data /app/logs

# Switch to non-root user
USER app

# Expose port (ریل‌وی معمولا از این استفاده می‌کند)
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ["sh", "-c", "curl -f http://localhost:${PORT:-5000}/api/stats || exit 1"]

# Run the application
CMD ["python", "start_bot.py", "start"]