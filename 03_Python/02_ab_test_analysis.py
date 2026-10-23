import pandas as pd
from pathlib import Path

# Load validated dataset
project_dir = Path(__file__).resolve().parent.parent
csv_path = project_dir / "01_Data" / "ab_test_clean.csv"

df = pd.read_csv(csv_path)

# Calculate A/B testing KPIs
summary = (
    df.groupby("test_group")
    .agg(
        total_users=("user_id", "count"),
        conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")
    )
)

summary["conversion_rate_pct"] = (
    summary["conversion_rate"] * 100
)

print("\nA/B TESTING SUMMARY")
print(summary.to_string())

# Calculate treatment vs control lift
ad_rate = summary.loc["ad", "conversion_rate"]
psa_rate = summary.loc["psa", "conversion_rate"]

absolute_lift_pp = (ad_rate - psa_rate) * 100
relative_lift_pct = ((ad_rate / psa_rate) - 1) * 100

print("\nEXPERIMENT RESULTS")
print(f"Absolute lift: {absolute_lift_pp:.4f} percentage points")
print(f"Relative lift: {relative_lift_pct:.2f}%")

from statsmodels.stats.proportion import proportions_ztest

# Two-proportion Z-test
successes = [
    summary.loc["ad", "conversions"],
    summary.loc["psa", "conversions"]
]

sample_sizes = [
    summary.loc["ad", "total_users"],
    summary.loc["psa", "total_users"]
]

z_stat, p_value = proportions_ztest(
    count=successes,
    nobs=sample_sizes,
    alternative="two-sided"
)

alpha = 0.05

print("\nSTATISTICAL SIGNIFICANCE TEST")
print(f"Z-statistic: {z_stat:.4f}")
print(f"P-value: {p_value:.10f}")
print(f"Significance level: {alpha}")

if p_value < alpha:
    print("Result: Statistically significant difference")
    print("Decision: Reject the null hypothesis")
else:
    print("Result: No statistically significant difference detected")
    print("Decision: Fail to reject the null hypothesis")

from statsmodels.stats.proportion import confint_proportions_2indep

# 95% confidence interval for the difference in conversion rates
ci_low, ci_high = confint_proportions_2indep(
    count1=int(summary.loc["ad", "conversions"]),
    nobs1=int(summary.loc["ad", "total_users"]),
    count2=int(summary.loc["psa", "conversions"]),
    nobs2=int(summary.loc["psa", "total_users"]),
    compare="diff",
    method="newcomb",
    alpha=0.05
)

print("\n95% CONFIDENCE INTERVAL")
print(f"Lower bound: {ci_low * 100:.4f} percentage points")
print(f"Upper bound: {ci_high * 100:.4f} percentage points")

# Analyze experiment group allocation
total_users = summary["total_users"].sum()

summary["allocation_pct"] = (
    summary["total_users"] / total_users * 100
)

print("\nEXPERIMENT GROUP ALLOCATION")

for group, row in summary.iterrows():
    print(
        f"{group.upper()}: "
        f"{int(row['total_users']):,} users "
        f"({row['allocation_pct']:.2f}%)"
    )

# Compare ad exposure between experiment groups
exposure_summary = (
    df.groupby("test_group")["total_ads"]
    .agg(["mean", "median", "std", "min", "max"])
)

print("\nAD EXPOSURE BY TEST GROUP")
print(exposure_summary.round(2).to_string())

# Analyze conversion rates by ad exposure

bins = [0, 5, 10, 20, 50, float("inf")]
labels = ["1-5", "6-10", "11-20", "21-50", "51+"]

df["exposure_group"] = pd.cut(
    df["total_ads"],
    bins=bins,
    labels=labels
)

exposure_conversion = (
    df.groupby(
        ["test_group", "exposure_group"],
        observed=True
    )
    .agg(
        users=("user_id", "count"),
        conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")
    )
)

exposure_conversion["conversion_rate_pct"] = (
    exposure_conversion["conversion_rate"] * 100
)

print("\nCONVERSION RATE BY AD EXPOSURE")
print(
    exposure_conversion[
        ["users", "conversions", "conversion_rate_pct"]
    ].round(4).to_string()
)

# Analyze conversion rates by day of week

day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

daily_conversion = (
    df.groupby(["most_ads_day", "test_group"])
    .agg(
        users=("user_id", "count"),
        conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")
    )
    .reset_index()
)

daily_conversion["conversion_rate_pct"] = (
    daily_conversion["conversion_rate"] * 100
)

daily_conversion["most_ads_day"] = pd.Categorical(
    daily_conversion["most_ads_day"],
    categories=day_order,
    ordered=True
)

daily_conversion = daily_conversion.sort_values(
    ["most_ads_day", "test_group"]
)

print("\nCONVERSION RATE BY DAY OF WEEK")
print(
    daily_conversion[
        ["most_ads_day", "test_group", "users",
         "conversions", "conversion_rate_pct"]
    ].round(4).to_string(index=False)
)

# Analyze conversion rates by hour of day

hourly_conversion = (
    df.groupby(["most_ads_hour", "test_group"])
    .agg(
        users=("user_id", "count"),
        conversions=("converted", "sum"),
        conversion_rate=("converted", "mean")
    )
    .reset_index()
)

hourly_conversion["conversion_rate_pct"] = (
    hourly_conversion["conversion_rate"] * 100
)

hourly_conversion = hourly_conversion.sort_values(
    ["most_ads_hour", "test_group"]
)

print("\nCONVERSION RATE BY HOUR OF DAY")
print(
    hourly_conversion[
        ["most_ads_hour", "test_group", "users",
         "conversions", "conversion_rate_pct"]
    ].round(4).to_string(index=False)
)

# Export A/B testing summary for Power BI

output_dir = project_dir / "04_PowerBI"
output_dir.mkdir(parents=True, exist_ok=True)

summary_export = summary.reset_index()

summary_export.to_csv(
    output_dir / "ab_test_summary.csv",
    index=False
)

print("\nPOWER BI EXPORT")
print("A/B testing summary exported successfully.")

# Export detailed analysis tables for Power BI

exposure_conversion.reset_index().to_csv(
    output_dir / "ab_test_exposure.csv",
    index=False
)

daily_conversion.to_csv(
    output_dir / "ab_test_daily.csv",
    index=False
)

hourly_conversion.to_csv(
    output_dir / "ab_test_hourly.csv",
    index=False
)

print("\nDETAILED POWER BI EXPORTS")
print("Exposure, daily and hourly analysis exported successfully.")