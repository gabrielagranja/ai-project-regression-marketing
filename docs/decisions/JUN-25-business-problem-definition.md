# ADR-001 — Business Problem Definition

**Date:** 2026-06-25

## Decision

The project objective has been redefined.

Instead of predicting campaign revenue using both planning variables and post-campaign performance metrics (e.g., clicks, conversions or impressions), the model will focus on **forecasting campaign revenue before launch** using only variables available during the campaign planning stage.

## Rationale

This approach better reflects a real business scenario.

Marketing and Growth teams need to estimate the expected revenue **before investing the advertising budget**, allowing them to compare different campaign configurations and make informed decisions.

## Impact

* Remove post-launch variables from the training features.
* Train the model using only planning-time variables.
* Align the future Streamlit application with a campaign forecasting use case.
* Increase the business value of the project while maintaining the same Machine Learning workflow.
