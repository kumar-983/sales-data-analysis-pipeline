import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("cleaned_data/clean_sales_data.xlsx")

print("Dataset Shape")
print(df.shape)

print("Columns")
print(df.columns)

print("Summary Statistics")
print(df.describe())

total_sales = df['Sales'].sum()
print("Total Sales:", total_sales)

total_profit = df['Profit'].sum()
print("Total Profit:", total_profit)

sales_category = df.groupby('Product Category')['Sales'].sum()

print("Sales by Category")
print(sales_category)

sales_category.plot(kind='bar')
plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.show()

profit_region = df.groupby('Region')['Profit'].sum()
print("Profit by Region")
print(profit_region)

profit_region.plot(kind='bar')
plt.title("Profit by Region")
plt.xlabel("Region")
plt.ylabel("Profit")
plt.show()

top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
print("Top 10 Products")
print(top_products)

top_products.plot(kind='bar')
plt.title("Top 10 Products by Sales")
plt.xlabel("Product")
plt.ylabel("Sales")
plt.show()

top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
print("Top 10 Customers")
print(top_customers)

top_customers.plot(kind='bar')
plt.title("Top 10 Customers by Sales")
plt.xlabel("Customer")
plt.ylabel("Sales")
plt.show()

monthly_sales = df.groupby('Order Month')['Sales'].sum()
print("Monthly Sales")
print(monthly_sales)

monthly_sales.plot(kind='line', marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

plt.scatter(df['Discount'], df['Profit'])
plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.show()