import streamlit as st
import requests
from typing import Dict, List
import json
from datetime import datetime
import os

# API URL from environment variable
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.markdown("""
    <div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%); border-radius: 12px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>Job Search</h1>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.1em; margin-top: 0.5rem;'>
            Find and Track Job Opportunities
        </p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state for job tracking
if 'tracked_jobs' not in st.session_state:
    st.session_state.tracked_jobs = []

# Job Search Section
st.markdown("""
    <div class='results-section'>
        <h2>🔍 Find Jobs</h2>
        <p style='color: #6c757d; margin-bottom: 1rem;'>
            Search and filter job opportunities
        </p>
    </div>
""", unsafe_allow_html=True)

# Search filters
col1, col2, col3 = st.columns(3)
with col1:
    job_title = st.text_input("Job Title", placeholder="e.g., Software Engineer")
with col2:
    location = st.text_input("Location", placeholder="e.g., New York, NY")
with col3:
    experience_level = st.selectbox(
        "Experience Level",
        ["Entry Level", "Mid Level", "Senior", "Lead", "Manager"]
    )

# Additional filters
col1, col2 = st.columns(2)
with col1:
    employment_type = st.multiselect(
        "Employment Type",
        ["Full-time", "Part-time", "Contract", "Remote"]
    )
with col2:
    salary_range = st.select_slider(
        "Salary Range (K USD)",
        options=[50, 75, 100, 125, 150, 175, 200, 225, 250],
        value=(75, 150)
    )

if st.button("Search Jobs"):
    # Simulated job results
    example_jobs = [
        {
            "title": "Senior Software Engineer",
            "company": "Tech Corp",
            "location": "New York, NY",
            "salary": "$120K - $180K",
            "description": "Looking for an experienced software engineer...",
            "requirements": ["Python", "React", "AWS", "5+ years experience"],
            "match_score": 85
        },
        {
            "title": "Full Stack Developer",
            "company": "StartUp Inc",
            "location": "Remote",
            "salary": "$100K - $140K",
            "description": "Join our fast-growing team...",
            "requirements": ["JavaScript", "Node.js", "MongoDB", "3+ years experience"],
            "match_score": 75
        }
    ]
    
    for job in example_jobs:
        with st.container():
            st.markdown(f"""
                <div class='results-section' style='position: relative;'>
                    <div style='position: absolute; top: 20px; right: 20px; background: rgba(13, 110, 253, 0.1); padding: 8px 16px; border-radius: 20px;'>
                        <span style='color: #0d6efd; font-weight: 500;'>{job['match_score']}% Match</span>
                    </div>
                    <h3>{job['title']}</h3>
                    <p style='color: #6c757d; margin-bottom: 0.5rem;'>{job['company']} • {job['location']}</p>
                    <p style='color: #10b981; font-weight: 500; margin-bottom: 1rem;'>{job['salary']}</p>
                    <p style='margin-bottom: 1rem;'>{job['description']}</p>
                    <div style='margin-bottom: 1rem;'>
                        {' '.join([f"<span class='skill-tag'>{req}</span>" for req in job['requirements']])}
                    </div>
                    <button class='stButton' onclick='null' style='background: #0d6efd; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;'>Apply Now</button>
                </div>
            """, unsafe_allow_html=True)

# Job Application Tracker
st.markdown("""
    <div class='results-section'>
        <h2>📋 Application Tracker</h2>
        <p style='color: #6c757d; margin-bottom: 1rem;'>
            Track your job applications and their status
        </p>
    </div>
""", unsafe_allow_html=True)

# Add New Application
with st.expander("➕ Add New Application"):
    col1, col2 = st.columns(2)
    with col1:
        new_company = st.text_input("Company Name")
        new_position = st.text_input("Position")
    with col2:
        new_date = st.date_input("Application Date")
        new_status = st.selectbox(
            "Status",
            ["Applied", "Phone Screen", "Interview", "Offer", "Rejected"]
        )
    
    if st.button("Add Application"):
        new_job = {
            "company": new_company,
            "position": new_position,
            "date": new_date.strftime("%Y-%m-%d"),
            "status": new_status,
            "notes": ""
        }
        st.session_state.tracked_jobs.append(new_job)
        st.success("Application added successfully!")

# Display Tracked Applications
if st.session_state.tracked_jobs:
    # Status counts for metrics
    status_counts = {
        "Applied": 0,
        "Interview": 0,
        "Offer": 0
    }
    for job in st.session_state.tracked_jobs:
        if job["status"] in status_counts:
            status_counts[job["status"]] += 1
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Applications", len(st.session_state.tracked_jobs))
    with col2:
        st.metric("Active Interviews", status_counts["Interview"])
    with col3:
        st.metric("Offers", status_counts["Offer"])
    
    # Applications table
    for job in st.session_state.tracked_jobs:
        status_color = {
            "Applied": "#6c757d",
            "Phone Screen": "#0d6efd",
            "Interview": "#fb923c",
            "Offer": "#10b981",
            "Rejected": "#ef4444"
        }
        
        st.markdown(f"""
            <div class='info-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h4 style='margin: 0; color: #1a1f36;'>{job['position']}</h4>
                        <p style='margin: 4px 0; color: #6c757d;'>{job['company']}</p>
                        <p style='margin: 0; color: #6c757d; font-size: 0.9em;'>Applied: {job['date']}</p>
                    </div>
                    <div style='background: {status_color.get(job["status"], "#6c757d")}1a; padding: 8px 16px; border-radius: 20px;'>
                        <span style='color: {status_color.get(job["status"], "#6c757d")}; font-weight: 500;'>{job['status']}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Job Search Tips
with st.expander("💡 Job Search Tips"):
    tips = [
        "Customize your resume for each application",
        "Follow up after applying",
        "Research the company before interviews",
        "Keep your skills section updated",
        "Network on professional platforms"
    ]
    for tip in tips:
        st.markdown(f"""
            <div class='info-card' style='border-left-color: #10b981;'>
                <div style='color: #1a1f36;'>• {tip}</div>
            </div>
        """, unsafe_allow_html=True) 