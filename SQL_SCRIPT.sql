use sales_analysis;
CREATE TABLE sales_data (
    order_id INT,
    order_date DATE,
    order_priority VARCHAR(20),
    order_quantity INT,
    sales FLOAT,
    discount FLOAT,
    ship_mode VARCHAR(50),
    profit FLOAT,
    unit_price FLOAT,
    shipping_cost FLOAT,
    customer_name VARCHAR(100),
    province VARCHAR(50),
    region VARCHAR(50),
    customer_segment VARCHAR(50),
    product_category VARCHAR(50),
    product_sub_category VARCHAR(50),
    product_name VARCHAR(255),
    product_container VARCHAR(50)
);

select * from sales_data;

-- TOTAL SALES AND PROFIT
SELECT 
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM sales_data;

-- SALES BY CATEGORY
SELECT 
    Product_Category,
    SUM(sales) AS total_sales
FROM sales_data
GROUP BY Product_Category
ORDER BY total_sales DESC;

-- TOP 10 CUSTOMERS
SELECT 
    customer_name,
    SUM(sales) AS total_sales
FROM sales_data
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;

-- PROFIT BY REGION
SELECT 
    region,
    SUM(profit) AS total_profit
FROM sales_data
GROUP BY region;

-- LOSS MAKING PRODUCTS
SELECT 
    product_name,
    SUM(profit) AS total_profit
FROM sales_data
GROUP BY product_name
HAVING total_profit < 0
ORDER BY total_profit;

-- MONTHLY SALES TREND
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    SUM(sales) AS total_sales
FROM sales_data
GROUP BY year, month
ORDER BY year, month;

-- BEST SHIPPING MODE
SELECT 
    ship_mode,
    SUM(profit) AS total_profit
FROM sales_data
GROUP BY ship_mode
ORDER BY total_profit DESC;