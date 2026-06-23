# BankSaathi Architecture Guide

BankSaathi acts as an Agentic AI system that interfaces between SBI customers and core services using LangGraph for multi-agent coordination.

## Agent System Overview
- **Samjho Node**: Conducts intent detection, language profiling, and risk mapping.
- **Khojo Node**: Examines profile parameters against schemes cataloged in ChromaDB and metadata DB.
- **Chalao Node**: Conducts stateful YONO app UI step-by-step guidance.
- **Queue Hatao Node**: Manages proactive notifications and branch appointments.
- **Suraksha Node**: Monitors anomalies and acts as the gatekeeper for compliance.
