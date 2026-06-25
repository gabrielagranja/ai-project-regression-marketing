# PROJECT MASTER RECORD

## Project Information

| Field | Value |
|---------|---------|
| Project Name | AI-Powered Digital Marketing Revenue Prediction |
| Project Type | Machine Learning Regression |
| Author | Gabriela Granja |
| Repository | ai-project-regression-marketing |
| Status | In Progress |
| Current Phase | Sprint 0 - Planning & Governance |

---

## Business Problem

Marketing teams invest significant budgets across multiple digital channels. Estimating campaign revenue before launching a campaign can improve planning, budget allocation, forecasting and overall marketing performance.

---

## Project Objective

Develop a machine learning solution capable of predicting digital marketing campaign revenue using campaign configuration, audience characteristics and campaign performance metrics.

The project aims to simulate a real-world business use case while following a complete machine learning lifecycle, from data exploration to deployment.

---

## Target Variable

### Current Target

```text
Revenue
```

### Status

Preliminary selection pending dataset validation.

---

## Dataset

### Selected Dataset

Digital Marketing Performance Dataset

### Source

Kaggle

### Status

Pending assessment and validation.

---

## Technology Stack

### Data Analysis

- Python
- Pandas
- NumPy

### Visualization

- Matplotlib
- Seaborn

### Machine Learning

- Scikit-Learn
- Optuna

### Application

- Streamlit

### Engineering

- Docker

---

## Project Scope

### Included

- Exploratory Data Analysis (EDA)
- Data Cleaning
- Feature Engineering
- Regression Modeling
- Hyperparameter Optimization
- Model Evaluation
- Streamlit Application
- Dockerization
- Technical Documentation

### Optional (Advanced Scope)

- Database Integration
- Cloud Deployment
- Monitoring
- Automated Retraining

---

## Success Criteria

### Academic

- Functional regression model
- Proper evaluation metrics
- Complete documentation

### Portfolio

- Professional repository structure
- Business-oriented problem definition
- Deployable application
- Clear storytelling and insights

---

## Current Milestone

### Product & Dataset Analysis

Objectives:

- Review dataset structure
- Validate target variable
- Detect potential data leakage
- Define preprocessing strategy

---

## Next Planned Deliverables

1. Dataset Assessment
2. Data Dictionary
3. Initial EDA
4. Baseline Model
5. Streamlit MVP
6. Dockerization

## Working Agreements

### Documentation

- All documentation must be written in Markdown.
- All documentation must be maintained in VS Code.
- Documentation must be updated continuously throughout the project.

### Git Workflow

- New project phases require a dedicated feature branch.
- Commits should represent a complete logical unit of work.
- Commit messages must follow professional conventions.

### Project Management

- Significant decisions must be documented.
- Daily progress must be recorded.
- Major milestones must be registered in PROJECT_LOG.md.

### Development Workflow

Business Understanding → Dataset Assessment → EDA → Feature Engineering → Modeling → Application → Deployment.


### 2026-06-25

**Business Scope Update**

The project objective was redefined.

Instead of predicting campaign revenue using post-campaign performance metrics, the project will focus on forecasting campaign revenue before launch using only planning-time variables.

See JUN-25-business-problem-definition