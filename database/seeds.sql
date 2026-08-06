USE pharmacy_db;

-- Clear existing data safely
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE sales;
TRUNCATE TABLE customers;
TRUNCATE TABLE users;
TRUNCATE TABLE medicines;
TRUNCATE TABLE categories;
SET FOREIGN_KEY_CHECKS = 1;

-- Seed Categories
INSERT INTO categories (category_id, name, description) VALUES
(1, 'Antibiotics', 'Medicines used to treat bacterial infections'),
(2, 'Painkillers', 'Analgesic drugs used to relieve pain'),
(3, 'Vitamins', 'Nutritional supplements and multivitamins'),
(4, 'Diabetes', 'Medicines to manage blood glucose levels'),
(5, 'Allergy', 'Antihistamines and allergy relief drugs');

-- Seed Medicines
INSERT INTO medicines (medicine_id, name, category_id, batch_number, expiry_date, price, quantity) VALUES
(1, 'Amoxicillin 500mg', 1, 'AMX1029', '2026-05-15', 12.50, 150),
(2, 'Paracetamol 500mg', 2, 'PCT5543', '2025-12-01', 3.00, 500),
(3, 'Vitamin C 1000mg', 3, 'VTC8872', '2026-01-20', 8.99, 8),
(4, 'Metformin 850mg', 4, 'MTF9911', '2025-11-30', 15.00, 45),
(5, 'Loratadine 10mg', 5, 'LRT0023', '2027-03-10', 6.50, 0);

-- Seed Users
INSERT INTO users (user_id, username, password_hash, role, email) VALUES
(1, 'admin_user', 'admin123', 'Admin', 'admin@pharmacy.com'),
(2, 'staff_jane', 'jane123', 'Staff', 'jane@pharmacy.com'),
(3, 'staff_john', 'john123', 'Staff', 'john@pharmacy.com'),
(4, 'manager_bob', 'bob123', 'Admin', 'bob@pharmacy.com'),
(5, 'staff_sarah', 'sarah123', 'Staff', 'sarah@pharmacy.com');

-- Seed Customers
INSERT INTO customers (customer_id, name, phone, email) VALUES
(1, 'Alice Smith', '555-0199', 'alice@email.com'),
(2, 'Bob Jones', '555-0144', 'bob.jones@email.com'),
(3, 'Charlie Brown', '555-0122', 'charlie@email.com'),
(4, 'Diana Prince', '555-0177', 'diana@email.com'),
(5, 'Evan Wright', '555-0155', 'evan@email.com');

-- Seed Sales
INSERT INTO sales (sale_id, customer_id, medicine_id, quantity_sold, total_price) VALUES
(1, 1, 1, 2, 25.00),
(2, 2, 2, 5, 15.00),
(3, 3, 3, 1, 8.99),
(4, 4, 4, 3, 45.00),
(5, 5, 1, 1, 12.50);