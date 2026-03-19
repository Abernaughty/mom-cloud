# 🌤️ mom-cloud

**Automated photo backup and archival pipeline** — solving Mom's iCloud storage woes while building cloud/DevOps portfolio skills.

## Problem

Mom's phone and iCloud are perpetually full because of photos. She needs a simple, automated way to offload photos to cheap cloud storage without thinking about it.

## Solution

An automated pipeline that:
1. **Ingests** photos from iCloud using `icloud-photos-downloader`
2. **Deduplicates** and organizes by date
3. **Uploads** to Azure Blob Storage (Cool/Archive tier) for pennies/month
4. **Monitors** the pipeline with alerts if something breaks
5. *(Optional)* Serves a self-hosted photo gallery via Immich or PhotoView

## Architecture

```
iCloud ──► icloud-photos-downloader ──► Local staging (Raspberry Pi)
                                              │
                                    Dedup + organize by date
                                              │
                                    Upload to Azure Blob Storage
                                        (Cool / Archive tier)
                                              │
                                    Monitoring + Alerting
                                      (Grafana / Loki)
```

## Tech Stack

| Layer | Tool |
|---|---|
| Ingestion | `icloud-photos-downloader` (CLI) |
| Scripting | Python 3.11+ |
| Cloud Storage | Azure Blob Storage (Cool/Archive) |
| IaC | Terraform |
| Containerization | Docker / Docker Compose |
| Automation | cron / systemd on Raspberry Pi |
| Monitoring | Grafana + Loki |
| Networking | Tailscale (secure remote access) |
| Gallery (optional) | Immich / PhotoView |

## Project Structure

```
mom-cloud/
├── src/                    # Python source code
│   ├── ingest.py           # iCloud download + staging logic
│   ├── dedup.py            # Deduplication engine
│   ├── upload.py           # Azure Blob upload logic
│   └── config.py           # Configuration loader
├── infra/                  # Terraform infrastructure
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
├── docker/                 # Container definitions
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/                # Automation and helper scripts
│   └── setup-pi.sh         # Raspberry Pi bootstrap script
├── monitoring/             # Observability config
│   ├── grafana/
│   └── loki/
├── tests/                  # Unit and integration tests
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI pipeline
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md
```

## Getting Started

### Prerequisites
- Python 3.11+
- Docker &amp; Docker Compose
- Terraform CLI
- Azure account (free tier works to start)
- Raspberry Pi (optional, for always-on automation)

### Quick Start
```bash
# Clone the repo
git clone https://github.com/Abernaughty/mom-cloud.git
cd mom-cloud

# Copy environment template
cp .env.example .env
# Edit .env with your Azure + iCloud credentials

# Install Python dependencies
pip install -r requirements.txt

# Run the pipeline
python src/ingest.py
```

## Milestones

- [ ] **M1 — Foundation**: Project scaffolding, config, environment setup
- [ ] **M2 — Ingestion**: iCloud download + local staging pipeline
- [ ] **M3 — Cloud Storage**: Azure Blob integration with lifecycle policies
- [ ] **M4 — Automation**: Dockerize + schedule on Raspberry Pi
- [ ] **M5 — Monitoring**: Grafana dashboards + alerting
- [ ] **M6 — Gallery** *(stretch)*: Self-hosted photo browsing UI

## License

MIT
