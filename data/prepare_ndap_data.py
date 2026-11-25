import os
import glob
import re
import numpy as np
import pandas as pd

# Anchor paths to DEV_PROJECT root regardless of where the script is invoked
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_root, "data")
os.makedirs(data_dir, exist_ok=True)

def extract_year(val):
    match = re.search(r"(\d{4})", str(val))
    return int(match.group(1)) if match else None

# Search recursively inside DEV_PROJECT and one level up
csv_files = glob.glob(os.path.join(project_root, "**", "*.csv"), recursive=True)
csv_files += glob.glob(os.path.join(os.path.dirname(project_root), "*.csv"))

df_it_clean = df_ex_clean = df_edu_clean = df_iti_clean = None
df_cat_clean = df_min_clean = df_pwd_clean = None

for path in csv_files:
    try:
        df = pd.read_csv(path)
    except Exception:
        continue
    cols = set(df.columns)

    if "Net Addition (UOM:Number), Scaling Factor:1" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_it_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "IT_Total_Employment": df["Employment (UOM:Number), Scaling Factor:1000000"] * 1_000_000,
            "IT_Net_Hiring_Addition": df["Net Addition (UOM:Number), Scaling Factor:1"]
        })
        print(f"Matched IT Sector file: {os.path.basename(path)}")

    elif "Employment Exchanges/Ueigbs (UOM:Number), Scaling Factor:1000" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_ex_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "Total_Registrations": df["Number Of Registration In The Employment Exchange Statistics  (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Total_Placements": df["Number Of Placement In The Employment Exchange Statistics (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Vacancies_Notified": df["Number Of Vacancies Notified In The Employment Exchange Statistics  (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Total_Live_Register": df["Number Of Live Register In The Employment Exchange Statistics  (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Placement_to_Vacancy_Pct": df["Percentage Of Placement To Vacancies Notified In The Employment Exchange Statistics (UOM:%(Percentage)), Scaling Factor:1"]
        })
        print(f"Matched Employment Exchange file: {os.path.basename(path)}")

    elif "Registration Of Educated Jobseekers In The Employment Exchange Statistics (UOM:Number), Scaling Factor:1000" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_edu_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "Educated_Registrations": df["Registration Of Educated Jobseekers In The Employment Exchange Statistics (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Educated_Placements": df["Placement Of Educated Jobseekers In The Employment Exchange Statistics (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Educated_Live_Register": df["Live Register Of Educated Jobseekers In The Employment Exchange Statistics (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Educated_Share_of_Register_Pct": df["Live Register To Total Live Register In The Employment Exchange Statistics (UOM:%(Percentage)), Scaling Factor:1"]
        })
        print(f"Matched Educated Job-Seekers file: {os.path.basename(path)}")

    elif "Registration Count Of Ex-Iti  (UOM:Number), Scaling Factor:1" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_iti_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "Ex_ITI_Placements": df["Placement Count Of Ex-Iti Trainees (UOM:Number), Scaling Factor:1"],
            "Apprentice_Placements": df["Placement Count Of Full-Term Apprentices.2  (UOM:Number), Scaling Factor:1"]
        })
        print(f"Matched ITI/Apprentices file: {os.path.basename(path)}")

    elif "Category Of Number Of Job-Seekers On Live Register Of Employment Exchanges (UOM:Number), Scaling Factor:100000" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_cat_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "Group_Type": "Social & Gender Category",
            "Demographic_Group": df["Category"],
            "Live_Register_Count": df["Category Of Number Of Job-Seekers On Live Register Of Employment Exchanges (UOM:Number), Scaling Factor:100000"] * 100_000,
            "Placements_Count": np.nan,
            "Share_of_Total_Register_Pct": df["Percentage Of Job-Seekers On Live Register Of Employment Exchanges (UOM:%(Percentage)), Scaling Factor:1"]
        })
        print(f"Matched Social/Gender Category file: {os.path.basename(path)}")

    elif "Minority Communities" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_min_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "Group_Type": "Minority Community",
            "Demographic_Group": df["Minority Communities"],
            "Live_Register_Count": df["Live Register  (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Placements_Count": df["Placement  (UOM:Number), Scaling Factor:1000"].fillna(0) * 1_000,
            "Share_of_Total_Register_Pct": np.nan
        })
        print(f"Matched Minority Communities file: {os.path.basename(path)}")

    elif "Category Of Differently Abled Jobseekers" in cols:
        df["Year_Num"] = df["Year"].apply(extract_year)
        df_pwd_clean = pd.DataFrame({
            "Year_Num": df["Year_Num"],
            "Group_Type": "Differently Abled Exchange Channel",
            "Demographic_Group": df["Category Of Differently Abled Jobseekers"],
            "Live_Register_Count": df["Live Register (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Placements_Count": df["Placement (UOM:Number), Scaling Factor:1000"] * 1_000,
            "Share_of_Total_Register_Pct": np.nan
        })
        print(f"Matched Differently Abled file: {os.path.basename(path)}")

required = {
    "IT Sector": df_it_clean,
    "Employment Exchange": df_ex_clean,
    "Educated Job-Seekers": df_edu_clean,
    "ITI/Apprentices": df_iti_clean,
    "Category": df_cat_clean,
    "Minority": df_min_clean,
    "Differently Abled": df_pwd_clean,
}
missing = [k for k, v in required.items() if v is None]
if missing:
    raise RuntimeError(f"Missing datasets: {missing}. CSVs scanned: {csv_files}")

master_macro = (
    df_ex_clean
    .merge(df_edu_clean, on="Year_Num", how="outer")
    .merge(df_iti_clean, on="Year_Num", how="outer")
    .merge(df_it_clean, on="Year_Num", how="outer")
    .sort_values("Year_Num")
    .reset_index(drop=True)
)
master_macro.to_csv(os.path.join(data_dir, "ndap_labour_macro.csv"), index=False)

master_demo = (
    pd.concat([df_cat_clean, df_min_clean, df_pwd_clean], ignore_index=True)
    .sort_values(["Year_Num", "Group_Type", "Demographic_Group"])
    .reset_index(drop=True)
)
master_demo.to_csv(os.path.join(data_dir, "ndap_demographics.csv"), index=False)

print("SUCCESS: Created data/ndap_labour_macro.csv and data/ndap_demographics.csv")
