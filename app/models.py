from datetime import datetime
from .extensions import db


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(500))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    jobs = db.relationship("Job", backref="customer", lazy=True, cascade="all, delete-orphan")
    inventory_items = db.relationship("InventoryItem", backref="owner", lazy=True, cascade="all, delete-orphan")


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    scheduled_date = db.Column(db.Date)
    status = db.Column(db.String(50), default="scheduled")
    total_cost = db.Column(db.Float, default=0.0)
    ai_estimate = db.Column(db.Text)
    notes = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    materials_used = db.relationship("JobMaterial", backref="job", lazy=True, cascade="all, delete-orphan")
    photos = db.relationship("JobPhoto", backref="job", lazy=True, cascade="all, delete-orphan")


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(50))
    unit_cost = db.Column(db.Float)
    supplier = db.Column(db.String(200))
    notes = db.Column(db.Text)


class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Float, default=0)
    unit = db.Column(db.String(50))
    unit_cost = db.Column(db.Float)
    location = db.Column(db.String(200))
    low_stock_alert = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=True)


class InventoryAudit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'))
    action = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer)


class JobMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("material.id"))
    name = db.Column(db.String(200))
    quantity = db.Column(db.Float)
    unit_cost = db.Column(db.Float)
    total_cost = db.Column(db.Float)


class JobPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    photo_data = db.Column(db.Text)
    caption = db.Column(db.String(500))
    ai_analysis = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
