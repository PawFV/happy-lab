---
name: lab-operations
description: Run lab operations like health checks, full reset, deploy, and service management. Use when the user wants to check lab status, reset the lab, deploy changes, or troubleshoot services.
---

# Lab Operations

## Health Check

Verify all services are running:

```bash
bash infra/scripts/health-check.sh
```

Manual checks:

```bash
# VulnBank
curl -s http://10.13.37.20:5000/ | head -20

# VulnShop
curl -s http://10.13.37.20:3001/ | head -20

# Grafana
curl -s http://10.13.37.1:3000/api/health

# Prometheus
curl -s http://10.13.37.1:9090/-/healthy

# MQTT
mosquitto_sub -h 10.13.37.1 -t '#' -C 1 -W 5
```

## Lab Reset

Full reset to clean state (wipes DBs, sessions, uploads):

```bash
bash infra/scripts/reset-lab.sh
```

## Local Dev (Docker Compose)

```bash
docker compose up -d              # start all
docker compose down               # stop all
docker compose up -d --build      # rebuild and start
docker compose logs -f vulnbank   # follow vulnbank logs
docker compose logs -f vulnshop   # follow vulnshop logs
docker compose restart vulnbank   # restart single service
```

## Deploy to Lab Network

Uses Ansible playbooks from `infra/`:

```bash
cd infra && ansible-playbook -i inventory.yml deploy.yml
```

## Testing

```bash
# VulnBank
cd labs/vulnbank && pytest tests/

# VulnShop
cd labs/vulnshop && pnpm test
```

## Troubleshooting

| Symptom | Check |
|---|---|
| VulnBank 500 error | `docker compose logs vulnbank` — likely DB init issue |
| VulnShop not starting | `docker compose logs vulnshop` — check node errors |
| MQTT not receiving | `mosquitto_sub -h 10.13.37.1 -t '#' -v` |
| Grafana no data | Check Prometheus targets at `:9090/targets` |
| ESP32 not connecting | Check WiFi credentials in `config.h` |
