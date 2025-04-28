from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional
from dotenv import load_dotenv
from app.core.resume_analyzer import ResumeAnalyzer
from app.utils.file_processor import FileProcessor
from app.utils.text_processor import TextProcessor

# Load environment variables
load_dotenv()

app = FastAPI(title="HireFit AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
resume_analyzer = ResumeAnalyzer()
text_processor = TextProcessor()

class ResumeAnalysis(BaseModel):
    skills: List[str]
    experience: List[str]
    education: List[str]
    match_score: float
    skill_gaps: List[str]
    improvement_suggestions: List[str]

class JobDescription(BaseModel):
    title: str
    description: str
    required_skills: List[str]
    preferred_skills: List[str]

@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...), job_description: Optional[str] = None):
    """
    Analyze a resume and provide insights
    """
    try:
        # Save uploaded file
        temp_file_path = await FileProcessor.save_upload_file(file)
        if not temp_file_path:
            raise HTTPException(status_code=400, detail="Failed to process uploaded file")

        try:
            # Extract text from resume
            resume_text = resume_analyzer.extract_text_from_file(temp_file_path)
            if not resume_text:
                raise HTTPException(status_code=400, detail="Could not extract text from the file")
            
            # Clean the text
            resume_text = text_processor.clean_text(resume_text)
            
            # Analyze resume
            analysis_result = resume_analyzer.analyze_resume(resume_text, job_description)
            
            if not analysis_result or not isinstance(analysis_result, dict):
                raise HTTPException(status_code=500, detail="Failed to analyze resume")
            
            # Extract the analysis results
            basic_info = analysis_result.get("basic_info", {})
            match_analysis = analysis_result.get("match_analysis", {})
            
            # Prepare response
            response_data = {
                "skills": basic_info.get("skills", []),
                "experience": basic_info.get("experience", []),
                "education": basic_info.get("education", []),
                "match_score": match_analysis.get("match_score", 0.0),
                "skill_gaps": match_analysis.get("skill_gaps", []),
                "improvement_suggestions": match_analysis.get("suggestions", [])
            }

            return {
                "status": "success",
                "message": "Resume analysis completed",
                "data": response_data
            }

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
        finally:
            # Clean up temporary file
            FileProcessor.cleanup_file(temp_file_path)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/generate-interview-questions")
async def generate_interview_questions(resume_analysis: ResumeAnalysis):
    """
    Generate interview questions based on resume analysis
    """
    try:
        questions = resume_analyzer.generate_interview_questions(resume_analysis.dict())
        questions_data = text_processor.extract_json_from_text(questions)
        
        return {
            "status": "success",
            "questions": questions_data.get("questions", [])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate-match-score")
async def calculate_match_score(resume_analysis: ResumeAnalysis, job_description: JobDescription):
    """
    Calculate match score between resume and job description
    """
    try:
        # Convert job description to text
        job_text = f"{job_description.title}\n{job_description.description}\n"
        job_text += "Required Skills: " + ", ".join(job_description.required_skills)
        job_text += "\nPreferred Skills: " + ", ".join(job_description.preferred_skills)
        
        # Calculate match score
        match_score = resume_analyzer.calculate_match_score(
            "\n".join(resume_analysis.experience + resume_analysis.skills),
            job_text
        )
        
        return {
            "status": "success",
            "match_score": match_score,
            "skill_gaps": [skill for skill in job_description.required_skills 
                         if skill.lower() not in [s.lower() for s in resume_analysis.skills]],
            "suggestions": [f"Consider learning {skill}" for skill in job_description.required_skills 
                          if skill.lower() not in [s.lower() for s in resume_analysis.skills]]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 