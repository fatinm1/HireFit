import streamlit as st
import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API URL from environment variable
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def analyze_resume(file: Any, job_description: str = None) -> Dict:
    """Send resume to backend for analysis"""
    files = {"file": file}
    data = {"job_description": job_description} if job_description else {}
    response = requests.post(f"{API_URL}/analyze-resume", files=files, data=data)
    return response.json()

def generate_interview_questions(resume_analysis: Dict) -> Dict:
    """Generate interview questions based on resume analysis"""
    response = requests.post(f"{API_URL}/generate-interview-questions", json=resume_analysis)
    return response.json()

st.markdown("""
    <div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%); border-radius: 12px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>Resume Analysis</h1>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.1em; margin-top: 0.5rem;'>
            AI-Powered Resume Analysis & Job Matching
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns with better spacing
col1, spacer, col2 = st.columns([5, 0.5, 6])

with col1:
    st.markdown("""
        <div class='results-section'>
            <h2>📤 Upload Resume</h2>
            <p style='color: #6c757d; margin-bottom: 1rem;'>
                Upload your resume in PDF or DOCX format
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "",  # Empty label for cleaner look
        type=["pdf", "docx"],
        help="Supported formats: PDF, DOCX | Max size: 200MB"
    )
    
    st.markdown("""
        <div class='results-section'>
            <h2>💼 Job Description</h2>
            <p style='color: #6c757d; margin-bottom: 1rem;'>
                Add a job description for better matching
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    job_description = st.text_area(
        "",  # Empty label for cleaner look
        height=200,
        placeholder="Paste the job description here..."
    )

with col2:
    if uploaded_file:
        st.markdown("""
            <div class='results-section'>
                <h2>🔍 Analysis Dashboard</h2>
                <p style='color: #6c757d; margin-bottom: 1rem;'>
                    Click analyze to start the AI-powered resume analysis
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("Analyze Resume"):
            with st.spinner("🔄 Processing your resume..."):
                result = analyze_resume(uploaded_file, job_description)
                
                if result["status"] == "success":
                    data = result["data"]
                    
                    # Match Score with animation
                    score = data['match_score'] * 100
                    color = (
                        "#10b981" if score >= 80 else
                        "#0d6efd" if score >= 60 else
                        "#fb923c" if score >= 40 else
                        "#ef4444"
                    )
                    st.markdown(
                        f"""
                        <div class='match-score' style='color: {color};'>
                            <div style='font-size: 0.6em; color: #6c757d; margin-bottom: 0.5rem;'>Match Score</div>
                            {score:.1f}%
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Save analysis to session state for other pages
                    st.session_state['resume_analysis'] = data
                    
                    # Skills as tags
                    st.markdown("""
                        <div class='results-section'>
                            <h3>⚙ Technical Skills</h3>
                        """, unsafe_allow_html=True)
                    skills_html = "".join([f"<span class='skill-tag'>{skill}</span>" for skill in data['skills']])
                    st.markdown(f"<div style='margin: 1rem 0;'>{skills_html}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Experience as cards
                    st.markdown("""
                        <div class='results-section'>
                            <h3>💻 Experience</h3>
                        """, unsafe_allow_html=True)
                    for exp in data["experience"]:
                        st.markdown(f"""
                            <div class='info-card'>
                                <div style='color: #1a1f36;'>{exp}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Education as cards
                    st.markdown("""
                        <div class='results-section'>
                            <h3>🎓 Education</h3>
                        """, unsafe_allow_html=True)
                    for edu in data["education"]:
                        st.markdown(f"""
                            <div class='info-card'>
                                <div style='color: #1a1f36;'>{edu}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Skill Gaps and Suggestions in a grid
                    col_gap, col_sugg = st.columns(2)
                    
                    with col_gap:
                        st.markdown("""
                            <div class='results-section'>
                                <h3>⚠ Skill Gaps</h3>
                            """, unsafe_allow_html=True)
                        for gap in data["skill_gaps"]:
                            st.markdown(f"""
                                <div class='alert alert-warning'>
                                    {gap}
                                </div>
                            """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with col_sugg:
                        st.markdown("""
                            <div class='results-section'>
                                <h3>💡 Suggestions</h3>
                            """, unsafe_allow_html=True)
                        for sugg in data["improvement_suggestions"]:
                            st.markdown(f"""
                                <div class='alert alert-success'>
                                    {sugg}
                                </div>
                            """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True) 