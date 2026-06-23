# BankSaathi — Agentic AI Banking Companion for 500 Million SBI Customers

```
██████╗  █████╗ ███╗   ██╗██╗  ██╗███████╗ █████╗  █████╗ ████████╗██╗  ██╗██╗
██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║  ██║██║
██████╔╝███████║██╔██╗ ██║█████╔╝ ███████╗███████║███████║   ██║   ███████║██║
██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ╚════██║██╔══██║██╔══██║   ██║   ██╔══██║██║
██████╔╝██╔══██║██║ ╚████║██║  ██╗███████║██║  ██║██║  ██║   ██║   ██║  ██║██║
╚══════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝
```

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-green.svg)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.1.14-orange.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An Agentic AI backend engine designed for the SBI Hackathon at GFF 2026. BankSaathi proactively scans customer profiles, verifies eligibility scores, and automates onboarding and scheduling journeys using stateful multi-agent orchestrators.

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Prerequisites](#prerequisites)
5. [Quick Start](#quick-start-development)
6. [Environment Variables](#environment-variables)
7. [The 5 Agents](#the-5-agents)
8. [API Endpoints](#api-endpoints)
9. [Running Tests](#running-tests)
10. [CI/CD Pipeline](#cicd-pipeline)
11. [Compliance Notes](#compliance-notes)
12. [Contributing](#contributing)
13. [License](#license)

## Architecture Overview
```
         [WhatsApp Cloud Channel]
                     │
                     ▼
         ┌────────────────────────┐
         │      FastAPI API       │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ LangGraph Orchestrator │
         └───────────┬────────────┘
                     │
         ┌───────────┴────────────────────────┐
         ▼           ▼          ▼             ▼
      [Samjho]    [Khojo]    [Chalao]    [Queue Hatao] (Suraksha monitors)
```

## Tech Stack
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.11 | Core Runtime |
| FastAPI | 0.111.0 | Web Framework |
| LangGraph | 0.1.14 | Agent State Orchestrator |
| PostgreSQL | 16 | Transaction Data / Auditing |
| Redis | 7 | Real-time cache |
| ChromaDB | 0.5.3 | Semantic Vector Database |

## Project Structure
```
banksaathi/
├── app/
│   ├── core/       # Logging, security, middleware (request trace correlation context)
│   ├── agents/     # Samjho, Khojo, Chalao, Queue Hatao, Suraksha agents & background worker loop
│   ├── api/        # Webhook routes & metrics
│   ├── db/         # SQL connection tools, migrations SQL schemas & migration database runner
│   ├── models/     # Database entities (SQLAlchemy declarations)
│   ├── schemas/    # Pydantic v2 validation schemas
│   ├── services/   # Mock and real API client integrations (whatsapp, queue_manager buffer, sarvam, gemini, YONO)
│   ├── prompts/    # System prompt configuration files
│   └── data/       # Static configuration datasets (schemes & backup prompts)
├── docker/         # Nginx configurations and production Dockerfiles
├── scripts/        # Seeding logic and local YONO mock server
└── tests/          # Unit & integration test suites
```

## Prerequisites
- Python >= 3.11
- Docker Desktop
- PostgreSQL & Redis local instances (or via docker-compose)

## Quick Start (Development)
1. Clone repository folder structures.
2. Copy `.env.example` file setup details:
   ```bash
   cp .env.example .env
   ```
3. Initialize the development python environment virtual wrapper:
   ```bash
   make install
   ```
4. Start required services:
   ```bash
   make docker-up
   ```
5. Apply SQL tables structure schema properties:
   ```bash
   make migrate
   ```
6. Populate static scheme details:
   ```bash
   make seed
   ```
7. Start local server instances:
   ```bash
   make dev
   ```
8. Access OpenAPI docs at `http://localhost:8000/docs`.

## Environment Variables
| Variable | Description | Required | Default |
|---|---|---|---|
| `APP_ENV` | Mode of the application (`development`, `production`, `test`) | No | `development` |
| `APP_SECRET_KEY` | HMAC/session signing secret | No | `your_secret_key_here` |
| `APP_PORT` | Local application webserver port | No | `8000` |
| `DEBUG` | Verbose traceback error flags | No | `true` |
| `DATABASE_URL` | Async PostgreSQL database connection URL | Yes | None |
| `REDIS_URL` | Redis cache connection URL | Yes | None |
| `WHATSAPP_TOKEN` | Meta Graph API bearer authorization token | Yes | None |
| `WHATSAPP_PHONE_NUMBER_ID`| Meta Phone registration identification key | Yes | None |
| `WHATSAPP_VERIFY_TOKEN` | Incoming WhatsApp webhook validation token | Yes | None |
| `SARVAM_API_KEY` | Sarvam AI authentication token | Yes | None |
| `SARVAM_STT_ENDPOINT` | Sarvam voice-to-text API routing endpoint | No | `https://api.sarvam.ai/speech-to-text` |
| `SARVAM_TTS_ENDPOINT` | Sarvam text-to-speech API routing endpoint | No | `https://api.sarvam.ai/text-to-speech` |
| `GEMINI_API_KEY` | Google AI Studio authentication API key | Yes | None |
| `GEMINI_MODEL` | Target model specification | No | `gemini-1.5-flash` |
| `CHROMADB_HOST` | Vector DB connection hostname | No | `localhost` |
| `CHROMADB_PORT` | Vector DB connection port | No | `8001` |
| `LANGGRAPH_CHECKPOINT_DB` | LangGraph persistent session DB URL | Yes | None |
| `YONO_MOCK_BASE_URL` | Local API server connection URL for YONO mocks | No | `http://localhost:8002` |
| `YONO_MOCK_ENABLED` | Mock integration switch | No | `true` |
| `LOG_LEVEL` | Global logging severity threshold | No | `INFO` |

## The 5 Agents
- **Samjho**: Extracts customer intent and language profile from text or transcribes audio input.
- **Khojo**: Identifies eligible programs based on parameters.
- **Chalao**: Translates matched schemes features into YONO steps navigation scripts.
- **Queue Hatao**: Books appointments and updates digital maturity levels.
- **Suraksha**: Monitors anomaly occurrences and routes actions for review.

## API Endpoints
| Method | Path | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/v1/webhook` | Handles incoming WhatsApp API payloads | Yes |
| `GET` | `/api/v1/health` | Returns health liveness status | No |
| `GET` | `/api/v1/admin/metrics` | Serves administrative metrics panels | Yes |

## Running Tests
To run unit and integration tests with coverage tracking:
```bash
make test
```

## CI/CD Pipeline
- **Continuous Integration**: Triggers on push or PRs. Validates standard styling checks (Ruff) and types coverage (MyPy), running pytest pipelines.
- **Continuous Deployment**: Continuous deploy configuration uses Github Actions connected to Railway APIs.

## Compliance Notes
- **DPDP Act 2023**: Incorporates consent acquisition screens dynamically inside conversational intakes.
- **RBI FREE-AI Rules**: Enforces audit trails tracking human approvals (Tier-3 checks).

## Contributing
Use standard workflow branches naming patterns: `feature/name-goes-here`, `fix/bug-fix-name`.

## License
MIT License.
