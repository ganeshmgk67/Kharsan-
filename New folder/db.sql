-- Construction Management System Database Schema
-- Using SQLite

-- Clients Table
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_info TEXT
);

-- Projects Table
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    name TEXT NOT NULL,
    site_location TEXT,
    start_date DATE,
    status TEXT,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

-- Materials Table
CREATE TABLE materials (
    material_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    name TEXT NOT NULL,
    supplier_name TEXT,
    quantity_used INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Labor Table
CREATE TABLE labor (
    worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT,
    assigned_project_id INTEGER,
    FOREIGN KEY (assigned_project_id) REFERENCES projects(project_id)
);

-- Finances Table
CREATE TABLE finances (
    invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    total_cost REAL,
    amount_paid REAL,
    payment_status TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Users Table for Authentication
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
