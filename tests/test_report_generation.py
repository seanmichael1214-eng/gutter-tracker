import pytest
from datetime import date, timedelta
from flask import url_for
from app.models import Job, Customer
from app.extensions import db

def test_download_today_report_with_job(client, app):
    """
    Test downloading the daily report when there is a job scheduled for today.
    """
    with app.app_context():
        # Create a customer
        customer = Customer(name="Test Customer", address="123 Test St")
        db.session.add(customer)
        db.session.commit()

        # Create a job for today
        today = date.today()
        job = Job(
            title="Test Job for Today",
            customer_id=customer.id,
            scheduled_date=today,
            status="scheduled",
            total_cost=150.00,
            description="A test job."
        )
        db.session.add(job)
        db.session.commit()

        # Log in
        client.post('/login', data={'password': 'NAO$'})

        # Make request to download report
        response = client.get('/reports/download_today')

        # Assertions
        assert response.status_code == 200
        assert response.mimetype == 'text/plain'
        assert 'attachment; filename=' in response.headers['Content-Disposition']
        
        report_content = response.data.decode('utf-8')
        assert "End of Shift Report" in report_content
        assert "Test Job for Today" in report_content
        assert "Test Customer" in report_content
        assert "123 Test St" in report_content
        assert "scheduled" in report_content
        assert "$150.00" in report_content

def test_download_today_report_no_jobs(client, app):
    """
    Test downloading the daily report when there are no jobs scheduled for today.
    """
    with app.app_context():
        # Ensure no jobs for today
        today = date.today()
        Job.query.filter_by(scheduled_date=today).delete()
        db.session.commit()
        
        # Log in
        client.post('/login', data={'password': 'NAO$'})

        # Make request to download report
        response = client.get('/reports/download_today')

        # Assertions
        assert response.status_code == 200
        assert response.mimetype == 'text/plain'
        
        report_content = response.data.decode('utf-8')
        assert "No jobs scheduled for today" in report_content
