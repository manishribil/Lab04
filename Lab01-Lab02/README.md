# Lab 1 – Requirements Engineering & UML Use-Case Modelling

**Course:** Software Engineering (UE24CS341A)
**Semester:** Sem-5 / Section E
**Student:** Manish Bala M (PES1UG24CS263)
**Faculty:** Ambika K
**Problem Statement:** #18 — Healthcare & Telemedicine

## Problem Statement

**Clinical Trial Subject Recruitment Engine**

Medical research institutions require an eligibility pre-screening platform for clinical trials, tracking subject inclusion/exclusion criteria, informed consent milestones, and visit compliance logs.

**Stakeholders / Actors:** Trial Candidate, Clinical Researcher, System Administrator

## Repository Contents

| File | Description |
|---|---|
| `Lab1_Requirements_Table_PS18.docx` | Requirements table — 5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001, NFR-002), each with ID, Type, Description, Priority, Acceptance Criteria, and Rationale |
| `Lab1_UseCase_Diagram_PS18.pdf` | UML Use-Case Diagram with all actors, primary use cases, one `«include»` relationship, and one `«extend»` relationship |
| `Lab1_UseCase_Flow_PS18.docx` | One-page use-case flow specification for UC-02 (Complete Eligibility Screening Survey) — preconditions, postconditions, main success scenario, and one alternate flow |
| `README.md` | This file |

## Requirements Summary

| Req ID | Type | Priority | Summary |
|---|---|---|---|
| FR-001 | Functional | High | Evaluate candidate survey responses against protocol criteria and classify eligibility |
| FR-002 | Functional | High | Candidate profile registration (demographics, medical history, medications) |
| FR-003 | Functional | High | Capture and timestamp informed consent milestones (e-signature) |
| FR-004 | Functional | Medium | Log and review visit compliance (scheduled vs. actual dates) |
| FR-005 | Functional | Medium | Notify candidate of eligibility outcome within 24 hours |
| NFR-001 | Nonfunctional | High | 21 CFR Part 11 compliance with cryptographic audit trails |
| NFR-002 | Nonfunctional | High | Encrypt PHI at rest (AES-256) and in transit (TLS 1.2+) |

## Actors & Use Cases

**Actors:** Trial Candidate, Clinical Researcher, System Administrator

**Use Cases:**
- UC-01 — Register Candidate Profile
- UC-02 — Complete Eligibility Screening Survey (**«include»** UC-06)
- UC-03 — View Eligibility Status
- UC-04 — Provide Informed Consent (**«extend»** by UC-07)
- UC-05 — Log Trial Visit Compliance
- UC-06 — Evaluate Eligibility Criteria
- UC-07 — Request Consent Clarification
- UC-08 — Manage Protocol Criteria

