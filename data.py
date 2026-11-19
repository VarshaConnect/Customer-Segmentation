
import pandas as pd
import numpy as np
from pathlib import Path

# Make results reproducible
np.random.seed(42)

# Total number of customers
n = 1000

# Customer behavior groups used to create realistic sample data
customer_types = [
    "Budget Frequent",
    "Premium High Value",
    "Occasional",
    "Young Trend Driven",
    "Family Practical"
]

probabilities = [0.25, 0.20, 0.20, 0.20, 0.15]

customer_type = np.random.choice(
    customer_types,
    size=n,
    p=probabilities
)

# Generate customer demographics
age = []
income = []
frequency = []
order_value = []

for group in customer_type:

    if group == "Budget Frequent":
        age.append(np.random.randint(20, 45))
        income.append(np.random.normal(350000, 60000))
        frequency.append(np.random.randint(12, 25))
        order_value.append(np.random.normal(1200, 250))

    elif group == "Premium High Value":
        age.append(np.random.randint(30, 60))
        income.append(np.random.normal(1000000, 180000))
        frequency.append(np.random.randint(8, 18))
        order_value.append(np.random.normal(6000, 1000))

    elif group == "Occasional":
        age.append(np.random.randint(25, 65))
        income.append(np.random.normal(500000, 100000))
        frequency.append(np.random.randint(1, 7))
        order_value.append(np.random.normal(2500, 500))

    elif group == "Young Trend Driven":
        age.append(np.random.randint(18, 30))
        income.append(np.random.normal(300000, 70000))
        frequency.append(np.random.randint(8, 20))
        order_value.append(np.random.normal(1800, 400))

    else:
        age.append(np.random.randint(30, 55))
        income.append(np.random.normal(700000, 120000))
        frequency.append(np.random.randint(5, 13))
        order_value.append(np.random.normal(3500, 600))

# Create customer dataset
df = pd.DataFrame({
    "Customer ID": [f"CUST{i:04d}" for i in range(1, n + 1)],
    "Gender": np.random.choice(
        ["Male", "Female"], size=n
    ),
    "Age": age,
    "Annual Income": income,
    "Purchase Frequency": frequency,
    "Average Order Value": order_value
})

# Clean numeric values
df["Annual Income"] = df["Annual Income"].clip(lower=100000).round(0)
df["Average Order Value"] = (
    df["Average Order Value"].clip(lower=200).round(2)
)

# Calculate total customer spending
df["Total Spending"] = (
    df["Purchase Frequency"] * df["Average Order Value"]
).round(2)

# Generate additional customer behavior information
df["Days Since Last Purchase"] = np.random.randint(1, 181, size=n)

categories = [
    "Electronics",
    "Fashion",
    "Beauty",
    "Home & Living",
    "Grocery",
    "Sports"
]

df["Preferred Category"] = np.random.choice(
    categories, size=n
)

df["Shopping Channel"] = np.random.choice(
    ["Online", "In-Store", "Both"],
    size=n,
    p=[0.50, 0.25, 0.25]
)

# Save dataset in the same project folder
file_path = Path(__file__).resolve().parent / "customer_data.csv"
df.to_csv(file_path, index=False)

# Display results
print("Customer dataset generated successfully!")
print("Total Customers:", len(df))
print("\nDataset Preview:")
print(df.head())

print("\nDataset Information:")
print(df.info())

print("\nDataset saved at:")
print(file_path)
