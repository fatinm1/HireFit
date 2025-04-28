import streamlit as st
import requests
import json
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(
    page_title="HireFit AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with a professional theme
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main page styling */
    .main {
        background-color: #f8f9fa;
        color: #212529;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1 {
        color: #0d6efd;
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    h2, h3 {
        color: #1a1f36;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-family: 'Inter', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(13, 110, 253, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(13, 110, 253, 0.3);
    }
    
    /* Text areas and inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: white;
        color: #1a1f36;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        padding: 12px;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #0d6efd;
        box-shadow: 0 0 0 3px rgba(13, 110, 253, 0.1);
    }
    
    /* File uploader */
    .uploadedFile {
        background-color: white;
        border: 2px dashed #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .uploadedFile:hover {
        border-color: #0d6efd;
        background-color: rgba(13, 110, 253, 0.05);
    }
    
    /* Match score */
    .match-score {
        font-family: 'Inter', sans-serif;
        font-size: 2.5em;
        font-weight: 700;
        color: #0d6efd;
        text-align: center;
        padding: 24px;
        border-radius: 12px;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        margin: 24px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Results sections */
    .results-section {
        background: white;
        padding: 24px;
        border-radius: 12px;
        margin: 16px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .results-section:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Skills tags */
    .skill-tag {
        display: inline-block;
        background: rgba(13, 110, 253, 0.1);
        color: #0d6efd;
        padding: 6px 12px;
        border-radius: 20px;
        margin: 4px;
        font-size: 0.9em;
        font-weight: 500;
    }
    
    /* Experience and Education cards */
    .info-card {
        background: #f8f9fa;
        padding: 16px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 4px solid #0d6efd;
    }
    
    /* Alerts and notifications */
    .alert {
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
        font-weight: 500;
    }
    
    .alert-success {
        background: #d1e7dd;
        color: #0f5132;
        border: 1px solid #badbcc;
    }
    
    .alert-warning {
        background: #fff3cd;
        color: #856404;
        border: 1px solid #ffeeba;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #0d6efd;
    }
    </style>
    """, unsafe_allow_html=True)

# API URL
API_URL = "http://localhost:8000"

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

def main():
    # Modern header with gradient
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%); border-radius: 12px; margin-bottom: 2rem;'>
            <h1 style='color: white; margin: 0;'>HireFit AI</h1>
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
                        
                        # Interview Questions
                        if st.button("Generate Interview Questions"):
                            with st.spinner("🔄 Preparing questions..."):
                                questions = generate_interview_questions(data)
                                if questions["status"] == "success":
                                    st.markdown("""
                                        <div class='results-section'>
                                            <h3>🎯 Technical Interview Questions</h3>
                                        """, unsafe_allow_html=True)
                                    for i, question in enumerate(questions["questions"], 1):
                                        st.markdown(f"""
                                            <div class='info-card' style='border-left-color: #10b981;'>
                                                <div style='font-weight: 500; color: #1a1f36;'>Q{i}. {question}</div>
                                            </div>
                                        """, unsafe_allow_html=True)
                                    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 