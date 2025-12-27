from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    current_app,
)
from functools import wraps
from datetime import datetime
import base64

from .extensions import db
from .models import Customer, Job, Material, InventoryItem, JobMaterial, JobPhoto
from .ai import get_ai_estimate, analyze_photo, suggest_schedule, gemini_model

# Main blueprint
main = Blueprint("main", __name__)

# Simple auth decorator

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("main.login"))
        return f(*args, **kwargs)
    return wrapper

# Splash / Login
@main.route("/")
def splash():
    if session.get("logged_in"):
        return redirect(url_for("main.dashboard"))
    return render_template("splash.html")

@main.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "").strip()
        if password == current_app.config.get("APP_PASSWORD", ""):
            session["logged_in"] = True
            current_app.logger.info("Successful login from %s", request.remote_addr)
            return redirect(url_for("main.dashboard"))
        else:
            current_app.logger.info("Failed login attempt from %s", request.remote_addr)
            error = "Invalid password"
    return render_template("login.html", error=error)

@main.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("main.splash"))

# Home with per-user inventories
@main.route("/home")
@login_required
def home():
    customers = Customer.query.all()
    current_id = request.args.get("customer_id", type=int)
    # Persist current owner for per-user isolation
    if current_id:
        session["current_owner_id"] = current_id
    inventories = InventoryItem.query.filter_by(owner_id=current_id).all() if current_id else []
    return render_template("index.html", customers=customers, current_id=current_id, inventories=inventories)

# Dashboard
@main.route("/dashboard")
@login_required
def dashboard():
    total_jobs = Job.query.count()
    completed_jobs = Job.query.filter_by(status="completed").count()
    scheduled_jobs = Job.query.filter_by(status="scheduled").count()
    total_revenue = (db.session.query(db.func.sum(Job.total_cost)).filter_by(status="completed").scalar() or 0)
    return render_template(
        "dashboard.html",
        total_jobs=total_jobs,
        completed_jobs=completed_jobs,
        scheduled_jobs=scheduled_jobs,
        total_revenue=total_revenue,
    )

# Customers
@main.route("/customers")
@login_required
def customers():
    search_query = request.args.get("search", "").lower()
    if search_query:
        customers = Customer.query.filter(
            db.or_(
                Customer.name.ilike(f"%{search_query}%"),
                Customer.address.ilike(f"%{search_query}%"),
                Customer.phone.ilike(f"%{search_query}%"),
            )
        ).all()
    else:
        customers = Customer.query.order_by(Customer.created.desc()).all()
    return render_template("customers.html", customers=customers, search_query=search_query)

@main.route("/customers/add", methods=["POST"])
@login_required
def add_customer():
    customer = Customer(
        name=request.form["name"],
        address=request.form["address"],
        phone=request.form["phone"],
        email=request.form.get("email", ""),
        notes=request.form.get("notes", ""),
    )
    db.session.add(customer)
    db.session.commit()
    return redirect(url_for("main.customers"))

@main.route("/customers/edit/<int:customer_id>", methods=["GET", "POST"])
@login_required
def edit_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    if request.method == "POST":
        customer.name = request.form["name"]
        customer.address = request.form["address"]
        customer.phone = request.form["phone"]
        customer.email = request.form.get("email", "")
        customer.notes = request.form.get("notes", "")
        db.session.commit()
        return redirect(url_for("main.customers"))
    return render_template("edit_customer.html", customer=customer)

@main.route("/customers/delete/<int:customer_id>")
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return redirect(url_for("main.customers"))

# Jobs (minimal)
@main.route("/jobs")
@login_required
def jobs():
    status_filter = request.args.get("status", "")
    if status_filter:
        jobs = Job.query.filter_by(status=status_filter).order_by(Job.scheduled_date.desc()).all()
    else:
        jobs = Job.query.order_by(Job.scheduled_date.desc()).all()
    customers = Customer.query.all()
    return render_template("jobs.html", jobs=jobs, customers=customers, status_filter=status_filter)

@main.route("/jobs/add", methods=["POST"])
@login_required
def add_job():
    customer_id = int(request.form["customer_id"])
    job = Job(
        customer_id=customer_id,
        title=request.form["title"],
        description=request.form["description"],
        scheduled_date=(datetime.strptime(request.form["scheduled_date"], "%Y-%m-%d").date() if request.form.get("scheduled_date") else None),
        status="scheduled",
    )
    if request.form.get("use_ai_estimate") == "on":
        owner = Customer.query.get(customer_id)
        job.ai_estimate = get_ai_estimate(job.description, owner.address) if owner else None
    db.session.add(job)
    db.session.commit()
    return redirect(url_for("main.jobs"))

@main.route("/jobs/<int:job_id>")
@login_required
def view_job(job_id):
    job = Job.query.get_or_404(job_id)
    materials = Material.query.all()
    return render_template("view_job.html", job=job, materials=materials)

@main.route("/jobs/<int:job_id>/status", methods=["POST"])
@login_required
def update_job_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("main.view_job", job_id=job_id))

@main.route("/jobs/<int:job_id>/add_photo", methods=["POST"])
@login_required
def add_photo_to_job(job_id):
    job = Job.query.get_or_404(job_id)
    photo_data = request.form["photo_data"]
    caption = request.form.get("caption", "")
    photo = JobPhoto(job_id=job_id, photo_data=photo_data, caption=caption)
    if request.form.get("analyze_photo") == "on":
        photo.ai_analysis = analyze_photo(photo_data, f"Job: {job.title}")
    db.session.add(photo)
    db.session.commit()
    return redirect(url_for("main.view_job", job_id=job_id))

# Inventory (full CRUD)
@main.route("/inventory")
@login_required
def inventory():
    location_filter = request.args.get("location", "")
    # Per-user isolation: only show items for the currently selected owner
    owner_id = session.get("current_owner_id")
    if owner_id is None:
        inventory_items = []
    else:
        query = InventoryItem.query.filter_by(owner_id=owner_id)
        if location_filter:
            query = query.filter_by(location=location_filter)
        inventory_items = query.all()
    return render_template("inventory.html", inventory=inventory_items, location_filter=location_filter)

@main.route("/inventory/add", methods=["POST"])
@login_required
def add_inventory():
    owner_id = int(request.form["owner_id"]) if request.form.get("owner_id") else None
    if owner_id is None:
        from flask import session as _session
        owner_id = _session.get("current_owner_id")
    item = InventoryItem(
        name=request.form["name"],
        quantity=float(request.form["quantity"]),
        unit=request.form["unit"],
        unit_cost=float(request.form["unit_cost"]),
        location=request.form["location"],
        low_stock_alert=float(request.form.get("low_stock_alert", 0)),
        notes=request.form.get("notes", ""),
        owner_id=owner_id,
    )
    db.session.add(item)
    db.session.commit()
    return redirect(url_for("main.inventory"))

@main.route("/inventory/edit/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_inventory(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    if request.method == "POST":
        item.name = request.form["name"]
        item.quantity = float(request.form["quantity"])
        item.unit = request.form["unit"]
        item.unit_cost = float(request.form["unit_cost"])
        item.location = request.form["location"]
        item.low_stock_alert = float(request.form.get("low_stock_alert", 0))
        item.notes = request.form.get("notes", "")
        item.owner_id = int(request.form["owner_id"]) if request.form.get("owner_id") else None
        db.session.commit()
        return redirect(url_for("main.inventory"))
    return render_template("edit_inventory.html", item=item)

@main.route("/inventory/delete/<int:item_id>")
@login_required
def delete_inventory(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("main.inventory"))

# Utilities and API
@main.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.json or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"response": "Please send a message."})
    # Simple inventory commands
    def parse_kv(text):
        d = {}
        for part in text.split(','):
            if '=' in part:
                k,v = part.split('=',1)
                d[k.strip()] = v.strip()
        return d
    lm = message.lower()
    if lm.startswith("inventory-add"):
        rest = message[len("inventory-add"):].strip()
        kv = parse_kv(rest)
        owner_id = int(kv.get("owner_id")) if kv.get("owner_id") else None
        item = InventoryItem(
            name=kv.get("name","Inventory Item"),
            quantity=float(kv.get("quantity", 0)),
            unit=kv.get("unit", ""),
            unit_cost=float(kv.get("unit_cost", 0)),
            location=kv.get("location", ""),
            low_stock_alert=float(kv.get("low_stock_alert", 0)),
            notes=kv.get("notes", ""),
            owner_id=owner_id,
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({"response": f"Added item {item.name} (id {item.id})"})
    if lm.startswith("inventory-update"):
        rest = message[len("inventory-update"):].strip()
        kv = parse_kv(rest)
        if "id" not in kv:
            return jsonify({"response": "Missing id for update"})
        item = InventoryItem.query.get(int(kv["id"]))
        if not item:
            return jsonify({"response": "Item not found"})
        if "name" in kv: item.name = kv["name"]
        if "quantity" in kv: item.quantity = float(kv["quantity"])
        if "unit" in kv: item.unit = kv["unit"]
        if "unit_cost" in kv: item.unit_cost = float(kv["unit_cost"])
        if "location" in kv: item.location = kv["location"]
        if "notes" in kv: item.notes = kv["notes"]
        if "low_stock_alert" in kv: item.low_stock_alert = float(kv["low_stock_alert"])
        if "owner_id" in kv: item.owner_id = int(kv["owner_id"]) if kv["owner_id"] else None
        db.session.commit()
        return jsonify({"response": f"Updated item {item.id}"})
    if lm.startswith("inventory-delete"):
        rest = message[len("inventory-delete"):].strip()
        kv = parse_kv(rest)
        if "id" not in kv:
            return jsonify({"response": "Missing id for delete"})
        item = InventoryItem.query.get(int(kv["id"]))
        if not item:
            return jsonify({"response": "Item not found"})
        db.session.delete(item)
        db.session.commit()
        return jsonify({"response": f"Deleted item {item.id}"})
    if lm.startswith("inventory-scan"):
        rest = message[len("inventory-scan"):].strip()
        kv = parse_kv(rest)
        image_data = kv.get("image_data") or kv.get("photo_data")
        if not image_data:
            return jsonify({"response": "No image_data provided"})
        item = InventoryItem(name="Scanned Item", quantity=1, unit="each", location=kv.get("location", ""), owner_id=int(kv.get("owner_id")) if kv.get("owner_id") else None)
        db.session.add(item)
        db.session.commit()
        return jsonify({"response": f"Created scanned inventory item {item.name} (id {item.id})"})
    if lm.startswith("/") or lm.startswith("!"):
        return jsonify({"response": "Unknown command. Try inventory- commands or /help"})
    # Fallback
    if hasattr(gemini_model, 'generate_content'):
        try:
            resp = gemini_model.generate_content(f"You are helping a user: {message}")
            return jsonify({"response": resp.text})
        except Exception:
            pass
    return jsonify({"response": f"You asked: {message}. I can help with inventory commands."})


@main.route("/api/ai/help", methods=["POST"])
def api_ai_help():
    data = request.json or {}
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Question required"}), 400
    try:
        prompt = f"You are a helpful tech support assistant. Question: {question}"
        response = gemini_model.generate_content(prompt)
        return jsonify({"success": True, "answer": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main.route("/api/ai/estimate", methods=["POST"])
def api_ai_estimate():
    data = request.json or {}
    description = data.get("description", "")
    address = data.get("address", "Unknown address")
    if not description:
        return jsonify({"error": "Description required"}), 400
    try:
        estimate = get_ai_estimate(description, address)
        return jsonify({"success": True, "estimate": estimate, "provider": "LocalFallback"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@main.route("/api/ai/suggest-schedule", methods=["POST"])
def api_suggest_schedule():
    data = request.json or {}
    address = data.get("address", "")
    suggestion = "Next available"
    if address:
        suggestion = f"Date suggested for {address}: soon"
    return jsonify({"suggestion": suggestion})


@main.route("/api/ai/scan-inventory", methods=["POST"])
def api_scan_inventory():
    data = request.json or {}
    photo_data = data.get("photo_data", "")
    if not photo_data:
        return jsonify({"error": "Photo data required"}), 400
    try:
        if "," in photo_data:
            image_data = photo_data.split(",")[1]
        else:
            image_data = photo_data
        image_bytes = base64.b64decode(image_data)
        prompt = "Analyze inventory image"
        if hasattr(gemini_model, "generate_content"):
            analysis = gemini_model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}]).text
        else:
            analysis = "Inventory analysis placeholder"
        return jsonify({"success": True, "analysis": analysis, "provider": "LocalFallback"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# Quick Estimate
@main.route("/quick-estimate")
@login_required
def quick_estimate():
    return render_template("quick_estimate.html")


# Help
@main.route("/help")
@login_required
def help_page():
    return render_template("help.html")