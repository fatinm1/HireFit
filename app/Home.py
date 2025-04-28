import streamlit as st
import os

# Configure the page
st.set_page_config(
    page_title="HireFit AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get backend URL from environment variable
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

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
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        margin: 16px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        border-left: 4px solid #0d6efd;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Stats */
    .stat-card {
        background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
        color: white;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        margin: 16px 0;
    }
    
    .stat-number {
        font-size: 2.5em;
        font-weight: 700;
        margin: 8px 0;
    }
    
    .stat-label {
        font-size: 0.9em;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div style='text-align: center; padding: 3rem 0; background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%); border-radius: 12px; margin-bottom: 2rem;'>
        <h1 style='color: white; font-size: 3em; margin: 0;'>HireFit AI</h1>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.2em; margin-top: 1rem; margin-bottom: 2rem;'>
            Your AI-Powered Career Assistant
        </p>
        <div style='display: flex; justify-content: center; gap: 1rem;'>
            <a href='?page=Resume_Analysis' style='text-decoration: none;'>
                <button style='background: white; color: #0d6efd; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 500; cursor: pointer;'>
                    Get Started
                </button>
            </a>
            <a href='#features' style='text-decoration: none;'>
                <button style='background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid white; padding: 12px 24px; border-radius: 8px; font-weight: 500; cursor: pointer;'>
                    Learn More
                </button>
            </a>
        </div>
    </div>
""", unsafe_allow_html=True)

# Stats Section
st.markdown("<div id='stats'>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>98%</div>
            <div class='stat-label'>Accuracy Rate</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>5K+</div>
            <div class='stat-label'>Resumes Analyzed</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>1K+</div>
            <div class='stat-label'>Job Matches</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>24/7</div>
            <div class='stat-label'>AI Support</div>
        </div>
    """, unsafe_allow_html=True)

# Features Section
st.markdown("<div id='features'>", unsafe_allow_html=True)
st.markdown("""
    <h2 style='text-align: center; margin: 3rem 0;'>Key Features</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class='feature-card'>
            <h3>📄 Resume Analysis</h3>
            <p>Advanced AI-powered resume analysis that provides detailed insights into your skills, experience, and potential improvements.</p>
            <ul>
                <li>Skill extraction and categorization</li>
                <li>Experience evaluation</li>
                <li>Education assessment</li>
                <li>Improvement suggestions</li>
            </ul>
        </div>
        
        <div class='feature-card'>
            <h3>🎯 Interview Preparation</h3>
            <p>Comprehensive interview preparation tools to help you succeed in your next interview.</p>
            <ul>
                <li>AI-generated interview questions</li>
                <li>Practice sessions with feedback</li>
                <li>Common interview tips</li>
                <li>Mock interview scheduling</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='feature-card'>
            <h3>💼 Job Search</h3>
            <p>Smart job search and tracking system to manage your job applications effectively.</p>
            <ul>
                <li>Personalized job recommendations</li>
                <li>Application tracking</li>
                <li>Status updates</li>
                <li>Progress analytics</li>
            </ul>
        </div>
        
        <div class='feature-card'>
            <h3>📊 Analytics Dashboard</h3>
            <p>Detailed analytics and insights about your job search progress and performance.</p>
            <ul>
                <li>Application statistics</li>
                <li>Interview success rate</li>
                <li>Skill gap analysis</li>
                <li>Improvement tracking</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Getting Started Section
st.markdown("""
    <h2 style='text-align: center; margin: 3rem 0;'>Getting Started</h2>
""", unsafe_allow_html=True)

st.markdown("""
    <div class='feature-card' style='text-align: center;'>
        <h3>3 Simple Steps</h3>
        <div style='display: flex; justify-content: space-around; margin: 2rem 0;'>
            <div>
                <div style='font-size: 2em; color: #0d6efd; margin-bottom: 1rem;'>1</div>
                <div style='font-weight: 500; margin-bottom: 0.5rem;'>Upload Resume</div>
                <div style='color: #6c757d;'>Upload your resume in PDF or DOCX format</div>
            </div>
            <div>
                <div style='font-size: 2em; color: #0d6efd; margin-bottom: 1rem;'>2</div>
                <div style='font-weight: 500; margin-bottom: 0.5rem;'>Get Analysis</div>
                <div style='color: #6c757d;'>Receive detailed insights and suggestions</div>
            </div>
            <div>
                <div style='font-size: 2em; color: #0d6efd; margin-bottom: 1rem;'>3</div>
                <div style='font-weight: 500; margin-bottom: 0.5rem;'>Start Applying</div>
                <div style='color: #6c757d;'>Apply to matching jobs with confidence</div>
            </div>
        </div>
        <a href='?page=Resume_Analysis' style='text-decoration: none;'>
            <button style='background: #0d6efd; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 500; cursor: pointer;'>
                Start Now
            </button>
        </a>
    </div>
""", unsafe_allow_html=True) 