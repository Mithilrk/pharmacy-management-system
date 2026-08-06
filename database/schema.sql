CREATE DATABASE IF NOT EXISTS pharmacy_db;
USE pharmacy_db;

-- 1. Table: Categories
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 2. Table: Medicines
CREATE TABLE IF NOT EXISTS medicines (
    medicine_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    category_id INT,
    batch_number VARCHAR(50) NOT NULL,
    expiry_date DATE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL
);

-- 3. Table: Users
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    email VARCHAR(100)
);

-- 4. Table: Customers
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100)
);

-- 5. Table: Sales
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    medicine_id INT,
    quantity_sold INT NOT NULL,
    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id) ON DELETE CASCADE
);

-- MySQL VIEW: Exposes public availability and filters out expired items
CREATE OR REPLACE VIEW view_available_medicines AS
SELECT 
    m.medicine_id,
    m.name AS medicine_name,
    c.name AS category_name,
    m.price,
    m.expiry_date,
    CASE 
        WHEN m.quantity > 10 THEN 'In Stock'
        WHEN m.quantity > 0 AND m.quantity <= 10 THEN 'Low Stock'
        ELSE 'Out of Stock'
    END AS availability_status
FROM medicines m
LEFT JOIN categories c ON m.category_id = c.category_id
WHERE m.expiry_date > CURDATE();