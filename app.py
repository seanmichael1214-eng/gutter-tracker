from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
import base64

app = Flask(__name__)

# Data files
CUSTOMERS_FILE = 'customers.json'
JOBS_FILE = 'jobs.json'
INVENTORY_FILE = 'inventory.json'
MATERIALS_FILE = 'materials.json'

# Load/Save functions
def load_json(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            # Ensure IDs exist
            if isinstance(data, list):
                for i, item in enumerate(data):
                    if 'id' not in item:
                        item['id'] = i
            return data
    return []

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

# Customer routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/customers')
def customers():
    customers = load_json(CUSTOMERS_FILE)
    search_query = request.args.get('search', '').lower()
    
    if search_query:
        filtered = [c for c in customers 
                   if search_query in c.get('name', '').lower() 
                   or search_query in c.get('address', '').lower()
                   or search_query in c.get('phone', '').lower()]
    else:
        filtered = customers
    
    return render_template('customers.html', customers=filtered, search_query=search_query)

@app.route('/customers/add', methods=['POST'])
def add_customer():
    customers = load_json(CUSTOMERS_FILE)
    new_customer = {
        'id': len(customers),
        'name': request.form['name'],
        'address': request.form['address'],
        'phone': request.form['phone'],
        'email': request.form.get('email', ''),
        'notes': request.form.get('notes', ''),
        'created': datetime.now().isoformat()
    }
    customers.append(new_customer)
    save_json(CUSTOMERS_FILE, customers)
    return redirect(url_for('customers'))

@app.route('/customers/edit/<int:customer_id>', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customers = load_json(CUSTOMERS_FILE)
    
    if request.method == 'POST':
        customers[customer_id]['name'] = request.form['name']
        customers[customer_id]['address'] = request.form['address']
        customers[customer_id]['phone'] = request.form['phone']
        customers[customer_id]['email'] = request.form.get('email', '')
        customers[customer_id]['notes'] = request.form.get('notes', '')
        save_json(CUSTOMERS_FILE, customers)
        return redirect(url_for('customers'))
    
    customer = customers[customer_id]
    return render_template('edit_customer.html', customer=customer, customer_id=customer_id)

@app.route('/customers/delete/<int:customer_id>')
def delete_customer(customer_id):
    customers = load_json(CUSTOMERS_FILE)
    customers.pop(customer_id)
    for i, customer in enumerate(customers):
        customer['id'] = i
    save_json(CUSTOMERS_FILE, customers)
    return redirect(url_for('customers'))

# Job routes
@app.route('/jobs')
def jobs():
    jobs = load_json(JOBS_FILE)
    customers = load_json(CUSTOMERS_FILE)
    status_filter = request.args.get('status', '')
    
    if status_filter:
        filtered = [j for j in jobs if j.get('status') == status_filter]
    else:
        filtered = jobs
    
    # Add customer names to jobs
    customer_dict = {c['id']: c['name'] for c in customers}
    for job in filtered:
        job['customer_name'] = customer_dict.get(job.get('customer_id'), 'Unknown')
    
    return render_template('jobs.html', jobs=filtered, customers=customers, status_filter=status_filter)

@app.route('/jobs/add', methods=['POST'])
def add_job():
    jobs = load_json(JOBS_FILE)
    new_job = {
        'id': len(jobs),
        'customer_id': int(request.form['customer_id']),
        'title': request.form['title'],
        'description': request.form['description'],
        'scheduled_date': request.form.get('scheduled_date', ''),
        'status': 'scheduled',
        'materials_used': [],
        'photos': [],
        'total_cost': 0,
        'notes': '',
        'created': datetime.now().isoformat()
    }
    jobs.append(new_job)
    save_json(JOBS_FILE, jobs)
    return redirect(url_for('jobs'))

@app.route('/jobs/<int:job_id>')
def view_job(job_id):
    jobs = load_json(JOBS_FILE)
    customers = load_json(CUSTOMERS_FILE)
    materials = load_json(MATERIALS_FILE)
    
    job = jobs[job_id]
    customer = next((c for c in customers if c['id'] == job['customer_id']), None)
    
    return render_template('view_job.html', job=job, customer=customer, 
                         job_id=job_id, materials=materials)

@app.route('/jobs/<int:job_id>/status', methods=['POST'])
def update_job_status(job_id):
    jobs = load_json(JOBS_FILE)
    jobs[job_id]['status'] = request.form['status']
    save_json(JOBS_FILE, jobs)
    return redirect(url_for('view_job', job_id=job_id))

@app.route('/jobs/<int:job_id>/add_material', methods=['POST'])
def add_material_to_job(job_id):
    jobs = load_json(JOBS_FILE)
    inventory = load_json(INVENTORY_FILE)
    
    material_id = int(request.form['material_id'])
    quantity = float(request.form['quantity'])
    
    # Find material details
    material = next((m for m in inventory if m['id'] == material_id), None)
    if material:
        material_entry = {
            'material_id': material_id,
            'name': material['name'],
            'quantity': quantity,
            'unit_cost': material['unit_cost'],
            'total_cost': quantity * material['unit_cost']
        }
        
        if 'materials_used' not in jobs[job_id]:
            jobs[job_id]['materials_used'] = []
        
        jobs[job_id]['materials_used'].append(material_entry)
        
        # Update total cost
        jobs[job_id]['total_cost'] = sum(m['total_cost'] for m in jobs[job_id]['materials_used'])
        
        # Reduce inventory
        material['quantity'] -= quantity
        save_json(INVENTORY_FILE, inventory)
    
    save_json(JOBS_FILE, jobs)
    return redirect(url_for('view_job', job_id=job_id))

@app.route('/jobs/<int:job_id>/add_photo', methods=['POST'])
def add_photo_to_job(job_id):
    jobs = load_json(JOBS_FILE)
    
    photo_data = request.form['photo_data']
    photo_caption = request.form.get('caption', '')
    
    if 'photos' not in jobs[job_id]:
        jobs[job_id]['photos'] = []
    
    jobs[job_id]['photos'].append({
        'data': photo_data,
        'caption': photo_caption,
        'timestamp': datetime.now().isoformat()
    })
    
    save_json(JOBS_FILE, jobs)
    return redirect(url_for('view_job', job_id=job_id))

@app.route('/jobs/<int:job_id>/notes', methods=['POST'])
def update_job_notes(job_id):
    jobs = load_json(JOBS_FILE)
    jobs[job_id]['notes'] = request.form['notes']
    save_json(JOBS_FILE, jobs)
    return redirect(url_for('view_job', job_id=job_id))

# Inventory routes
@app.route('/inventory')
def inventory():
    inventory = load_json(INVENTORY_FILE)
    location_filter = request.args.get('location', '')
    low_stock = request.args.get('low_stock', '')
    
    filtered = inventory
    if location_filter:
        filtered = [i for i in filtered if i.get('location') == location_filter]
    if low_stock:
        filtered = [i for i in filtered if i.get('quantity', 0) <= i.get('low_stock_alert', 0)]
    
    return render_template('inventory.html', inventory=filtered, 
                         location_filter=location_filter, low_stock=low_stock)

@app.route('/inventory/add', methods=['POST'])
def add_inventory():
    inventory = load_json(INVENTORY_FILE)
    new_item = {
        'id': len(inventory),
        'name': request.form['name'],
        'quantity': float(request.form['quantity']),
        'unit': request.form['unit'],
        'unit_cost': float(request.form['unit_cost']),
        'location': request.form['location'],
        'low_stock_alert': float(request.form.get('low_stock_alert', 0)),
        'notes': request.form.get('notes', ''),
        'created': datetime.now().isoformat()
    }
    inventory.append(new_item)
    save_json(INVENTORY_FILE, inventory)
    return redirect(url_for('inventory'))

@app.route('/inventory/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_inventory(item_id):
    inventory = load_json(INVENTORY_FILE)
    
    if request.method == 'POST':
        inventory[item_id]['name'] = request.form['name']
        inventory[item_id]['quantity'] = float(request.form['quantity'])
        inventory[item_id]['unit'] = request.form['unit']
        inventory[item_id]['unit_cost'] = float(request.form['unit_cost'])
        inventory[item_id]['location'] = request.form['location']
        inventory[item_id]['low_stock_alert'] = float(request.form.get('low_stock_alert', 0))
        inventory[item_id]['notes'] = request.form.get('notes', '')
        save_json(INVENTORY_FILE, inventory)
        return redirect(url_for('inventory'))
    
    item = inventory[item_id]
    return render_template('edit_inventory.html', item=item, item_id=item_id)

@app.route('/inventory/delete/<int:item_id>')
def delete_inventory(item_id):
    inventory = load_json(INVENTORY_FILE)
    inventory.pop(item_id)
    for i, item in enumerate(inventory):
        item['id'] = i
    save_json(INVENTORY_FILE, inventory)
    return redirect(url_for('inventory'))

@app.route('/inventory/adjust/<int:item_id>', methods=['POST'])
def adjust_inventory(item_id):
    inventory = load_json(INVENTORY_FILE)
    adjustment = float(request.form['adjustment'])
    inventory[item_id]['quantity'] += adjustment
    save_json(INVENTORY_FILE, inventory)
    return redirect(url_for('inventory'))

# Materials library (standard materials with pricing)
@app.route('/materials')
def materials():
    materials = load_json(MATERIALS_FILE)
    return render_template('materials.html', materials=materials)

@app.route('/materials/add', methods=['POST'])
def add_material():
    materials = load_json(MATERIALS_FILE)
    new_material = {
        'id': len(materials),
        'name': request.form['name'],
        'unit': request.form['unit'],
        'unit_cost': float(request.form['unit_cost']),
        'supplier': request.form.get('supplier', ''),
        'notes': request.form.get('notes', '')
    }
    materials.append(new_material)
    save_json(MATERIALS_FILE, materials)
    return redirect(url_for('materials'))

# Reports
@app.route('/reports')
def reports():
    jobs = load_json(JOBS_FILE)
    customers = load_json(CUSTOMERS_FILE)
    inventory = load_json(INVENTORY_FILE)
    
    # Calculate statistics
    total_jobs = len(jobs)
    completed_jobs = len([j for j in jobs if j.get('status') == 'completed'])
    total_revenue = sum(j.get('total_cost', 0) for j in jobs if j.get('status') == 'completed')
    low_stock_items = [i for i in inventory if i.get('quantity', 0) <= i.get('low_stock_alert', 0)]
    
    # Recent jobs
    recent_jobs = sorted(jobs, key=lambda x: x.get('created', ''), reverse=True)[:10]
    customer_dict = {c['id']: c['name'] for c in customers}
    for job in recent_jobs:
        job['customer_name'] = customer_dict.get(job.get('customer_id'), 'Unknown')
    
    return render_template('reports.html', 
                         total_jobs=total_jobs,
                         completed_jobs=completed_jobs,
                         total_revenue=total_revenue,
                         low_stock_items=low_stock_items,
                         recent_jobs=recent_jobs)

if __name__ == '__main__':
    app.run(debug=True)
