# VULN: Security Misconfiguration - Running as root
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# VULN: Security Misconfiguration - Exposing debug port
EXPOSE 5000

# VULN: Security Misconfiguration - Debug mode enabled, running as root
ENV FLASK_APP=app:create_app
ENV FLASK_DEBUG=1
ENV FLASK_RUN_RELOAD=0

CMD ["flask", "run", "--host=0.0.0.0"]
