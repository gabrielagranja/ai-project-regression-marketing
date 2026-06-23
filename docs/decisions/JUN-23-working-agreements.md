# DEC-000 | Working Agreements

## Status

Approved

## Date

2026-06-23

---

## Context

This document establishes the working agreements, documentation standards, Git workflow and project management practices that will be followed throughout the development of the AI-Powered Digital Marketing Revenue Prediction project.

The purpose of these agreements is to ensure consistency, traceability, reproducibility and professional project organization.

---

## Decision

The project will follow the standards and conventions described in this document.

---

# Documentation Standards

## Format

All project documentation must be written in Markdown (`.md`).

## Editor

All documentation should be created and maintained using Visual Studio Code.

## Language

English will be used as the primary language for project documentation.

## Principles

- Documentation must be updated continuously.
- Documentation must reflect the actual state of the project.
- Empty documents should be avoided.
- Information should not be duplicated across files.
- Major decisions must be documented.
- Project progress must be traceable through Git and project documentation.

---

# Documentation Structure

```text
docs/
│
├── PROJECT_MASTER_RECORD.md
├── PROJECT_LOG.md
│
├── daily/
│   └── YYYY-MM-DD.md
│
└── decisions/
    └── DEC-XXX-name.md
```

## PROJECT_MASTER_RECORD.md

Contains the current and official state of the project.

Includes:

- Project objective
- Business problem
- Dataset
- Target variable
- Technology stack
- Current milestone
- Next deliverables

## PROJECT_LOG.md

Contains major milestones, completed phases and project evolution.

Should only record significant achievements and project-level changes.

## daily/

Contains daily working session records.

Each file must follow the format:

```text
YYYY-MM-DD.md
```

## decisions/

Contains significant project decisions and their rationale.

Each decision must have its own document.

Examples:

```text
DEC-000-working-agreements.md
DEC-001-target-variable.md
DEC-002-dataset-selection.md
DEC-003-model-selection.md
```

---

# Git Workflow

## Branch Strategy

Major workstreams must be developed in dedicated branches.

Examples:

```text
docs/project-governance
feature/dataset-assessment
feature/eda-analysis
feature/feature-engineering
feature/modeling
feature/streamlit-app
feature/dockerization
feature/deployment
```

## Commit Policy

Commits should represent a complete logical unit of work.

Do not commit:

- Incomplete work
- Broken code
- Temporary experiments

## Commit Convention

Examples:

```text
docs: add project governance documentation
docs: document dataset assessment
feat: implement baseline regression model
feat: create streamlit prediction interface
fix: correct preprocessing pipeline
test: add preprocessing unit tests
```

---

# Project Workflow

The project should follow the sequence below:

```text
Business Understanding
        ↓
Dataset Assessment
        ↓
Exploratory Data Analysis
        ↓
Feature Engineering
        ↓
Modeling
        ↓
Application Development
        ↓
Deployment
```

Major deviations from this workflow should be documented.

---

# Project Management

## Daily Records

Each working session should be documented in the `daily/` directory.

## Decision Records

Important project decisions must be documented using a dedicated decision record.

## Milestones

Major achievements should be recorded in `PROJECT_LOG.md`.

## Governance

The project will be managed using a lightweight PMO approach, ensuring:

- Traceability
- Documentation discipline
- Controlled scope
- Clear decision-making process

---

# Success Criteria

## Academic Objectives

- Functional regression model
- Proper evaluation metrics
- Complete documentation
- Reproducible workflow

## Portfolio Objectives

- Professional repository structure
- Business-oriented problem definition
- Clean Git history
- Deployable application
- Clear storytelling and insights

---

## Expected Impact

These working agreements provide a consistent framework for project management, development, documentation and decision-making throughout the project lifecycle.