from flask import Flask, render_template, request, redirect, url_for, send_file, session
from flask_session import Session
import sqlite3
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import date
import csv
from functools import wraps
import hashlib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get configuration from environment variables
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
Session(app)

# Get the directory where the app is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'construction.db')
DB_SQL = os.path.join(BASE_DIR, 'db.sql')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        print(f"Creating database at {DATABASE}")
        conn = get_db_connection()
        try:
            with open(DB_SQL, 'r') as f:
                sql = f.read()
            print(f"Reading SQL from {DB_SQL}")
            conn.executescript(sql)
            # Add sample data
            conn.execute("INSERT INTO clients (name, contact_info) VALUES ('ABC Corp', 'abc@corp.com')")
            conn.execute("INSERT INTO clients (name, contact_info) VALUES ('XYZ Ltd', 'xyz@ltd.com')")
            conn.execute("INSERT INTO projects (client_id, name, site_location, start_date, status) VALUES (1, 'Office Building', 'Downtown', '2024-01-15', 'active')")
            conn.execute("INSERT INTO projects (client_id, name, site_location, start_date, status) VALUES (2, 'Residential Complex', 'Suburb', '2024-02-01', 'completed')")
            conn.execute("INSERT INTO materials (project_id, name, supplier_name, quantity_used) VALUES (1, 'Cement', 'BuildSupplies Inc', 500)")
            conn.execute("INSERT INTO labor (name, role, assigned_project_id) VALUES ('John Doe', 'Engineer', 1)")
            conn.execute("INSERT INTO finances (project_id, total_cost, amount_paid, payment_status) VALUES (1, 150000.00, 75000.00, 'pending')")
            # Add default user
            password_hash = hashlib.sha256('admin123'.encode()).hexdigest()
            conn.execute("INSERT INTO users (username, password, email) VALUES ('admin', ?, 'admin@construction.com')", (password_hash,))
            conn.commit()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            conn.close()
    else:
        print(f"Database already exists at {DATABASE}")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password_hash)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        password_hash = hash_password(password)
        conn = get_db_connection()
        
        try:
            conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                        (username, password_hash, email))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            conn.close()
            return render_template('register.html', error='Username or email already exists')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    total_projects = conn.execute('SELECT COUNT(*) as count FROM projects').fetchone()['count']
    active_projects = conn.execute('SELECT COUNT(*) as count FROM projects WHERE status = "active"').fetchone()['count']
    total_clients = conn.execute('SELECT COUNT(*) as count FROM clients').fetchone()['count']
    total_materials = conn.execute('SELECT COUNT(*) as count FROM materials').fetchone()['count']
    total_workers = conn.execute('SELECT COUNT(*) as count FROM labor').fetchone()['count']
    total_invoices = conn.execute('SELECT COUNT(*) as count FROM finances').fetchone()['count']
    total_revenue = conn.execute('SELECT SUM(total_cost) as total FROM finances').fetchone()['total'] or 0
    pending_payments = conn.execute('SELECT SUM(total_cost - amount_paid) as pending FROM finances WHERE payment_status != "paid"').fetchone()['pending'] or 0
    conn.close()
    return render_template('dashboard.html', total_projects=total_projects, active_projects=active_projects, total_clients=total_clients, total_materials=total_materials, total_workers=total_workers, total_invoices=total_invoices, total_revenue=total_revenue, pending_payments=pending_payments)
    conn = get_db_connection()
    total_projects = conn.execute('SELECT COUNT(*) as count FROM projects').fetchone()['count']
    active_projects = conn.execute('SELECT COUNT(*) as count FROM projects WHERE status = "active"').fetchone()['count']
    total_clients = conn.execute('SELECT COUNT(*) as count FROM clients').fetchone()['count']
    total_materials = conn.execute('SELECT COUNT(*) as count FROM materials').fetchone()['count']
    total_workers = conn.execute('SELECT COUNT(*) as count FROM labor').fetchone()['count']
    total_invoices = conn.execute('SELECT COUNT(*) as count FROM finances').fetchone()['count']
    total_revenue = conn.execute('SELECT SUM(total_cost) as total FROM finances').fetchone()['total'] or 0
    pending_payments = conn.execute('SELECT SUM(total_cost - amount_paid) as pending FROM finances WHERE payment_status != "paid"').fetchone()['pending'] or 0
    conn.close()
    return render_template('dashboard.html', total_projects=total_projects, active_projects=active_projects, total_clients=total_clients, total_materials=total_materials, total_workers=total_workers, total_invoices=total_invoices, total_revenue=total_revenue, pending_payments=pending_payments)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    if request.method == 'POST':
        client_id = request.form['client_id']
        name = request.form['name']
        site_location = request.form['site_location']
        start_date = request.form['start_date']
        status = request.form['status']
        conn = get_db_connection()
        
        # Insert project
        cursor = conn.execute('INSERT INTO projects (client_id, name, site_location, start_date, status) VALUES (?, ?, ?, ?, ?)',
                     (client_id, name, site_location, start_date, status))
        project_id = cursor.lastrowid
        
        # Assign workers to project
        worker_ids = request.form.getlist('worker_ids')
        for worker_id in worker_ids:
            if worker_id:
                conn.execute('UPDATE labor SET assigned_project_id = ? WHERE worker_id = ?',
                           (project_id, worker_id))
        
        # Add materials to project
        material_names = request.form.getlist('material_names')
        material_suppliers = request.form.getlist('material_suppliers')
        material_quantities = request.form.getlist('material_quantities')
        
        for i in range(len(material_names)):
            if material_names[i]:
                quantity = material_quantities[i] if i < len(material_quantities) and material_quantities[i] else 0
                conn.execute('INSERT INTO materials (project_id, name, supplier_name, quantity_used) VALUES (?, ?, ?, ?)',
                           (project_id, material_names[i], material_suppliers[i] if i < len(material_suppliers) else '', quantity))
        
        conn.commit()
        conn.close()
        return redirect(url_for('projects'))
    
    conn = get_db_connection()
    clients = conn.execute('SELECT * FROM clients').fetchall()
    workers = conn.execute('SELECT * FROM labor WHERE assigned_project_id IS NULL').fetchall()
    conn.close()
    
    return render_template('add_project.html', clients=clients, workers=workers)

@app.route('/edit_project/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    if request.method == 'POST':
        client_id = request.form['client_id']
        name = request.form['name']
        site_location = request.form['site_location']
        start_date = request.form['start_date']
        status = request.form['status']
        conn = get_db_connection()
        conn.execute('UPDATE projects SET client_id = ?, name = ?, site_location = ?, start_date = ?, status = ? WHERE project_id = ?',
                     (client_id, name, site_location, start_date, status, id))
        
        # Update worker assignments
        # First, remove all current assignments for this project
        conn.execute('UPDATE labor SET assigned_project_id = NULL WHERE assigned_project_id = ?', (id,))
        
        # Then add new assignments
        worker_ids = request.form.getlist('worker_ids')
        for worker_id in worker_ids:
            if worker_id:
                conn.execute('UPDATE labor SET assigned_project_id = ? WHERE worker_id = ?',
                           (id, worker_id))
        
        # Remove old materials and add new ones
        conn.execute('DELETE FROM materials WHERE project_id = ?', (id,))
        
        material_names = request.form.getlist('material_names')
        material_suppliers = request.form.getlist('material_suppliers')
        material_quantities = request.form.getlist('material_quantities')
        
        for i in range(len(material_names)):
            if material_names[i]:
                quantity = material_quantities[i] if i < len(material_quantities) and material_quantities[i] else 0
                conn.execute('INSERT INTO materials (project_id, name, supplier_name, quantity_used) VALUES (?, ?, ?, ?)',
                           (id, material_names[i], material_suppliers[i] if i < len(material_suppliers) else '', quantity))
        
        conn.commit()
        conn.close()
        return redirect(url_for('projects'))
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE project_id = ?', (id,)).fetchone()
    clients = conn.execute('SELECT * FROM clients').fetchall()
    
    # Get all workers and mark which ones are assigned to this project
    assigned_workers = conn.execute('SELECT worker_id FROM labor WHERE assigned_project_id = ?', (id,)).fetchall()
    assigned_worker_ids = [w['worker_id'] for w in assigned_workers]
    
    workers = conn.execute('SELECT * FROM labor WHERE assigned_project_id IS NULL OR assigned_project_id = ?', (id,)).fetchall()
    materials = conn.execute('SELECT * FROM materials WHERE project_id = ?', (id,)).fetchall()
    
    conn.close()
    return render_template('edit_project.html', project=project, clients=clients, workers=workers, assigned_worker_ids=assigned_worker_ids, materials=materials)

@app.route('/delete_project/<int:id>', methods=['POST'])
@login_required
def delete_project(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM projects WHERE project_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('projects'))

@app.route('/materials')
@login_required
def materials():
    conn = get_db_connection()
    materials_list = conn.execute('''
        SELECT m.material_id, m.name, m.supplier_name, m.quantity_used, p.name as project_name
        FROM materials m
        JOIN projects p ON m.project_id = p.project_id
    ''').fetchall()
    conn.close()
    return render_template('materials.html', materials=materials_list)

@app.route('/projects')
@login_required
def projects():
    conn = get_db_connection()
    projects_list = conn.execute('SELECT * FROM projects').fetchall()
    
    # Fetch workers and materials for each project
    project_details = []
    for project in projects_list:
        workers = conn.execute('SELECT name, role FROM labor WHERE assigned_project_id = ?', (project['project_id'],)).fetchall()
        materials = conn.execute('SELECT name, quantity_used FROM materials WHERE project_id = ?', (project['project_id'],)).fetchall()
        project_details.append({
            'project': project,
            'workers': workers,
            'materials': materials
        })
    
    conn.close()
    return render_template('projects.html', project_details=project_details)

@app.route('/labor')
@login_required
def labor():
    conn = get_db_connection()
    labor_list = conn.execute('SELECT * FROM labor').fetchall()
    conn.close()
    return render_template('labor.html', labor=labor_list)

@app.route('/finances')
@login_required
def finances():
    status_filter = request.args.get('status')
    conn = get_db_connection()
    if status_filter:
        finances_list = conn.execute('SELECT * FROM finances WHERE payment_status = ?', (status_filter,)).fetchall()
    else:
        finances_list = conn.execute('SELECT * FROM finances').fetchall()
    conn.close()
    return render_template('finances.html', finances=finances_list, status_filter=status_filter)

@app.route('/clients')
@login_required
def clients():
    conn = get_db_connection()
    clients_list = conn.execute('SELECT * FROM clients').fetchall()
    conn.close()
    return render_template('clients.html', clients=clients_list)

@app.route('/add_client', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        conn = get_db_connection()
        conn.execute('INSERT INTO clients (name, contact_info) VALUES (?, ?)', (name, contact_info))
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))
    return render_template('add_client.html')

@app.route('/edit_client/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    if request.method == 'POST':
        name = request.form['name']
        contact_info = request.form['contact_info']
        conn = get_db_connection()
        conn.execute('UPDATE clients SET name = ?, contact_info = ? WHERE client_id = ?',
                     (name, contact_info, id))
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))
    conn = get_db_connection()
    client = conn.execute('SELECT * FROM clients WHERE client_id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_client.html', client=client)

@app.route('/delete_client/<int:id>', methods=['POST'])
@login_required
def delete_client(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM clients WHERE client_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('clients'))

@app.route('/add_material', methods=['GET', 'POST'])
@login_required
def add_material():
    if request.method == 'POST':
        project_id = request.form['project_id']
        name = request.form['name']
        supplier_name = request.form['supplier_name']
        quantity_used = request.form['quantity_used']
        conn = get_db_connection()
        conn.execute('INSERT INTO materials (project_id, name, supplier_name, quantity_used) VALUES (?, ?, ?, ?)',
                     (project_id, name, supplier_name, quantity_used))
        conn.commit()
        conn.close()
        return redirect(url_for('materials'))
    return render_template('add_material.html')

@app.route('/edit_material/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_material(id):
    if request.method == 'POST':
        project_id = request.form['project_id']
        name = request.form['name']
        supplier_name = request.form['supplier_name']
        quantity_used = request.form['quantity_used']
        conn = get_db_connection()
        conn.execute('UPDATE materials SET project_id = ?, name = ?, supplier_name = ?, quantity_used = ? WHERE material_id = ?',
                     (project_id, name, supplier_name, quantity_used, id))
        conn.commit()
        conn.close()
        return redirect(url_for('materials'))
    conn = get_db_connection()
    material = conn.execute('SELECT * FROM materials WHERE material_id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_material.html', material=material)

@app.route('/delete_material/<int:id>', methods=['POST'])
@login_required
def delete_material(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM materials WHERE material_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('materials'))

@app.route('/add_worker', methods=['GET', 'POST'])
@login_required
def add_worker():
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        assigned_project_id = request.form['assigned_project_id']
        conn = get_db_connection()
        conn.execute('INSERT INTO labor (name, role, assigned_project_id) VALUES (?, ?, ?)',
                     (name, role, assigned_project_id))
        conn.commit()
        conn.close()
        return redirect(url_for('labor'))
    return render_template('add_worker.html')

@app.route('/edit_worker/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_worker(id):
    if request.method == 'POST':
        name = request.form['name']
        role = request.form['role']
        assigned_project_id = request.form['assigned_project_id']
        conn = get_db_connection()
        conn.execute('UPDATE labor SET name = ?, role = ?, assigned_project_id = ? WHERE worker_id = ?',
                     (name, role, assigned_project_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('labor'))
    conn = get_db_connection()
    worker = conn.execute('SELECT * FROM labor WHERE worker_id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_worker.html', worker=worker)

@app.route('/delete_worker/<int:id>', methods=['POST'])
@login_required
def delete_worker(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM labor WHERE worker_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('labor'))

@app.route('/add_invoice', methods=['GET', 'POST'])
@login_required
def add_invoice():
    if request.method == 'POST':
        project_id = request.form['project_id']
        total_cost = request.form['total_cost']
        amount_paid = request.form['amount_paid']
        payment_status = request.form['payment_status']
        conn = get_db_connection()
        conn.execute('INSERT INTO finances (project_id, total_cost, amount_paid, payment_status) VALUES (?, ?, ?, ?)',
                     (project_id, total_cost, amount_paid, payment_status))
        conn.commit()
        conn.close()
        return redirect(url_for('finances'))
    return render_template('add_invoice.html')

@app.route('/edit_invoice/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_invoice(id):
    if request.method == 'POST':
        project_id = request.form['project_id']
        total_cost = request.form['total_cost']
        amount_paid = request.form['amount_paid']
        payment_status = request.form['payment_status']
        conn = get_db_connection()
        conn.execute('UPDATE finances SET project_id = ?, total_cost = ?, amount_paid = ?, payment_status = ? WHERE invoice_id = ?',
                     (project_id, total_cost, amount_paid, payment_status, id))
        conn.commit()
        conn.close()
        return redirect(url_for('finances'))
    conn = get_db_connection()
    invoice = conn.execute('SELECT * FROM finances WHERE invoice_id = ?', (id,)).fetchone()
    conn.close()
    return render_template('edit_invoice.html', invoice=invoice)

@app.route('/delete_invoice/<int:id>', methods=['POST'])
@login_required
def delete_invoice(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM finances WHERE invoice_id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('finances'))

@app.route('/download_invoice/<int:id>')
@login_required
def download_invoice(id):
    conn = get_db_connection()
    invoice = conn.execute('''
        SELECT f.*, p.name as project_name, c.name as client_name
        FROM finances f
        JOIN projects p ON f.project_id = p.project_id
        JOIN clients c ON p.client_id = c.client_id
        WHERE f.invoice_id = ?
    ''', (id,)).fetchone()
    conn.close()
    if not invoice:
        return "Invoice not found", 404

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Construction Invoice Receipt", styles['Title']))
    story.append(Spacer(1, 12))

    # Invoice details
    data = [
        ['Invoice ID:', str(invoice['invoice_id'])],
        ['Client:', invoice['client_name']],
        ['Project:', invoice['project_name']],
        ['Total Cost:', f"${invoice['total_cost']:.2f}"],
        ['Amount Paid:', f"${invoice['amount_paid']:.2f}"],
        ['Payment Status:', invoice['payment_status'].capitalize()],
        ['Date:', 'Generated on ' + str(date.today())]
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (1, 0), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"invoice_{id}.pdf", mimetype='application/pdf')

@app.route('/export/<table>')
@login_required
def export_table(table):
    tables = ['clients', 'projects', 'materials', 'labor', 'finances']
    if table not in tables:
        return "Invalid table", 400
    conn = get_db_connection()
    data = conn.execute(f'SELECT * FROM {table}').fetchall()
    conn.close()
    if not data:
        return "No data", 404
    output = BytesIO()
    writer = csv.writer(output)
    writer.writerow(data[0].keys())
    for row in data:
        writer.writerow(row)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name=f'{table}.csv', mimetype='text/csv')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
