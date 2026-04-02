# VULN: Security Misconfiguration - Running as root
FROM node:20-slim

WORKDIR /app

COPY package.json pnpm-lock.yaml ./
RUN npm i -g pnpm && pnpm install --frozen-lockfile

COPY . .

# VULN: Security Misconfiguration - Exposing debug port
EXPOSE 3001

# VULN: Security Misconfiguration - No non-root user
CMD ["node", "index.js"]
