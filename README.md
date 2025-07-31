
# BioWeave MVP
BioWeave is a tool for biotech labs and companies to streamline their data acquisition and processing pipelines. High-value experimental or clinical data is frequently locked up in incompatible formats, spreadsheets, or disparate systems, making it hard to use. Scientists and data teams end up spending enormous effort on data wrangling and cleanup instead of actual analysis. Interoperability is a also key challenge. Instruments and vendors often output data in bespoke CSV/Excel files meant for human reading, not machine-ready. Labs resort to manual work or custom scripts to combine such data. 

Poor data integration also impedes the adoption of AI/ML in biotech. High-quality, well-labeled datasets are needed for AI, but many organizations aren’t there yet.

We hope to create a tool that lets biotech firms automate their data processing so they can focus on what matters. 

This is currently out‑of‑the‑box minimum‑viable backend that turns messy CRO/Instrument spreadsheets (CSV/Excel)
into a clean, schema‑aligned, FAIR‑annotated table stored in Postgres, and (optionally) pushed to Benchling.

---

## Quick Start (Docker)

```bash
# 1. Clone / unzip this directory
cd bioweave_mvp

# 2. Copy env template and fill in (optional) Benchling token
cp .env.example .env
# edit .env with your DB url or use defaults and set BENCHLING_API_TOKEN

# 3. Build & run
docker compose up --build
```

Navigate to <http://localhost:8000/docs> and try `/upload` with a sample CSV.

---

## Local Dev (no Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start Postgres however you like and export DATABASE_URL
export DATABASE_URL=postgresql+psycopg2://bioweave:bioweave@localhost:5432/bioweave
uvicorn bioweave.main:app --reload
```

---

## Directory Layout

```
bioweave_mvp/
├─ bioweave/            # Python package
│  ├─ __init__.py
│  ├─ config.py         # Environment settings
│  ├─ models.py         # SQLAlchemy models
│  ├─ schema_def.py     # Pandera schema
│  ├─ ingest.py         # Core ingest/clean pipeline
│  ├─ benchling_client.py
│  └─ mapping.yml       # Field‑alias mapping
├─ main.py              # Entrypoint (delegates to package)
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ .env.example
```

---

## Extending

* Add more aliases in `bioweave/mapping.yml`
* Extend `bioweave/schema_def.py` for extra columns & rules
* Swap in Celery/RabbitMQ if you need async ingests
* Layer in PDF/patent agents reusing the ingest queue and metadata tables

More coming soon!
