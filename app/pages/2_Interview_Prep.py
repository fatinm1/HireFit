import streamlit as st
import requests
from typing import Dict, List
import json
import os

# API URL from environment variable
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def generate_interview_questions(resume_analysis: Dict) -> Dict:
    """Generate interview questions based on resume analysis"""
    response = requests.post(f"{API_URL}/generate-interview-questions", json=resume_analysis)
    return response.json()

st.markdown("""
    <div style='text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%); border-radius: 12px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>Interview Preparation</h1>
        <p style='color: rgba(255, 255, 255, 0.9); font-size: 1.1em; margin-top: 0.5rem;'>
            AI-Powered Interview Questions & Practice
        </p>
    </div>
""", unsafe_allow_html=True)

# Check if resume analysis exists in session state
if 'resume_analysis' not in st.session_state:
    st.warning("⚠️ Please analyze your resume first in the Resume Analysis page!")
else:
    # Technical Interview Questions
    st.markdown("""
        <div class='results-section'>
            <h2>🎯 Technical Interview Questions</h2>
            <p style='color: #6c757d; margin-bottom: 1rem;'>
                Practice with AI-generated questions based on your resume
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Generate New Questions"):
        with st.spinner("🔄 Preparing questions..."):
            questions = generate_interview_questions(st.session_state.resume_analysis)
            if questions["status"] == "success":
                st.session_state.interview_questions = questions["questions"]
    
    # Display questions and allow practice
    if 'interview_questions' in st.session_state:
        for i, question in enumerate(st.session_state.interview_questions, 1):
            with st.expander(f"Question {i}: {question}"):
                # User's answer input
                user_answer = st.text_area(
                    "Your Answer",
                    key=f"answer_{i}",
                    height=100,
                    placeholder="Type your answer here..."
                )
                
                # Practice timer
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("Start Practice Timer", key=f"timer_{i}"):
                        st.write("⏱️ 2:00 minutes remaining")
                with col2:
                    if st.button("Record Answer", key=f"record_{i}"):
                        st.success("Answer recorded!")
    
    # Interview Tips
    st.markdown("""
        <div class='results-section'>
            <h2>💡 Interview Tips</h2>
            <p style='color: #6c757d; margin-bottom: 1rem;'>
                Based on your profile and target role
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Common interview tips
    tips = [
        {
            "category": "Technical Skills",
            "tips": [
                "Be prepared to explain your technical projects in detail",
                "Practice coding on a whiteboard",
                "Review your listed skills thoroughly",
                "Prepare examples of problem-solving"
            ]
        },
        {
            "category": "Behavioral Questions",
            "tips": [
                "Use the STAR method (Situation, Task, Action, Result)",
                "Prepare specific examples from your experience",
                "Focus on your role and contributions",
                "Quantify results when possible"
            ]
        },
        {
            "category": "Company Research",
            "tips": [
                "Research the company's products/services",
                "Understand the company's culture and values",
                "Prepare questions for the interviewer",
                "Review recent company news"
            ]
        }
    ]
    
    for category in tips:
        with st.expander(f"📌 {category['category']} Tips"):
            for tip in category["tips"]:
                st.markdown(f"""
                    <div class='info-card' style='border-left-color: #10b981;'>
                        <div style='color: #1a1f36;'>• {tip}</div>
                    </div>
                """, unsafe_allow_html=True)
    
    # Mock Interview Scheduler
    st.markdown("""
        <div class='results-section'>
            <h2>🎥 Mock Interview</h2>
            <p style='color: #6c757d; margin-bottom: 1rem;'>
                Schedule a mock interview with an AI interviewer
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        interview_date = st.date_input("Select Date")
    with col2:
        interview_time = st.time_input("Select Time")
    
    if st.button("Schedule Mock Interview"):
        st.success(f"Mock interview scheduled for {interview_date} at {interview_time}!")
        st.info("You will receive an email with the meeting link and preparation instructions.") 