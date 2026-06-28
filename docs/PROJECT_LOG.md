# PROJECT LOG

## Sprint 0 - Planning & Governance

### 2026-06-23

#### Repository Setup

- Repository created.
- Initial project structure defined.
- Documentation framework established.

#### Key Decisions

- Revenue selected as preliminary target variable.
- Docker included in project scope.
- Working agreements formally documented.

#### Next Milestone

Product & Dataset Analysis.

### Dataset Management

- Dataset storage policy established.
- Data files excluded from version control.
- Dataset documentation added.

### 2026-06-23

#### Dataset Assessment Completed

Completed the initial dataset audit and validation process.

Key findings:

- 30,000 observations.
- 35 variables.
- No missing values.
- No duplicate records.
- No constant features.
- Revenue identified as preliminary target variable.
- Strong correlation observed between revenue and conversions (0.76).
- Initial data leakage assessment completed.

#### Next Milestone

Formalize modeling assumptions and begin Exploratory Data Analysis (EDA).

## Sprint 0 - Planning & Governance

### 2026-06-23

#### Dataset Assessment Completed

- Dataset audited and validated.
- Revenue selected as preliminary target variable.
- No missing values detected.
- No duplicate records detected.
- No constant variables detected.
- Preliminary leakage analysis completed.

Status: Completed

### 2026-06-25

#### Business Scope Update

The project objective was redefined.

Instead of predicting campaign revenue using post-campaign performance metrics, the project will focus on forecasting campaign revenue before launch using only planning-time variables.

This change improves the business relevance of the project because the model will support campaign planning, budget allocation and decision-making before campaign execution.

#### Impact

- The target variable remains `revenue`.
- Post-campaign performance metrics will be treated as potential data leakage.
- Feature selection must be reviewed.
- The Dataset Assessment notebook must be updated.
- The EDA must focus on planning-time variables and their relationship with revenue.

#### Next Actions

- Update `01_dataset_assessment.ipynb`.
- Review the Data Leakage section.
- Create a formal decision record for the new business scope.
- Define the list of allowed planning-time features.