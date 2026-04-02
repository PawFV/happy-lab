# happy - Home Security Lab

Educational hacking lab with real hardware to learn offensive and defensive security.

## Security Context

**IMPORTANT**: This is an authorized educational pentesting lab. All devices belong to the operator. The network is isolated on VLAN 1337. There is no real user data. Vulnerabilities in the apps are **intentional** and for learning.

- NEVER "fix" VulnBank or VulnShop vulnerabilities unless explicitly requested
- NEVER expose this lab to the public Internet
- All vulnerable code is marked with `# VULN:` or `// VULN:` comments

## Hardware

| Device | Hostname | IP | Role |
|---|---|---|---|
| Raspberry Pi 5 | happy-core | 10.13.37.1 | Core: monitoring, reverse proxy, MQTT broker |
| Pi Zero 2 #1 | happy-honeypot | 10.13.37.10 | Honeypot: Cowrie SSH, Dionaea |
| Pi Zero 2 #2 | happy-victim | 10.13.37.20 | Victim: VulnBank, VulnShop |
| ESP32 sensors | happy-sensor-N | 10.13.37.50-59 | IoT: ambient mic, contact mic, transducer |
| ESP32-CAM | happy-cam | 10.13.37.60 | Camera: MJPEG streaming, snapshots |

## Project Layout

```
core/          -> Raspberry Pi 5 config (OS, network, monitoring, proxy, MQTT)
nodes/         -> Pi Zero 2 config (honeypot and victim)
iot/           -> ESP32 firmware (PlatformIO, sensors, camera)
labs/          -> Intentionally vulnerable web apps (VulnBank Flask, VulnShop Express)
infra/         -> Automation (Ansible, deploy/reset scripts)
docs/          -> Documentation (architecture, setup guides, attack playbooks)
```

## Language

- **Documentation and comments**: English
- **Code** (variables, functions, commits): English
- **Logs and CLI**: English

## Code Conventions

- **Python**: Black formatter, 4 spaces, optional type hints
- **JavaScript**: Prettier, 2 spaces, const/let (not var), ESM where possible
- **C++ (ESP32)**: PlatformIO, shared libs under `iot/common/lib/`
- **Docker**: Pin image versions, one compose file per service group
- **YAML**: 2 spaces, quote strings with special characters
- **Shell scripts**: bash, `set -euo pipefail` at the top

## Common Tasks

### Add a vulnerability to VulnBank

1. Create or edit a route under `labs/vulnbank/app/routes/`
2. Add a template if there is UI under `labs/vulnbank/app/templates/`
3. Mark with `# VULN: [category] - [description]`
4. Document in `labs/vulnbank/vulns/VULNERABILITIES.md`
5. Add a test in `labs/vulnbank/tests/test_vulns.py`

### Add a vulnerability to VulnShop

1. Create or edit a route under `labs/vulnshop/src/routes/`
2. Mark with `// VULN: [category] - [description]`
3. Document in `labs/vulnshop/vulns/VULNERABILITIES.md`
4. Add a test in `labs/vulnshop/tests/test_vulns.js`

### Add a new ESP32 sensor type

1. Copy `iot/sensor-node/` as a template
2. Edit `src/main.cpp` and `include/config.h`
3. Reuse libs from `iot/common/lib/` (mqtt_client, wifi_manager, sensor_base)

### Deploy to Pi

From Linux/macOS:
```bash
bash infra/scripts/deploy.sh
```

This tars the project (excluding .git, node_modules, .venv, etc.), uploads it to the Pi via SCP/rsync, and runs `docker compose up --build -d`.

### First-time Pi setup

Install Docker on a fresh Pi:
```bash
ssh happy-core "bash -s" < infra/scripts/setup-pi.sh
```

### Lab reset

```bash
bash infra/scripts/reset-lab.sh
```

### Health check

```bash
bash infra/scripts/health-check.sh
```

## Vulnerable Apps

### VulnBank (Python/Flask) — port 5000

Fake bank with: SQL injection, broken auth, IDOR, XSS (reflected/stored/DOM), CSRF, broken access control, mass assignment, information disclosure.

### VulnShop (Node.js/Express) — port 3001

Fake shop with: command injection, SSRF, insecure deserialization, path traversal, JWT manipulation, NoSQL injection, unrestricted upload, prototype pollution.

## Monitoring Stack (Pi 5)

- **Grafana** (:3000) — Dashboards
- **Prometheus** (:9090) — Metrics
- **Loki** (:3100) — Logs
- **AlertManager** (:9093) — Alerts
- **Traefik** (:80/:8080) — Reverse proxy
- **Mosquitto** (:1883) — MQTT broker

## Deploy

The Pi (happy-core) has no GitHub access. Deployment is done via SSH:

1. Develop locally on your PC (this repo has git)
2. Run `bash infra/scripts/deploy.sh` from your Unix dev machine
3. The script tars the project, uploads via SCP, extracts, and runs `docker compose up --build -d`

SSH config (`~/.ssh/config`):
```
Host happy-core
    HostName 192.168.1.137
    User darkin
    IdentityFile ~/.ssh/id_ed25519
```

Apps after deploy:
- VulnBank → http://192.168.1.137:5000
- VulnShop → http://192.168.1.137:3001

## Testing

> **Note**: VulnBank tests require a real MySQL database to accurately test SQL injection vulnerabilities. Make sure the MySQL container is running first.

```bash
# Start MySQL container (from project root)
docker compose up -d mysql

# VulnBank
cd labs/vulnbank && pytest tests/ -v

# VulnShop
cd labs/vulnshop && pnpm test

# Infrastructure
bash infra/scripts/health-check.sh
```
