# Code Snippets - Gutter Tracker

Reusable code patterns for common tasks.

## Table of Contents
- [Flask Routes](#flask-routes)
- [Database Operations](#database-operations)
- [AI/Gemini Integration](#aigemini-integration)
- [Frontend/Templates](#frontendfmplates)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Utilities](#utilities)

---

## Flask Routes

### Basic GET Route
```python
@app.route('/customers')
def customers():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)
```

### POST Route with Form Data
```python
@app.route('/customers/add', methods=['POST'])
def add_customer():
    name = request.form.get('name')
    phone = request.form.get('phone')
    address = request.form.get('address')

    customer = Customer(name=name, phone=phone, address=address)
    db.session.add(customer)
    db.session.commit()

    return redirect(url_for('customers'))
```

### Route with URL Parameters
```python
@app.route('/customers/edit/<int:customer_id>')
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('edit_customer.html', customer=customer)
```

### API Route with JSON
```python
@app.route('/api/customers', methods=['GET'])
def api_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'address': c.address
    } for c in customers])
```

### Route with Query Parameters
```python
@app.route('/customers')
def customers():
    search = request.args.get('search', '')

    if search:
        customers = Customer.query.filter(
            db.or_(
                Customer.name.ilike(f'%{search}%'),
                Customer.address.ilike(f'%{search}%'),
                Customer.phone.ilike(f'%{search}%')
            )
        ).all()
    else:
        customers = Customer.query.all()

    return render_template('customers.html',
                         customers=customers,
                         search_query=search)
```

---

## Database Operations

### Create Model
```python
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    jobs = db.relationship('Job', backref='customer', lazy=True)
```

### CRUD Operations
```python
# CREATE
new_customer = Customer(
    name="John Doe",
    phone="555-1234",
    address="123 Main St"
)
db.session.add(new_customer)
db.session.commit()

# READ - Get all
customers = Customer.query.all()

# READ - Get by ID
customer = Customer.query.get(customer_id)
# Or with 404 handling
customer = Customer.query.get_or_404(customer_id)

# READ - Filter
customers = Customer.query.filter_by(name="John Doe").all()
customers = Customer.query.filter(Customer.name.ilike('%john%')).all()

# UPDATE
customer = Customer.query.get(customer_id)
customer.phone = "555-9999"
db.session.commit()

# DELETE
customer = Customer.query.get(customer_id)
db.session.delete(customer)
db.session.commit()
```

### Relationships
```python
# One-to-Many
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    jobs = db.relationship('Job', backref='customer', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    title = db.Column(db.String(200))

# Access relationship
customer = Customer.query.get(1)
all_jobs = customer.jobs  # Get all jobs for this customer

job = Job.query.get(1)
customer_name = job.customer.name  # Get customer from job
```

### Complex Queries
```python
# Join query
results = db.session.query(Customer, Job).join(Job).all()

# Aggregation
from sqlalchemy import func
total_jobs = db.session.query(func.count(Job.id)).scalar()

# Order by
customers = Customer.query.order_by(Customer.name.asc()).all()

# Pagination
page = request.args.get('page', 1, type=int)
per_page = 20
customers = Customer.query.paginate(page=page, per_page=per_page)
```

---

## AI/Gemini Integration

### Basic Text Generation
```python
import google.generativeai as genai
import os

# Configure
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Generate
prompt = "Explain gutter installation best practices"
response = model.generate_content(prompt)
result = response.text
```

### Vision Analysis (Photo)
```python
import base64

# Photo data from frontend (base64)
photo_data = request.json.get('photo_data')

# Decode base64
if ',' in photo_data:
    photo_data = photo_data.split(',')[1]
image_bytes = base64.b64decode(photo_data)

# Prepare for Gemini
image_part = {
    "mime_type": "image/jpeg",
    "data": image_bytes
}

# Analyze
prompt = "Analyze this gutter installation. Identify issues and recommendations."
response = model.generate_content([prompt, image_part])
analysis = response.text
```

### Structured Output with JSON
```python
prompt = f"""
Analyze this gutter job and provide estimate.

REQUIRED JSON FORMAT:
{{
    "material_cost": 0.00,
    "labor_cost": 0.00,
    "total_cost": 0.00,
    "notes": "explanation"
}}

House: {house_type}
Linear feet: {linear_feet}
"""

response = model.generate_content(prompt)
result_text = response.text

# Extract JSON
import json
import re
json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
if json_match:
    data = json.loads(json_match.group())
```

### Error Handling for AI
```python
try:
    response = model.generate_content(prompt)
    result = response.text

    if not result:
        raise ValueError("Empty response from AI")

    return jsonify({'success': True, 'result': result})

except Exception as e:
    print(f"AI Error: {str(e)}")
    return jsonify({
        'success': False,
        'error': 'AI service temporarily unavailable'
    }), 500
```

### AI Helper Function Pattern
```python
def get_ai_estimate(house_type, linear_feet, material_type="aluminum"):
    """Get AI-generated estimate for gutter job"""

    prompt = f"""
    You are a professional gutter installation estimator.

    DETAILS:
    - House type: {house_type}
    - Linear feet: {linear_feet}
    - Material: {material_type}

    Provide detailed cost breakdown including:
    - Material costs
    - Labor costs
    - Total estimate

    Be specific with prices based on 2024 market rates.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating estimate: {str(e)}"
```

---

## Frontend/Templates

### Jinja Template Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Gutter Tracker{% endblock %}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    {% include 'navbar.html' %}

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <a href="/help" class="help-fab" title="Get Help">❓</a>
</body>
</html>
```

### Navigation Bar Component
```html
<!-- templates/navbar.html -->
<nav class="navbar">
    <h1>Gutter Tracker</h1>
    <ul>
        <li><a href="/" class="{% if request.endpoint == 'dashboard' %}active{% endif %}">Dashboard</a></li>
        <li><a href="/customers" class="{% if request.endpoint == 'customers' %}active{% endif %}">Customers</a></li>
        <li><a href="/jobs" class="{% if request.endpoint == 'jobs' %}active{% endif %}">Jobs</a></li>
        <li><a href="/inventory" class="{% if request.endpoint == 'inventory' %}active{% endif %}">Inventory</a></li>
    </ul>
</nav>
```

### Form with Validation
```html
<form method="POST" action="/customers/add">
    <div class="form-group">
        <label>Customer Name *</label>
        <input type="text" name="name" required>
    </div>

    <div class="form-group">
        <label>Phone *</label>
        <input type="tel" name="phone" pattern="[0-9\-\(\) ]+" required>
    </div>

    <div class="form-group">
        <label>Email</label>
        <input type="email" name="email">
    </div>

    <button type="submit" class="btn btn-success">Add Customer</button>
</form>
```

### Loop with Conditional
```html
{% if customers|length == 0 %}
    <div class="no-results">No customers found</div>
{% else %}
    {% for customer in customers %}
    <div class="card">
        <h3>{{ customer.name }}</h3>
        <p><strong>Phone:</strong> {{ customer.phone }}</p>
        <p><strong>Address:</strong> {{ customer.address }}</p>

        <div class="card-actions">
            <a href="/customers/edit/{{ customer.id }}" class="btn btn-primary">Edit</a>
            <a href="/customers/delete/{{ customer.id }}"
               onclick="return confirm('Delete {{ customer.name }}?')"
               class="btn btn-danger">Delete</a>
        </div>
    </div>
    {% endfor %}
{% endif %}
```

### JavaScript AJAX Call
```html
<script>
function analyzePhoto() {
    const photoData = capturedImageData;  // base64 image

    fetch('/api/ai/analyze-photo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            photo_data: photoData
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('result').innerHTML = data.analysis;
        } else {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Request failed');
    });
}
</script>
```

---

## API Endpoints

### POST Endpoint with JSON
```python
@app.route('/api/ai/estimate', methods=['POST'])
def api_estimate():
    try:
        data = request.get_json()

        # Validate input
        if not data or 'linear_feet' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: linear_feet'
            }), 400

        linear_feet = data.get('linear_feet')
        house_type = data.get('house_type', '1-story')

        # Process
        estimate = get_ai_estimate(house_type, linear_feet)

        return jsonify({
            'success': True,
            'estimate': estimate
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
```

### File Upload Endpoint
```python
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'Empty filename'}), 400

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join('uploads', filename)
    file.save(filepath)

    return jsonify({
        'success': True,
        'filename': filename
    })
```

---

## Authentication

### Login Required Decorator
```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Usage
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

### Login Route
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')

        if password == os.getenv('APP_PASSWORD'):
            session['logged_in'] = True
            session.permanent = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid password')

    return render_template('login.html')
```

### Logout Route
```python
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
```

---

## Utilities

### Date Formatting
```python
from datetime import datetime

# In Python
created_at = datetime.utcnow()
formatted = created_at.strftime('%Y-%m-%d %H:%M:%S')

# In Jinja template
{{ customer.created_at.strftime('%B %d, %Y') }}
```

### Currency Formatting
```python
# In Python
price = 1234.56
formatted = f"${price:,.2f}"  # $1,234.56

# In Jinja template
{{ "%.2f"|format(price) }}
${{ price|round(2) }}
```

### Phone Number Formatting
```python
import re

def format_phone(phone):
    # Remove all non-digits
    digits = re.sub(r'\D', '', phone)

    # Format as (XXX) XXX-XXXX
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone
```

### Slug Generation
```python
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

# Usage
title = "Gutter Installation - Main Street"
slug = slugify(title)  # "gutter-installation-main-street"
```

### File Size Validation
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    # Check size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE:
        return jsonify({'error': 'File too large'}), 400

    # Process file
    ...
```

### Environment Variable Helper
```python
import os

def get_env(key, default=None, required=False):
    """Get environment variable with validation"""
    value = os.getenv(key, default)

    if required and not value:
        raise ValueError(f"Required environment variable {key} not set")

    return value

# Usage
DATABASE_URL = get_env('DATABASE_URL', required=True)
DEBUG = get_env('DEBUG', default='False') == 'True'
```

---

## CSS Snippets

### Outdoor-Optimized Button
```css
.btn {
    /* Large touch target for gloves */
    min-height: 54px;
    min-width: 54px;
    padding: 15px 30px;

    /* High contrast */
    background: var(--accent);
    color: white;
    font-size: 18px;
    font-weight: 600;

    /* Visual feedback */
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
}

.btn:active {
    transform: translateY(0);
}
```

### Floating Action Button
```css
.help-fab {
    position: fixed;
    bottom: 24px;
    right: 24px;
    width: 64px;
    height: 64px;

    background: linear-gradient(135deg, var(--accent) 0%, #00ff88 100%);
    color: white;
    font-size: 32px;

    border-radius: 50%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);

    display: flex;
    align-items: center;
    justify-content: center;

    text-decoration: none;
    transition: transform 0.2s;
    z-index: 1000;
}

.help-fab:hover {
    transform: scale(1.1);
}
```

### Responsive Card Grid
```css
.card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
}

.card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
```

---

## Testing Snippets

### Basic Test Function
```python
import pytest
from app_gemini import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
```

### API Test
```python
def test_api_endpoint(client):
    response = client.post('/api/ai/estimate',
        json={
            'house_type': '1-story',
            'linear_feet': '100'
        }
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'estimate' in data
```

---

Copy and adapt these snippets for your development needs!
