import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Email Outreach Agent",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .main-header {
        color: #667eea;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        color: #666;
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #4caf50;
        color: #2e7d32;
        margin-bottom: 20px;
    }
    .error-box {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #f44336;
        color: #c62828;
        margin-bottom: 20px;
    }
    .sent-badge {
        background-color: #4caf50;
        color: white;
        padding: 5px 12px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    .failed-badge {
        background-color: #f44336;
        color: white;
        padding: 5px 12px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.85em;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📧 AI Email Outreach Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Generate personalized outreach emails and send them automatically</div>', unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'loading' not in st.session_state:
    st.session_state.loading = False

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="FastAPI server URL"
    )
    st.divider()
    st.info("ℹ️ Make sure the FastAPI server is running on the configured URL")

# Main form
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Company Information")
    company_name = st.text_input(
        "Company Name",
        placeholder="e.g., Microsoft, Google, Apple",
        help="Name of the company you're reaching out to"
    )
    hr_name = st.text_input(
        "Recruiter/HR Name",
        placeholder="e.g., Satya Nadella",
        help="Name of the recruiter or HR person for personalization"
    )

with col2:
    st.subheader("🎯 Email Mode")
    mode = st.radio(
        "Select email input mode",
        options=["🔍 Auto-Generate from Domain", "✏️ Enter Custom Emails"],
        label_visibility="collapsed"
    )

st.divider()

# Mode-specific inputs
if "Auto-Generate" in mode:
    st.subheader("🔍 Auto-Generate Emails")
    domain = st.text_input(
        "Company Domain",
        placeholder="e.g., microsoft.com",
        help="Will generate: hr@, careers@, jobs@, recruitment@"
    )
    email_input = None
    mode_type = "domain"

else:
    st.subheader("✏️ Custom Email Addresses")
    st.write("Enter email addresses in any of these formats:")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("• john@company.com")
        st.caption("• jane@company.com")
    with col2:
        st.caption("• one per line")
        st.caption("• or comma-separated")
    
    email_input = st.text_area(
        "Email Addresses",
        placeholder="john@company.com\njane@company.com\nrecruiting@company.com",
        height=120,
        help="One email per line or comma-separated"
    )
    domain = None
    mode_type = "emails"

st.divider()

# Submit button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    send_button = st.button(
        "🚀 Send Outreach Emails",
        type="primary",
        use_container_width=True
    )

with col2:
    reset_button = st.button(
        "🔄 Clear Form",
        use_container_width=True
    )

if reset_button:
    st.session_state.results = None
    st.rerun()

# Handle form submission
if send_button:
    # Validation
    errors = []
    
    if not company_name:
        errors.append("Company name is required")
    if not hr_name:
        errors.append("Recruiter/HR name is required")
    
    if mode_type == "domain":
        if not domain:
            errors.append("Company domain is required")
    else:
        if not email_input or not email_input.strip():
            errors.append("At least one email address is required")
        else:
            # Parse emails
            emails_list = [e.strip() for e in email_input.replace('\n', ',').split(',') if e.strip()]
            if not emails_list:
                errors.append("Please enter valid email addresses")
    
    if errors:
        for error in errors:
            st.error(f"❌ {error}")
    else:
        # Prepare API request
        params = {
            "company": company_name,
            "hr_name": hr_name
        }
        
        if mode_type == "domain":
            params["domain"] = domain
        else:
            emails_list = [e.strip() for e in email_input.replace('\n', ',').split(',') if e.strip()]
            params["emails"] = ",".join(emails_list)
        
        # Show progress
        with st.spinner("🔄 Processing your request... (20 seconds per email)"):
            try:
                response = requests.get(
                    f"{api_url}/outreach",
                    params=params,
                    timeout=300
                )
                
                if response.status_code == 200:
                    st.session_state.results = response.json()
                else:
                    st.error(f"❌ API Error: {response.status_code} - {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"❌ Connection Error: Cannot reach API at {api_url}")
                st.info("💡 Make sure the FastAPI server is running: `uvicorn app.main:app --reload`")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

# Display results
if st.session_state.results:
    st.divider()
    st.subheader("📤 Outreach Results")
    
    results_data = st.session_state.results
    company = results_data.get("company", "Unknown")
    result_items = results_data.get("results", [])
    
    # Summary
    sent_count = sum(1 for r in result_items if r["status"] == "sent")
    failed_count = sum(1 for r in result_items if r["status"] == "failed")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Emails", len(result_items))
    with col2:
        st.metric("Sent", sent_count, delta=f"{sent_count}/{len(result_items)}")
    with col3:
        st.metric("Failed", failed_count)
    
    st.divider()
    
    # Results table
    if result_items:
        st.write("**Email Delivery Status:**")
        
        # Create table data
        table_data = []
        for idx, result in enumerate(result_items, 1):
            table_data.append({
                "#": idx,
                "Email": result["email"],
                "Status": "✅ SENT" if result["status"] == "sent" else "❌ FAILED"
            })
        
        # Display as formatted list
        for item in table_data:
            col1, col2, col3 = st.columns([0.5, 2.5, 1])
            with col1:
                st.write(f"**{item['#']}.**")
            with col2:
                st.write(item['Email'])
            with col3:
                if "✅" in item['Status']:
                    st.markdown(f'<span class="sent-badge">{item["Status"]}</span>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<span class="failed-badge">{item["Status"]}</span>', unsafe_allow_html=True)
        
        # Success message
        if sent_count > 0:
            st.success(f"✅ Successfully sent {sent_count} outreach email(s)! Check your Gmail sent folder.")
    
    # Export option
    st.divider()
    if st.button("💾 Export Results as JSON"):
        json_str = json.dumps(st.session_state.results, indent=2)
        st.download_button(
            label="Download JSON",
            data=json_str,
            file_name=f"outreach_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# Footer
st.divider()
st.markdown("""
---
**💡 Tips:**
- Use domain mode for auto-discovering recruiter emails
- Use custom email mode to target specific people you've researched
- Each email is sent with a 20-second delay to avoid spam filters
- All outreach attempts are logged to the database

**🔗 Links:**
- [API Documentation](http://localhost:8000/docs)
- [FastAPI Server](http://localhost:8000)
- [GitHub Repository](https://github.com/your-username/auto-email)
""")
