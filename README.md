# NETSAGE — Cisco Packet Tracer AI Troubleshooting Assistant

NETSAGE is an enterprise AI-assisted network troubleshooting system for Cisco Packet Tracer labs and network operations centers (NOC). It reads network troubleshooting case metadata, Packet Tracer CLI outputs (e.g. `show vlan brief`, `show interfaces trunk`, `show ip interface brief`, `ipconfig`), executes a deterministic rule checker, generates structured diagnostic reasoning using the **Grok AI API (xAI)**, enforces human-in-the-loop review, and logs audit entries for Responsible AI compliance.

---

## 🏗 Architecture Overview

```
Frontend Dashboard (React + Vite + Tailwind CSS)
        ↓
Backend API (FastAPI)
        ↓
Evidence Loader (TXT Evidence & .pkt Mapping)
        ↓
Deterministic Rule Checker (Pattern Matching)
        ↓
Grok AI Diagnosis (xAI API)
        ↓
Human Review (Accept / Edit / Reject)
        ↓
Final Diagnosis + Responsible AI Log
```

---

## ⚙ Installation & Environment Setup

### 1. Requirements
- Python 3.10+
- Node.js 18+ and npm

### 2. Environment Configuration (.env)
Create a `.env` file in the root directory:

```env
XAI_API_KEY=your_grok_api_key_here
GROK_MODEL=grok-2-latest
API_HOST=127.0.0.1
API_PORT=8000
```

> **IMPORTANT**: The API key must ONLY exist in `.env`. It is never logged or exposed to the frontend.

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Dashboard Frontend Dependencies
```bash
cd dashboard
npm install
cd ..
```

---

## 🚀 How to Start the System

### 1. Start the Backend API
From the root project directory:
```bash
python backend/main.py
```
Or via Uvicorn:
```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Swagger Docs: `http://127.0.0.1:8000/docs`
- Health Endpoint: `http://127.0.0.1:8000/api/health`

### 2. Start the Frontend Dashboard
From the `dashboard/` folder:
```bash
cd dashboard
npm run dev
```
- Dashboard UI: `http://localhost:3000`

---

## 🤖 How Grok AI Diagnosis Works

1. **Evidence Ingestion**: When a case (e.g., `NET-001`) is selected, `evidence_loader.py` retrieves CLI evidence outputs (`show_vlan.txt`, `show_interfaces_trunk.txt`, `ipconfig.txt`, etc.).
2. **Rule Checker Execution**: `rule_checker.py` evaluates the CLI evidence for deterministic fault signatures (e.g. VLAN mismatch, trunk missing, subinterface shutdown, NAT inside/outside swap, ACL blocks).
3. **Grok Prompt Engineering**: `grok_client.py` constructs a structured prompt sent to xAI's Grok API (`https://api.x.ai/v1/chat/completions`) with strict system rules forbidding hallucinated topology or CLI outputs.
4. **JSON Validation & Safety Enforcement**: Grok returns a structured JSON diagnosis containing root cause, confidence score (0-100), supporting evidence, recommended single next CLI command, and recommended fix.
5. **Human-in-the-Loop Mandate**: Every AI diagnosis includes `needs_human_review: true`. Recommended commands and fixes are never executed automatically.
6. **Graceful Fallback**: If Grok API is unreachable or returns invalid JSON, the backend falls back to rule-checker results without crashing.

---

## 👤 How Human Review & Responsible AI Logging Work

1. **Review Decisions**: Network Engineers audit AI diagnoses in the dashboard with options to:
   - `[ ACCEPT ]`: Confirm AI diagnosis as accurate.
   - `[ EDIT ]`: Refine root cause or fix command.
   - `[ REJECT ]`: Mark diagnosis as inaccurate and supply human correction.
2. **Audit Logging**: Every diagnosis and review action is recorded in:
   - `data/logs/responsible_ai_log.json`
   - `data/logs/human_reviews.csv`
   - `data/logs/corrections.csv`
3. **Analytics**: The system computes real-time metrics including total cases, cases by concept/severity, human-AI agreement rate, and total AI corrections.

---

## ➕ How to Add a New Packet Tracer Case

1. **Add Metadata to CSV**:
   Add a new row in `data/cases/cases.csv`:
   ```csv
   NET-031,Title Here,Symptom Description,Topology,Expected Fault,Layer 3,Routing,High,show ip route,Fix command
   ```
2. **Add Evidence TXT Files**:
   Create directory `data/evidence/NET-031/` and populate command output text files:
   - `data/evidence/NET-031/case.txt`
   - `data/evidence/NET-031/show_ip_route.txt`
   - `data/evidence/NET-031/show_ip_interface_brief.txt`
3. **Add Packet Tracer File (Optional)**:
   Place `NET-031.pkt` in `data/packet_tracer/`.
4. **Add Custom Rule (Optional)**:
   Add a pattern match method `_check_net_031(...)` in `backend/rule_checker.py`.

---

## 📡 API Endpoints

- `GET /api/health` — Health check & Grok service status.
- `GET /api/cases` — List all troubleshooting cases.
- `GET /api/cases/{case_id}` — Get full details of a specific case.
- `GET /api/cases/{case_id}/evidence` — Get CLI evidence TXT files for a case.
- `POST /api/cases/{case_id}/diagnose` — Run rule checker + Grok AI diagnosis.
- `POST /api/cases/{case_id}/review` — Submit human review decision (accept, edit, reject).
- `GET /api/responsible-ai` — Retrieve responsible AI audit logs.
- `GET /api/analytics` — Get system analytics & human-AI agreement statistics.
