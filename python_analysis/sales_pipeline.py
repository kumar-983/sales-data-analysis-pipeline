import argparse
import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


NUMERIC_COLS = [
    'Sales',
    'Profit',
    'Discount',
    'Unit Price',
    'Shipping Cost',
    'Order Quantity'
]

CATEGORICAL_COLS = [
    'Order Priority',
    'Ship Mode',
    'Region',
    'Product Category',
    'Product Container'
]


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel("C:\\Users\\kundan kumar\\OneDrive\Desktop\\Sales_analysis_project\dataset\\sales_data.xlsx")
    df.columns = df.columns.str.strip()
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in NUMERIC_COLS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())

    for col in CATEGORICAL_COLS:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode().iloc[0])

    if 'Customer Name' in df.columns:
        df['Customer Name'] = df['Customer Name'].fillna('Unknown Customer')
    if 'Product Name' in df.columns:
        df['Product Name'] = df['Product Name'].fillna('Unknown Product')

    for date_col in ['Order Date', 'Ship Date']:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df[date_col] = df[date_col].ffill()

    if 'Order ID' in df.columns:
        df = df.dropna(subset=['Order ID'])

    df = df.drop_duplicates()

    if 'Order Date' in df.columns:
        df = df.dropna(subset=['Order Date'])
        df['Order Year'] = df['Order Date'].dt.year
        df['Order Month'] = df['Order Date'].dt.month
        df['Order Day'] = df['Order Date'].dt.day

    if 'Ship Date' in df.columns:
        df = df.dropna(subset=['Ship Date'])

    return df


def save_data(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_excel(path, index=False)


def summarise_data(df: pd.DataFrame) -> Dict[str, object]:
    return {
        'shape': df.shape,
        'columns': list(df.columns),
        'summary': df.describe(include='all', datetime_is_numeric=True).to_dict(),
        'total_sales': df['Sales'].sum() if 'Sales' in df.columns else None,
        'total_profit': df['Profit'].sum() if 'Profit' in df.columns else None,
    }


def run_eda(df: pd.DataFrame, output_dir: str, show_plots: bool = False) -> None:
    os.makedirs(output_dir, exist_ok=True)

    print('Dataset Shape')
    print(df.shape)
    print('\nColumns')
    print(df.columns.tolist())
    print('\nSummary Statistics')
    print(df.describe())

    if 'Sales' in df.columns:
        total_sales = df['Sales'].sum()
        print('\nTotal Sales:', total_sales)
    if 'Profit' in df.columns:
        total_profit = df['Profit'].sum()
        print('Total Profit:', total_profit)

    if 'Product Category' in df.columns and 'Sales' in df.columns:
        sales_category = df.groupby('Product Category')['Sales'].sum()
        print('\nSales by Category')
        print(sales_category)
        chart_path = os.path.join(output_dir, 'sales_by_category.png')
        sales_category.plot(kind='bar')
        plt.title('Sales by Product Category')
        plt.xlabel('Category')
        plt.ylabel('Sales')
        plt.tight_layout()
        plt.savefig(chart_path)
        if show_plots:
            plt.show()
        plt.clf()

    if 'Region' in df.columns and 'Profit' in df.columns:
        profit_region = df.groupby('Region')['Profit'].sum()
        print('\nProfit by Region')
        print(profit_region)
        chart_path = os.path.join(output_dir, 'profit_by_region.png')
        profit_region.plot(kind='bar')
        plt.title('Profit by Region')
        plt.xlabel('Region')
        plt.ylabel('Profit')
        plt.tight_layout()
        plt.savefig(chart_path)
        if show_plots:
            plt.show()
        plt.clf()

    if 'Product Name' in df.columns and 'Sales' in df.columns:
        top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
        print('\nTop 10 Products')
        print(top_products)
        chart_path = os.path.join(output_dir, 'top_products.png')
        top_products.plot(kind='bar')
        plt.title('Top 10 Products by Sales')
        plt.xlabel('Product')
        plt.ylabel('Sales')
        plt.tight_layout()
        plt.savefig(chart_path)
        if show_plots:
            plt.show()
        plt.clf()

    if 'Customer Name' in df.columns and 'Sales' in df.columns:
        top_customers = df.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10)
        print('\nTop 10 Customers')
        print(top_customers)
        chart_path = os.path.join(output_dir, 'top_customers.png')
        top_customers.plot(kind='bar')
        plt.title('Top 10 Customers by Sales')
        plt.xlabel('Customer')
        plt.ylabel('Sales')
        plt.tight_layout()
        plt.savefig(chart_path)
        if show_plots:
            plt.show()
        plt.clf()

    if 'Order Month' in df.columns and 'Sales' in df.columns:
        monthly_sales = df.groupby('Order Month')['Sales'].sum()
        print('\nMonthly Sales')
        print(monthly_sales)
        chart_path = os.path.join(output_dir, 'monthly_sales.png')
        monthly_sales.plot(kind='line', marker='o')
        plt.title('Monthly Sales Trend')
        plt.xlabel('Month')
        plt.ylabel('Sales')
        plt.tight_layout()
        plt.savefig(chart_path)
        if show_plots:
            plt.show()
        plt.clf()

    if 'Discount' in df.columns and 'Profit' in df.columns:
        chart_path = os.path.join(output_dir, 'discount_vs_profit.png')
        plt.scatter(df['Discount'], df['Profit'])
        plt.title('Discount vs Profit')
        plt.xlabel('Discount')
        plt.ylabel('Profit')
        plt.tight_layout()
        plt.savefig(chart_path)
        if show_plots:
            plt.show()
        plt.clf()

    print(f'EDA charts saved to: {output_dir}')


def run_pipeline(
    raw_path: str,
    clean_path: str,
    eda_dir: str,
    show_plots: bool = False,
    skip_clean: bool = False,
    skip_eda: bool = False,
) -> None:
    df = None
    if not skip_clean:
        print(f'Loading raw data from {raw_path}')
        df = load_data(raw_path)
        print('Cleaning raw data...')
        df = clean_data(df)
        save_data(df, clean_path)
        print(f'Clean dataset saved to {clean_path}')
    else:
        print(f'Skipping cleaning. Loading cleaned data from {clean_path}')
        df = pd.read_excel(clean_path)

    if not skip_eda:
        print('Running exploratory data analysis...')
        run_eda(df, eda_dir, show_plots=show_plots)
    else:
        print('EDA step skipped.')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Sales data pipeline')
    parser.add_argument('--raw-input', default='dataset/sales_data.xlsx', help='Raw sales dataset input path')
    parser.add_argument('--clean-output', default='cleaned_data/clean_sales_data.xlsx', help='Cleaned dataset output path')
    parser.add_argument('--eda-output-dir', default='eda_outputs', help='Directory to save EDA charts')
    parser.add_argument('--show-plots', action='store_true', help='Show plots interactively')
    parser.add_argument('--skip-clean', action='store_true', help='Skip the cleaning step')
    parser.add_argument('--skip-eda', action='store_true', help='Skip the EDA step')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_pipeline(
        raw_path=args.raw_input,
        clean_path=args.clean_output,
        eda_dir=args.eda_output_dir,
        show_plots=args.show_plots,
        skip_clean=args.skip_clean,
        skip_eda=args.skip_eda,
    )
