# NetSage-AI — Project Status Report

**Project:** NETSAGE AI — AI + Network Troubleshooting (Cisco Internship Project)  
**Timestamp:** 2026-08-25  

---

## 1. Directory Structure Status

The root folder `NetSage-AI/` contains the following designated directories:

| Directory | Status | Notes |
| :--- | :--- | :--- |
| `backend/` | Existing (Empty) | Ready for FastAPI implementation |
| `dashboard/` | Existing (Empty) | Ready for React + Vite + Tailwind CSS frontend |
| `data/` | Existing | Contains `cases/`, `evidence/`, `logs/`, `packet_tracer/` |
| `docs/` | Existing (Empty) | For documentation artifacts |
| `prompts/` | Existing (Empty) | Ready for prompt templates & system prompts |
| `reports/` | Existing (Empty) | For generated evaluation reports |
| `tests/` | Existing (Empty) | Ready for pytest suite |

---

## 2. Existing Data Inventory

### A. CSV Dataset (`data/cases/cases.csv`)
- **Status:** Present (9,482 bytes)
- **Total Cases:** 30 cases (`NET-001` through `NET-030`)
- **Columns Present:** `case_id`, `title`, `symptome`, `topology`, `expected-fault`, `osi_layer`, `concept`, `severity`, `expected_next_command`, `expected_fix`

### B. Packet Tracer Files (`data/packet_tracer/`)
- **Total .pkt Files Found:** 29 files
- **Files Present:**
  - `NET-001-Wrong-VLAN-Assignment.pkt`
  - `NET-002-Trunk-Disabled.pkt`
  - `NET-003-VLAN-30-Missing.pkt`
  - `NET-004-VLAN-30-Not-Allowed-on-Trunk.pkt`
  - `NET-005-Access-Port-in-Trunk-Mode.pkt`
  - `NET-006-VLAN-30-Subinterface-Shutdown.pkt`
  - `NET-007-Wrong-VLAN-30-Gateway-IP.pkt`
  - `NET-008-Wrong-PC-Default-Gateway.pkt`
  - `NET-009-Wrong-Subnet-Mask.pkt`
  - `NET-011_NAT_Inside_Outside_Misconfiguration.pka.pkt`
  - `NET-012-NAT-ACL-Mismatch.pkt`
  - `NET-013.pkt` (Reference case)
  - `NET-014.pkt` (Reference case)
  - `NET-015-Wrong-DHCP-Assignment.pkt`
  - `NET-016-Wrong-DHCP-DNS-Assignment.pkt`
  - `NET-017-Wrong DHCP-Assignment.pkt`
  - `NET-018-Wrong-DNS-SERVICE-OFF-Assignment.pkt`
  - `NET-019-Wrong-WirelessWIFI-Assignment.pkt`
  - `NET-020-Wrong-WirelessRouting -Assignment - Copy.pkt`
  - `NET-021-Correct-WirelessRouting -Assignment.pkt`
  - `NET-022-Wrong_WIFI_Range-Assignment.pkt`
  - `NET-023-Correct-SecurityCamera-Assignment.pkt`
  - `NET-024-Wrong-WirelessRouting-Assignment.pkt`
  - `NET-025-Wrong-DNS_ACL-Assignment.pkt`
  - `NET-026-Wrong-DHCP-Assignment.pkt`
  - `NET-027-Wrong-Wireless-Assignment.pkt`
  - `NET-028-Wrong-DHCP-Assignment.pkt`
  - `NET-029-Correct-NAT-Assignment.pkt`
  - `NET-030.pkt`
- **Missing .pkt File:** `NET-010` (ACL Blocking Specific Host) is missing a Packet Tracer `.pkt` file in `data/packet_tracer/`.

### C. Evidence TXT Files (`data/evidence/`)
- **Status:** Present (30 files)
- **Files:** `case01.txt` through `case030.txt`
- **Missing Folder Structure:** Case-specific directories `data/evidence/NET-001/` to `NET-030/` with individual command outputs (`show_vlan.txt`, `show_interfaces_trunk.txt`, `show_running_config.txt`, `ipconfig.txt`, `ping_result.txt`, `topology.txt`) need to be organized/populated while preserving `case01.txt`–`case030.txt`.

### D. Prompts (`prompts/`)
- **Status:** Currently empty.
- **Required Files:**
  - `prompts/diagnose_prompt.md`
  - `prompts/explain_prompt.md`
  - `prompts/next_command_prompt.md`
  - `prompts/fix_prompt.md`
  - `prompts/templates/` (`vlan.txt`, `trunk.txt`, `routing.txt`, `dhcp.txt`, `dns.txt`, `acl.txt`, `nat.txt`, `wireless.txt`)

### E. Backend Code (`backend/`)
- **Status:** Currently empty. Structure to build: FastAPI app with config, API routes, schemas, AI diagnoser, deterministic rule engine, services, and utilities.

### F. Dashboard (`dashboard/`)
- **Status:** Currently empty. Structure to build: React + Vite + Tailwind CSS dashboard.

---

## 3. Cases & Evidence Coverage Summary

- **Total Cases Defined:** 30 (`NET-001` to `NET-030`)
- **Cases with CSV Entry:** 30 / 30 (100%)
- **Cases with TXT Evidence File:** 30 / 30 (100%)
- **Cases with Packet Tracer File:** 29 / 30 (96.7%) — `NET-010` missing .pkt file.
- **Per-Case Evidence Folders (`data/evidence/NET-XXX/`):** 0 / 30 (Need directory organization with detailed command TXT files).

---

## 4. Recommended Next Implementation Steps

1. **Populate Prompts & Templates**:
   - Create system prompts in `prompts/` forcing structured JSON output and safety rules.
   - Create template files in `prompts/templates/` for each network concept domain.

2. **Organize Evidence Subfolders**:
   - Create `data/evidence/NET-001/` through `data/evidence/NET-030/` folders.
   - Copy/split evidence details from `case01.txt`–`case030.txt` into individual files (`show_running_config.txt`, `ipconfig.txt`, `ping_result.txt`, `topology.txt`, etc.) while keeping original `caseXX.txt` intact.

3. **Build Backend (Python + FastAPI)**:
   - Setup CSV Loader supporting both `symptom`/`symptome` and `expected_fault`/`expected-fault` schemas.
   - Implement deterministic Rule Engine (`vlan`, `trunk`, `routing`, `dhcp`, `dns`, `acl`, `nat`, `wireless`).
   - Implement AI Diagnoser service with fallback local analysis & confidence calculation.
   - Implement Human Review & Responsible AI Logging (`data/logs/ai_responses.json`, `data/logs/human_reviews.csv`, `data/logs/corrections.csv`).
   - Implement REST APIs (`/api/cases`, `/api/diagnose`, `/api/review`, `/api/analytics`, `/api/health`, etc.).

4. **Build Dashboard (React + Vite + Tailwind CSS)**:
   - Modern networking/cybersecurity UI aesthetic (dark theme, glassmorphism, dynamic stats, diagnostic timeline).
   - Case Browser, Detailed Evidence Viewer, AI Diagnosis display with Confidence & Supporting Evidence, Human Review actions (`ACCEPT`, `EDIT`, `REJECT`), and Analytics / Responsible AI Logs.

5. **Automated Unit & Integration Tests**:
   - Tests for CSV loading, rule engine logic, AI schemas, review workflow, and API routes.
