import pandas as pd
from pathlib import Path

# Locate the project folder and CSV file
project_dir = Path(__file__).resolve().parent.parent
csv_path = project_dir / "01_Data" / "ab_test_clean.csv"

# Load the dataset
df = pd.read_csv(csv_path)

# Validate dataset structure
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

# Check data types and missing values
print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nConversion values:")
print(df["converted"].value_counts(dropna=False))