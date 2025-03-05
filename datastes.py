import os
import pandas as pd


def dedup_columns(columns):
    """Create unique column names by appending a counter to duplicates."""
    seen = {}
    new_cols = []
    for col in columns:
        if col in seen:
            seen[col] += 1
            new_cols.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 0
            new_cols.append(col)
    return new_cols


# File paths for all years
files = {
    "2013": "data/raw/2013_dbSomaliaFgsRevExp - Sheet1.csv",
    "2014": "data/raw/2014_dbSomaliaFgsRevExp - Sheet1.csv",
    "2015": "data/raw/2015_dbSomaliaFgsRevExp - Sheet1.csv",
    "2016": "data/raw/2016_dbSomaliaFgsRevExp - Sheet1.csv",
    "2017": "data/raw/2017_dbSomaliaFgsRevExp.xlsx",
    "2018": "data/raw/2018_dbSomaliaFgsRevExp.xlsx",
    "2019": "data/raw/2019_dbSomaliaFgsRevExp.xlsx",
    "2020": "data/raw/2020_dbSomaliaFgsRevExp.xlsx",
    "2021": "data/raw/2021_dbSomaliaFgsRevExp.xlsx",
    "2022": "data/raw/2022_dbSomaliaFgsRevExp.xlsx",
    "2023": "data/raw/2023_dbSomaliaFgsRevExp.xlsx",
    "2024": "data/raw/2024_dbSomaliaFgsRevExp.xlsx",
}

# Initialize a list to store dataframes
dfs = []

for year, path in files.items():
    try:
        # Load CSV or Excel file
        if path.endswith(".csv"):
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)

        # Add 'Year' column
        df["Year"] = int(year)

        # Convert column names to lowercase and strip spaces
        df.columns = df.columns.str.strip().str.lower()

        # Deduplicate column names if necessary
        if not df.columns.is_unique:
            df.columns = dedup_columns(df.columns)

        # Append dataframe to list
        dfs.append(df)

    except Exception as e:
        print(f"Error processing file {path}: {e}")

# Merge all dataframes
if dfs:
    merged_df = pd.concat(dfs, ignore_index=True)

    # Identify numeric columns automatically
    numeric_cols = merged_df.select_dtypes(include=["number"]).columns.tolist()

    # Fill missing numeric data with 0 for consistency
    merged_df[numeric_cols] = merged_df[numeric_cols].fillna(0)

    # Create the output folder if it doesn't exist
    output_folder = "data/processed/"
    os.makedirs(output_folder, exist_ok=True)

    # Save the cleaned and merged dataset
    output_path = os.path.join(
        output_folder, "Somalia_Government_Finances_2013_2024.csv"
    )
    merged_df.to_csv(output_path, index=False)

    print(f"✅ Merged and cleaned dataset saved as: {output_path}")
else:
    print("❌ No data was processed. Please check the file paths and formats.")
