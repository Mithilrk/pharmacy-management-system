# Pharmacy Management System

A small pharmacy management project with a Flask/MySQL application and a separate legacy PHP/MySQL implementation. The Flask app is the main project at the repository root. The PHP app and its macOS launcher are kept in [`legacy-php/`](legacy-php/README.md).

## Features

The Flask application includes:

- A public landing page and medicine availability search.
- Medicine inventory listing, creation, editing, and deletion.
- Customer listing and purchase history pages.
- A MySQL view that lists medicines that have not expired.

## Requirements

- Python 3.8 or later
- MySQL 8 or a compatible MySQL server
- PHP with the `mysqli` extension is only needed for the legacy application

## Set up and run the Flask app

Run these commands from the repository root.

1. Create and activate a virtual environment, then install Python dependencies:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create the database and tables:

   ```sh
   mysql -u root -p < database/schema.sql
   ```

   The schema creates and selects a database named `pharmacy_db`.

3. Create a local environment file and update it with your MySQL settings and a unique Flask secret:

   ```sh
   cp .env.example .env
   ```

   Set `DB_HOST`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME` in `.env`. Replace the example `FLASK_SECRET` with a long random value. Keep `.env` private; it is excluded from Git.

4. Start the development server:

   ```sh
   python app.py
   ```

5. Open <http://127.0.0.1:5000>.

## Optional demo data

To load the example categories, medicines, users, customers, and sales:

```sh
mysql -u root -p < database/seeds.sql
```

**This script truncates the existing tables before inserting demo rows.** Use it only with a disposable development database. The sample user passwords are placeholders stored as plain text; the Flask app does not currently implement login or use these rows for authentication.

## Main routes

| URL | Purpose |
| --- | --- |
| `/` | Public pharmacy landing page |
| `/check-availability` | Search the public availability view |
| `/admin/medicines` | View inventory |
| `/admin/medicines/add` | Add a medicine |
| `/admin/medicines/edit/<id>` | Edit a medicine |
| `/admin/customers` | View customers |
| `/admin/customers/<id>/history` | View a customer’s sale history |

Medicine deletion is handled by a POST request to `/admin/medicines/delete/<id>`.

## Repository layout

```text
app.py                 Flask routes and MySQL access
templates/             Jinja HTML templates
database/schema.sql    Flask app database schema and availability view
database/seeds.sql     Optional demo data (destructive reset)
legacy-php/            Separate PHP/MySQL app and macOS launcher
```

## Legacy PHP application

See [`legacy-php/README.md`](legacy-php/README.md) for setup, database configuration, and launch instructions. Its schema-only SQL dumps omit the source archive’s sample customer and employee records.

## Security and deployment

This repository is a development/demo project. The Flask routes under `/admin/` are not protected by authentication, the development server runs with debug mode enabled, and the legacy PHP application uses plain-text password comparisons. Do not expose either application to the public internet or use it with real customer data without first implementing appropriate authentication, access controls, input handling, and production deployment settings.
