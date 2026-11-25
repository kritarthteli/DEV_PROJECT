# The Post-Pandemic AI & Tech Job Market Shift

## Data Exploration & Visualization Project Dashboard (2024–2026)

An interactive, production-grade exploratory data analysis (EDA) dashboard built with **Streamlit**, **Pandas**, and **Plotly Express**, exploring post-pandemic tech workforce dynamics, skill premiums, career tier divergence, and remote work compensation.

---

### 🚀 Quick Start

1. **Activate the Virtual Environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Launch the Streamlit Dashboard:**
   ```powershell
   streamlit run app.py
   ```
   Open your browser at `http://localhost:8501`.

---

### 📂 How to Swap In Your Real Kaggle CSV

When you obtain your final Kaggle dataset (e.g., `linkedin_tech_jobs.csv`):
1. Place the CSV file directly in this folder.
2. Open [`app.py`](file:///c:/Users/krish/OneDrive/Desktop/DEV_project/DEV_PROJECT/app.py) and navigate to `load_and_prepare_data()`:
   ```python
   # Set use_csv to True and pass your filename:
   raw_df, clean_df = load_and_prepare_data(use_csv=True, csv_path='my_dataset.csv')
   ```
3. The dashboard will automatically apply the Regex cleaning pipeline to your data and update all 4 tabs and visualizations in real time!

---

### 🌟 Dashboard Architecture

- **Global Sidebar**: Real-time multi-dimensional filtering across Tech Domains, Specific Job Titles, Career Experience Tiers, Remote/Hybrid Work Mandates, and Annual Salary ranges.
- **Tab 1: Executive Summary & KPIs**: High-level market metrics (`Total Jobs Analyzed`, `Average Tech Salary`, `Most Demanded Skill`) and strategic insights on labor dynamics, AI shifts, and compensation benchmarks.
- **Tab 2: Interactive Visualizations (Plotly Express)**:
  - *Chart 1 (Scatter Plot)*: 'The Skill Premium' (Demand Frequency vs. Average Salary with Quadrant Thresholds).
  - *Chart 2 (Violin Plot)*: 'The Experience Gap' (Salary distributions across Entry-level, Mid-level, Senior, and Executive tiers).
  - *Chart 3 (Grouped Bar Chart)*: 'The Remote Reality' (Remote vs. Hybrid vs. On-site compensation across tech domains).
  - *Chart 4 (Treemap)*: 'Domain Demand' (Hierarchical breakdown of job posting volume by domain and title).
- **Tab 3: Behind the Data (The Cleaning Pipeline)**: Side-by-side Raw vs. Cleaned dataframes, programmatic outlier handling via Z-score thresholding, and an **Interactive Live Regex Testing Playground**.
- **Tab 4: 'Know Your Worth' Salary Calculator**: Interactive compensation calculator with dynamic market salary estimation, 25th/75th percentile confidence bands, market percentile rank gauge, and targeted upskilling recommendations.