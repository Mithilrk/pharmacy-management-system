# Legacy PHP application

This folder contains the PHP/MySQL implementation supplied in `Pharmacy-Management-System-master.zip` and the `Pharmacia.app` macOS launcher. The existing Flask application remains at the repository root.

## Requirements

- PHP with the `mysqli` extension
- MySQL or MariaDB
- macOS to use the optional `Pharmacia.app` launcher

## Set up the database

1. Create a database named `pharmacy` in MySQL.
2. Import [`pharmacy.sql`](pharmacy.sql). It contains the tables and routines without the archive’s customer, employee, and login sample records.
3. Configure MySQL connection details in `PHARMACY/config.php`. The included defaults use `localhost`, user `root`, an empty password, and database `pharmacy`; adjust them for your local setup.

The legacy login code uses plain text password comparisons. The schema-only import does not create accounts. Do not deploy this application with real users or expose it to the public internet without replacing its authentication and securing the PHP endpoints.

## Run with PHP

From this directory, run:

```sh
php -S 127.0.0.1:8000 -t PHARMACY
```

Then open <http://127.0.0.1:8000/mainpage.php>.

## Run on macOS

Open `Pharmacia.app`. It starts PHP’s built-in server on `127.0.0.1:8000` and opens the login page. PHP must be installed and available as `php` on your `PATH` (or at `/opt/homebrew/bin/php`). MySQL must already be running.

## Included material

- `PHARMACY/`: PHP pages, stylesheets, and application images
- `pharmacy.sql`: schema and routines for initial setup, with sample rows removed
- `pharmacy-tables.sql`: alternate schema dump, with sample rows removed
- `restore-routines.sql`: stored procedures and functions
- `ER_Diagram.png`, `RelationalModel.png`: supplied database diagrams
- `Pharmacia.app/`: portable macOS launcher bundle
