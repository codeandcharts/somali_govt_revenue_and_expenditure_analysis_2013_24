import pandas as pd

# 📂 Load World Bank Macroeconomic Indicators
wb_data = pd.read_csv(
    "./data/raw/API_SOM_DS2_en_csv_v2_3285.csv", skiprows=4
)  # Skipping metadata rows

# 🔍 Step 1: Select Relevant Macroeconomic Indicators
indicators = {
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",  # GDP Growth (%)
    "FP.CPI.TOTL.ZG": "inflation_rate",  # Inflation Rate (%)
    "GC.DOD.TOTL.GD.ZS": "government_debt_percent_gdp",  # Gov. Debt (% of GDP)
    "GC.TAX.TOTL.GD.ZS": "tax_revenue_percent_gdp",  # Tax Revenue (% of GDP)
    "DT.ODA.ODAT.GN.ZS": "foreign_aid_percent_gdp",  # Foreign Aid (% of GDP)
    "SL.UEM.TOTL.ZS": "unemployment_rate",  # Unemployment Rate (%)
}

# 🔍 Step 2: Filter for Somalia’s Relevant Indicators
wb_filtered = wb_data[wb_data["Indicator Code"].isin(indicators.keys())]

# 🔄 Step 3: Transform Data to Long Format (Year-wise)
wb_long = wb_filtered.melt(
    id_vars=["Indicator Name", "Indicator Code"], var_name="year", value_name="value"
)

# 🔹 Step 4: Ensure the Year Column is Numeric
wb_long = wb_long[pd.to_numeric(wb_long["year"], errors="coerce").notna()]
wb_long["year"] = wb_long["year"].astype(int)

# 🔍 Step 5: Map Indicator Codes to Clear Names
wb_long["Indicator Name"] = wb_long["Indicator Code"].map(indicators)

# 🔄 Step 6: Pivot to Get Indicators as Columns
wb_final = wb_long.pivot(
    index="year", columns="Indicator Name", values="value"
).reset_index()

# 📂 Load Somalia Government Finance Data
gov_finance = pd.read_csv("cleaned_somalia_budget.csv")

# 🔗 Step 7: Merge Government Finance Data with Macroeconomic Indicators
merged_df = pd.merge(gov_finance, wb_final, on="year", how="left")

# 📝 Step 8: Save the Cleaned & Merged Dataset
output_path = "./data/processed/Somalia_Govt_Finance_with_Macroeconomics.csv"
merged_df.to_csv(output_path, index=False)

print(f"✅ Merged dataset saved as: {output_path}")
