# 🚨 Enterprise Agent DevOps  
## Autonomous AI Incident Commander (Multi-Agent Orchestrated System)

---

<p align="center">
  <b>AI-driven Incident Lifecycle Automation</b><br>
  Multi-Agent Reasoning • Decision Engine • Jira Escalation • Learning Memory
</p>

---

# 🧠 What Is This?

Enterprise Agent DevOps is a **multi-stage AI orchestration system** that autonomously handles production incidents:

- Incident classification  
- Root cause reasoning  
- Action planning  
- Remediation execution (simulated)  
- Health validation  
- Governance decision logic  
- Escalation to Jira  
- Learning memory tracking  

This is NOT a chatbot.

It is a **structured AI system with governance and decision control.**

---

# 🎯 Problem It Solves

In enterprise environments:

- Incidents require multiple teams (DB, Infra, App)
- Root cause is often ambiguous
- Escalation is inconsistent
- MTTR is high
- Engineers manually triage repetitive issues

This project acts as an:

> 🧠 Autonomous Incident Commander

Reducing:
- Human triage effort
- Escalation delays
- Cognitive overload
- Root cause bias

---

# 🏗️ System Architecture

## 🔷 High-Level Architecture

            ┌─────────────────────┐
            │   User Incident     │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │  Incident Agent     │
            │ (Severity + Service)│
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │ Root Cause Agent    │
            │ (Hypothesis + Conf) │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │ Action Planning     │
            │ Agent               │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │ Remediation Engine  │
            │ (Execute Actions)   │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │ Health Validator    │
            │ (Error Rate Check)  │
            └──────────┬──────────┘
                       ↓
            ┌─────────────────────┐
            │ Decision Engine     │
            │ APPROVE / RETRY /   │
            │ ESCALATE            │
            └──────────┬──────────┘
                       ↓
        ┌─────────────────────────────┐
        │ Jira Escalation (If Needed) │
        └──────────┬──────────────────┘
                   ↓
          ┌─────────────────┐
          │ Memory Engine   │
          │ (Learning Layer)│
          └─────────────────┘

          
---

# 🤖 Agents Implemented (Current Scope)

## 1️⃣ Incident Agent
- Classifies severity (P1–P4)
- Identifies impacted service
- Outputs structured JSON

## 🧠 Example Classification Output

```json
{
  "severity": "P1",
  "service": "Checkout",
  "confidence": 0.95
}
```

---

## 2️⃣ Root Cause Agent

**Responsibilities**

- Analyzes symptoms  
- Produces hypothesis  
- Provides evidence list  
- Returns confidence score  

---

## 3️⃣ Action Planning Agent

**Responsibilities**

- Generates remediation plan  
- Prioritizes actions  
- Produces structured output  

---

## 4️⃣ Remediation Engine

**Simulates**

- Action execution  
- Success / failure rate  
- Remediation effectiveness  

---

## 5️⃣ Health Validation Agent

**Simulates**

- Error rate evaluation  

**System States**

- `STABLE`
- `UNSTABLE`

---

## 6️⃣ Decision Engine (Governance Layer)

**Evaluates**

- Incident severity  
- Agent confidence  
- Remediation success rate  
- Current error rate  
- Attempt number  

**Outputs**

- `APPROVE`
- `RETRY`
- `ESCALATE`

---

## 7️⃣ Jira Integration (Real API)

If the system remains unstable:

- AI generates structured Jira payload  
- Real Jira REST API call  
- Ticket automatically created  

**Ticket Includes**

- Title  
- Priority  
- Root cause  
- Recommended actions  

> This is NOT mocked. It uses a real Jira REST integration.

---

## 8️⃣ Learning Memory Engine

**Stores**

- Service  
- Root cause  
- Remediation success  
- Timestamp  

**Current Stage**

- Passive memory logging  

**Future Evolution**

- Pattern detection  
- Confidence tuning  
- Reinforcement-style learning  

---

## 🖥️ Dashboard (Streamlit)

The dashboard visualizes:

- Incident classification  
- Root cause reasoning  
- Action plan  
- Remediation results  
- Health state  
- Decision verdict  
- Jira escalation result  
- Memory history  

It shows a visible decision loop — not just logs.

---

## 🔬 Orchestration Logic

### Core Lifecycle

```
Incident
   ↓
Reason
   ↓
Plan
   ↓
Execute
   ↓
Validate
   ↓
Decide
   ↓
Escalate (if needed)
   ↓
Learn
```

---

## 📂 Project Structure

```
enterprise-agent-devops/
│
├── orchestrator/
│   ├── agents/
│   │   ├── incident_agent.py
│   │   ├── root_cause_agent.py
│   │   ├── action_agent.py
│   │   └── jira_agent.py
│   │
│   ├── executors/
│   │   ├── remediation_engine.py
│   │   └── validation_agent.py
│   │
│   ├── tools/
│   │   └── jira_client.py
│   │
│   ├── decision_engine.py
│   ├── memory_engine.py
│   ├── pipeline.py
│   └── main.py
│
├── dashboard/
│   └── app.py
│
└── README.md
```

---

## ⚙️ Tech Stack

- Python  
- SAP AI Core (LLM deployment)  
- Streamlit  
- Jira REST API  
- Modular Agent Architecture  
- Structured JSON prompting  

---

## 🔮 Future Roadmap

- Multi-agent debate system (DB vs Infra vs Network)  
- Scoring engine for hypothesis ranking  
- Real Prometheus metrics integration  
- Kubernetes remediation execution  
- Adaptive confidence weighting  
- Closed-loop autonomous healing  
