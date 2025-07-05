# Stochastic-Models-for-Pricing-Futures-on-WTI-Crude-Oil
This repository contains the empirical study (made in python) of four stochastic models for WTI crude oil futures pricing. The goal is to estimate model parameters and evaluate predictive performance using real market data.

# 📈 Stochastic Models for Pricing WTI Futures

This project implements four **closed-form stochastic models** to price **futures contracts on WTI crude oil**, with both in-sample estimation and out-of-sample evaluation. The models are applied on real data, and include error diagnostics and maturity-stratified performance analysis.

> 🎓 This work is part of a Master's Thesis in Finance & Banking at the **University of Piraeus**, titled:  
> **"Stochastic Models for Pricing Futures on WTI Crude Oil"**

---

## 📚 Models Included

| Model | Description | SDE | Parameters |
|-------|-------------|-----|------------|
| 1. GBM (Gabillon) | Geometric Brownian Motion | dS = μ·Sₜ·dt + σ·Sₜ·dWₜ | δ |
| 2. OU (Schwartz) | Mean-reverting log process | dS = θ(μ − ln S)·dt + σ·S·dWₜ | θ, α, σ |
| 3. Modified Bessel | Square-root with nonlinear vol | dS = a·√S·dt + σ·S^(3/4)·dWₜ | a, σ |
| 4. Modified CIR | CIR drift with ¾ volatility | dS = (a·√S + b·S)·dt + σ·S^(3/4)·dWₜ | a, b, σ |

Each model provides an **analytical expression** for futures prices under no-arbitrage and deterministic interest rate assumptions.




## 📊 Dataset Summary

### 🔹 In-Sample: `DATASETORG.xlsx`
- **Spot prices**: WTI (daily), 08/12/2022–19/11/2024
- **Futures prices**: 12 CME contracts (Jan–Dec 2024), 245 daily observations per contract
- **Interest rates**: Daily 10-year US Treasury rates from FRED
- **TTM**: Calculated in trading days

### 🔹 Out-of-Sample: `DATASETORG_OFS.xlsx`
- **Spot prices**: 10 trading days (23/10/2024 to 19/08/2024)
- **Futures prices**: 12 ICE contracts (expiring Jan–Dec 2025)
- **Interest rates**: 10-day sample of 10Y Treasury rates
- **TTM**: Provided as 10 × 12 matrix

---



### ****** How to Run ******

At line 29, set model choise to your preffered model (1-4) or type "all" if you want to run all models at once.
Then, python main.py


### ****** Project Stracture ******
├── main.py
│   → Main script to run model estimation, evaluation, and plotting
├── preprocessing.py
│   → Functions to load, align, clean, and flatten futures, spot, and rate data
├── models.py
│   → Contains all four closed-form pricing models and parameter estimation logic
├── plotting.py
│   → Functions to visualize in-sample fits, daily RMSE, and model comparisons
├── metrics.py
│   → Functions for residual analysis grouped by maturity buckets
├── DATASETORG.xlsx
│   → In-sample dataset with 12 futures contracts, spot prices, and interest rates
├── DATASETORG_OFS.xlsx
│   → Out-of-sample dataset for evaluation on new market data





