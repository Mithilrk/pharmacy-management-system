import os
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from dotenv import load_dotenv

# Load environmental variables from .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'fallback_secret_key')

# Database connection configuration
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'pharmacy_db')
    )

# ==========================================
# 1. PUBLIC PORTAL ROUTES
# ==========================================

@app.route('/')
def home():
    """Shop landing page showcasing contact and location details."""
    shop_info = {
        "name": "Community Care Pharmacy",
        "address": "123 Health Street, Medical District, Cityville",
        "phone": "+1 (555) 019-9999",
        "hours": "Mon-Sat: 8:00 AM - 10:00 PM, Sun: 10:00 AM - 6:00 PM",
        "gmaps_link": "https://maps.google.com"
    }
    return render_template('public_home.html', shop=shop_info)

@app.route('/check-availability')
def check_availability():
    """
    Public search module using SELECT on the MySQL VIEW.
    Demonstrates VIEW execution.
    """
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if search_query:
        # Querying from the View
        query = """
            SELECT * FROM view_available_medicines 
            WHERE medicine_name LIKE %s OR category_name LIKE %s
        """
        cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
    else:
        query = "SELECT * FROM view_available_medicines"
        cursor.execute(query)
        
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('public_availability.html', medicines=results, search_query=search_query)

# ==========================================
# 2. MEDICINE MANAGEMENT (Staff Backend)
# ==========================================

@app.route('/admin/medicines')
def list_medicines():
    """Demonstrates SELECT with JOIN to retrieve inventory details."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT m.*, c.name AS category_name 
        FROM medicines m 
        LEFT JOIN categories c ON m.category_id = c.category_id
    """
    cursor.execute(query)
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('medicines_list.html', medicines=medicines)

@app.route('/admin/medicines/add', methods=['GET', 'POST'])
def add_medicine():
    """Demonstrates INSERT operation."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        batch_number = request.form['batch_number']
        expiry_date = request.form['expiry_date']
        price = request.form['price']
        quantity = request.form['quantity']

        insert_query = """
            INSERT INTO medicines (name, category_id, batch_number, expiry_date, price, quantity) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (name, category_id, batch_number, expiry_date, price, quantity))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Medicine added successfully.")
        return redirect(url_for('list_medicines'))
    
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('medicine_form.html', categories=categories, action="Add", medicine=None)

@app.route('/admin/medicines/edit/<int:medicine_id>', methods=['GET', 'POST'])
def edit_medicine(medicine_id):
    """Demonstrates UPDATE operation."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        batch_number = request.form['batch_number']
        expiry_date = request.form['expiry_date']
        price = request.form['price']
        quantity = request.form['quantity']

        update_query = """
            UPDATE medicines 
            SET name = %s, category_id = %s, batch_number = %s, expiry_date = %s, price = %s, quantity = %s 
            WHERE medicine_id = %s
        """
        cursor.execute(update_query, (name, category_id, batch_number, expiry_date, price, quantity, medicine_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Medicine details updated.")
        return redirect(url_for('list_medicines'))

    cursor.execute("SELECT * FROM medicines WHERE medicine_id = %s", (medicine_id,))
    medicine = cursor.fetchone()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('medicine_form.html', medicine=medicine, categories=categories, action="Edit")

@app.route('/admin/medicines/delete/<int:medicine_id>', methods=['POST'])
def delete_medicine(medicine_id):
    """Demonstrates DELETE operation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM medicines WHERE medicine_id = %s", (medicine_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Medicine deleted from inventory.")
    return redirect(url_for('list_medicines'))

# ==========================================
# 3. CUSTOMER HISTORY MANAGEMENT
# ==========================================

@app.route('/admin/customers')
def list_customers():
    """Retrieves customer lists."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('customers_list.html', customers=customers)

@app.route('/admin/customers/<int:customer_id>/history')
def customer_history(customer_id):
    """Retrieves detailed customer purchase history using relationships."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
    customer = cursor.fetchone()

    history_query = """
        SELECT s.sale_id, m.name AS medicine_name, s.quantity_sold, s.total_price, s.sale_date 
        FROM sales s
        JOIN medicines m ON s.medicine_id = m.medicine_id
        WHERE s.customer_id = %s
        ORDER BY s.sale_date DESC
    """
    cursor.execute(history_query, (customer_id,))
    history = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template('customer_history.html', customer=customer, history=history)

if __name__ == '__main__':
    app.run(debug=True)