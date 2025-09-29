# Dockerfile
# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Django port
EXPOSE 8000

ENV DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1,13.62.67.73,www.fieldmgmtgx.dpdns.org,fieldmgmtgx.dpdns.org'

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
