from fastapi import FastAPI
import time
from .email_finder import find_possible_emails
from .email_generator import generate_email
from .email_sender import send_email
from .database import init_db, store_outreach
from .config import GMAIL_USER, GMAIL_PASSWORD

app = FastAPI(title="AI Email Outreach Agent", description="Automated job inquiry email system")

@app.on_event("startup")
def startup_event():
    """Initialize the database on startup."""
    init_db()

@app.get("/outreach")
def perform_outreach(company: str, hr_name: str = None, domain: str = None, emails: str = None):
    """
    Perform outreach to a company.

    Query Parameters:
    - company: Company name (required)
    - hr_name: Recruiter/HR name for personalization (required)
    - domain: Company domain (e.g., company.com) - used to generate emails if emails not provided
    - emails: Comma-separated list of email addresses (e.g., "email1@company.com,email2@company.com")
             If provided, overrides domain-based email generation

    Returns:
        dict: Results of the outreach attempts
    """
    # Determine which emails to use
    if emails:
        # Use provided emails (comma-separated and trimmed)
        email_list = [e.strip() for e in emails.split(',')]
    elif domain:
        # Generate possible emails from domain
        email_list = find_possible_emails(domain)
    else:
        return {"error": "Either 'domain' or 'emails' parameter must be provided"}

    # Generate personalized email
    email_body = generate_email(hr_name, company)
    subject = f"Job Inquiry at {company}"

    results = []
    for email in email_list:
        success = send_email(GMAIL_USER, GMAIL_PASSWORD, email, subject, email_body)
        status = "sent" if success else "failed"
        store_outreach(company, email, status)
        results.append({"email": email, "status": status})
        # Rate limiting: wait 20 seconds between emails to avoid Gmail blocking
        time.sleep(20)

    return {"company": company, "results": results}