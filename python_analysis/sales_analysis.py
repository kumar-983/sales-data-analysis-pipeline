import pandas as pd
import numpy as np
import os

df = pd.read_excel("dataset/sales_data.xlsx")

print("First 5 Rows")
print(df.head())

print("Dataset Shape")
print(df.shape)

df.columns = df.columns.str.strip()

print("Dataset Info")
print(df.info())

print("Missing Values")
print(df.isnull().sum())

numeric_cols = [
    'Sales',
    'Profit',
    'Discount',
    'Unit Price',
    'Shipping Cost',
    'Order Quantity'
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

for col in numeric_cols:
    df[col] = df[col].fillna(df[col].median())

categorical_cols = [
    'Order Priority',
    'Ship Mode',
    'Region',
    'Product Category',
    'Product Container'
]

for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

df['Customer Name'] = df['Customer Name'].fillna("Unknown Customer")
df['Product Name'] = df['Product Name'].fillna("Unknown Product")

df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], errors='coerce')

df['Order Date'] = df['Order Date'].ffill()
df['Ship Date'] = df['Ship Date'].ffill()

df = df.dropna(subset=['Order ID'])
df = df.drop_duplicates()

df['Order Year'] = df['Order Date'].dt.year
df['Order Month'] = df['Order Date'].dt.month
df['Order Day'] = df['Order Date'].dt.day

df = df.dropna(subset=['Order Date','Ship Date'])

print("Missing Values After Cleaning")
print(df.isnull().sum())

os.makedirs("cleaned_data", exist_ok=True)
df.to_excel("cleaned_data/clean_sales_data.xlsx", index=False)

print("Clean dataset saved successfully!")