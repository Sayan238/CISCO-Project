# NETSAGE AI — UI/UX Redesign & Preservation Plan

**Project:** NETSAGE AI — AI + Network Troubleshooting  
**Phase:** UI/UX Professional Redesign  
**Document:** `UI_REDESIGN_STATUS.md`  

---

## 1. Existing Functionality Audit

| Feature | Current Status | Backend Service | API Endpoint |
| :--- | :--- | :--- | :--- |
| **Case Dataset Listing** | Functional (30 cases) | `case_service.get_all_cases` | `GET /api/cases` |
| **Case Detail Retrieval** | Functional | `case_service.get_case_by_id` | `GET /api/cases/{case_id}` |
| **Evidence Inspection** | Functional | `evidence_service.get_evidence_for_case` | `GET /api/cases/{case_id}/evidence` |
| **Rule Engine Evaluation** | Functional (Deterministic) | `rule_engine.analyze` | `POST /api/diagnose` |
| **AI Diagnosis Pipeline** | Functional | `diagnostician.diagnose` | `GET /api/diagnosis/{case_id}` |
| **Human Review Submission** | Functional | `review_service.record_review` | `POST /api/review` |
| **Review History Log** | Functional | `review_service.get_review_history` | `GET /api/review/history` |
| **Dashboard Analytics** | Functional | `analytics_service.get_dashboard_analytics` | `GET /api/analytics` |
| **Audit Logs (AI Responses)** | Functional | `dashboard.py` route | `GET /api/logs/ai-responses` |
| **Audit Logs (Corrections)** | Functional | `dashboard.py` route | `GET /api/logs/corrections` |
| **Health Check** | Functional | `health.py` route | `GET /api/health` |

---

## 2. Target Redesign Architecture & Layout

The UI will be restructured into an enterprise NOC / Cisco Network Troubleshooting Platform with a fixed sidebar (240px width) and top header:

### A. Layout Structure (`src/layouts/MainLayout.jsx`)
- **Header:**
  - Product branding: `NETSAGE AI` + Subtitle: `AI + Network Troubleshooting`
  - Global Search input (Ctrl+K shortcut searching Case ID, title, concept, symptom, evidence file)
  - System Online badge (`● SYSTEM ONLINE`) & Human Review Required badge (`HUMAN REVIEW REQUIRED`)
  - Admin User Profile badge
- **Sidebar (240px width):**
  - Brand header & logo
  - Navigation menu items:
    1. **Dashboard** (NOC Dashboard overview with KPI cards, Donut/Bar charts, recent cases table, quick actions, recent activity)
    2. **Cases** (Interactive 3-column workspace: Left = Filterable Case list, Center = Case detail & Packet Tracer evidence terminal, Right = Rule Engine + AI Diagnosis + Copy CLI buttons + Human Review buttons)
    3. **Evidence** (Evidence Library displaying cases, `.txt` evidence files, `.pkt` file details, interactive terminal)
    4. **AI Diagnosis** (Dedicated AI Diagnostic pipeline view for analyzing cases)
    5. **Human Review** (Human review queue with ACCEPT, EDIT, REJECT forms & audit trails)
    6. **Analytics** (Dynamic charts for concepts, severity, review agreement rate, and AI confidence)
    7. **Responsible AI** (Audit metrics cards & evaluation table for `ai_responses.json`, `human_reviews.csv`, `corrections.csv`)
    8. **AI Logs** (Full JSON/CSV raw audit log viewer)
    9. **Settings** (System status, API connectivity, model confidence thresholds)
  - Bottom Sidebar Status: `● Backend Online`, `● AI Engine Ready`, `● Dataset Loaded`, `v1.0.0`

---

## 3. Component Redesign Plan

```
src/
├── api/
│   ├── index.js               # Centralized Axios/Fetch API client
│   ├── cases.js               # Case API endpoints
│   ├── evidence.js            # Evidence API endpoints
│   ├── diagnosis.js           # Diagnosis API endpoints
│   ├── reviews.js             # Review API endpoints
│   └── analytics.js           # Analytics API endpoints
├── components/
│   ├── common/
│   │   ├── Header.jsx         # Top application bar
│   │   ├── Sidebar.jsx        # Enterprise NOC left navigation bar
│   │   ├── StatusBadge.jsx    # Severity & review badges
│   │   ├── CopyButton.jsx     # Cisco CLI copy button with feedback
│   │   └── Skeleton.jsx       # Loading skeletons
│   ├── dashboard/
│   │   ├── KpiCards.jsx       # 5 Stat Cards (Cases, PKT files, Diagnoses, Reviews, Agreement)
│   │   ├── ChartsSection.jsx  # SVG Donut & Bar charts (Concept, Review Status, Severity)
│   │   ├── RecentCasesTable.jsx # Recent cases table with status, confidence & direct link
│   │   ├── QuickActions.jsx   # Quick action buttons
│   │   └── RecentActivity.jsx # Activity feed
│   ├── workspace/
│   │   ├── CaseListPanel.jsx  # Left column case browser with concept & severity filters
│   │   ├── CaseDetailPanel.jsx# Center column case symptom, topology & evidence terminal
│   │   └── AIDiagnosisPanel.jsx# Right column rule checker, AI diagnosis, CLI fix & human review
│   ├── evidence/
│   │   ├── EvidenceLibrary.jsx# Evidence & PKT file explorer
│   │   └── PacketTracerFiles.jsx# All .pkt files table
│   ├── review/
│   │   ├── HumanReviewModal.jsx# Modal for ACCEPT, EDIT, REJECT decisions
│   │   └── ReviewQueue.jsx    # Dedicated review queue
│   ├── logs/
│   │   └── ResponsibleAILogsView.jsx # Audit trail logger
│   └── settings/
│       └── SystemSettings.jsx # Settings & diagnostic status
└── pages/
    ├── DashboardPage.jsx
    ├── CasesPage.jsx
    ├── EvidencePage.jsx
    ├── DiagnosisPage.jsx
    ├── ReviewPage.jsx
    ├── AnalyticsPage.jsx
    ├── ResponsibleAIPage.jsx
    ├── LogsPage.jsx
    └── SettingsPage.jsx
```

---

## 4. Preservation & Non-Breaking Rules

1. **Backend & API Integrity:**
   - 0 changes to working backend algorithms (`backend/rules/`, `backend/ai/`, `backend/services/`).
   - Any new helper route (e.g. `/api/packet-tracer-files`) will extend existing routes without modifying existing ones.
2. **Data Model Integrity:**
   - Case schema, evidence files, log files (`ai_responses.json`, `human_reviews.csv`, `corrections.csv`) remain unchanged.
3. **Interactive Functionality:**
   - 100% of buttons (Search, Filters, Copy CLI, Accept, Edit, Reject, Tabs, Navigation) will be fully wired and functional.
