# Research‑Seminar  
_Avellaneda–Stoikov Market‑Making Simulator & Data Playground_

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)  
![Status](https://img.shields.io/badge/status-experimental-orange)

## ✨ What is this project?

This repository is a **minimal, self‑contained implementation of the Avellaneda–Stoikov (2008) optimal market‑making model**.  
It lets you:

1. **Run synthetic experiments** that compare the *inventory‑aware* optimal quoting strategy with a *naïve symmetric* strategy (`simulation.py`).  
2. **Replay the strategy on real data** (minute‑level Apple order‑book snippets) to see how it behaves in practice (`data.py`).  
3. Study a **step‑by‑step, pedagogy‑first script** (`test.py`) that follows the equations in the original paper nearly line‑for‑line.

Outputs are saved as PDFs (_P&L histograms, price paths, equity curves_) in the repo root.

> **Paper reference**: M. Avellaneda & S. Stoikov,  
> “High‑frequency trading in a limit order book”, *Quantitative Finance* **8**(3), 2008.  

Source files & data discovered in commit `d180ee7`&#8203;:contentReference[oaicite:0]{index=0}.  
Core implementation lives in `hftmaster/simulation.py`&#8203;:contentReference[oaicite:1]{index=1} with data‑driven variant in `hftmaster/data.py`&#8203;:contentReference[oaicite:2]{index=2}.

---

## 🗂️ Repository layout

```text
hftmaster/
├── appl.csv           # Sample mid‑price time series (Apple, Jan‑Feb 2021)
├── data.py            # Strategy on real data
├── simulation.py      # Synthetic GBM price, two strategies
├── test.py            # Verbose educational loop version
├── *.pdf              # Auto‑generated plots (saved on run)
└── .idea/             # JetBrains project files (can be ignored)


# 🚀 Quick start
1. Clone & enter the repo
    ```bash
    git clone https://github.com/eliray01/Research-Seminar.git
    cd Research-Seminar/hftmaster
    ```
2. Create environment & install deps
    ```bash
    python -m venv .venv
    source .venv/bin/activate       # Windows: .venv\Scripts\activate
    pip install numpy pandas matplotlib plotly
    ```

3. Run the synthetic simulation
    ```bash
    python simulation.py
    ```

Generates:

pnl.pdf – Histogram of P&L for both strategies

prices.pdf – Mid‑price vs optimal bid/ask quotes

4. Run on historical data
    ```bash
    python data.py                # uses appl.csv by default
    ```

