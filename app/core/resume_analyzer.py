from typing import Dict, List, Optional
import PyPDF2
from docx import Document
import os
from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import json
import requests
from pathlib import Path
import re
import logging
import traceback

# Configure logging with more detail
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ResumeAnalyzer:
    def __init__(self):
        logger.info("Initializing ResumeAnalyzer...")
        try:
            # Initialize model configuration
            model_path = "models"
            model_file = "mistral-7b-instruct-v0.1.Q4_K_M.gguf"
            full_path = os.path.join(model_path, model_file)

            # Create models directory if it doesn't exist
            os.makedirs(model_path, exist_ok=True)

            # Download model if it doesn't exist
            if not os.path.exists(full_path):
                logger.info("Downloading Mistral model... This might take a few minutes...")
                self._download_model(model_file, full_path)

            # Initialize the model with optimized settings for performance
            logger.info("Loading the model...")
            self.llm = CTransformers(
                model=full_path,
                model_type="mistral",
                config={
                    'max_new_tokens': 256,  # Reduced for faster responses
                    'temperature': 0.1,
                    'context_length': 1024,  # Balanced for performance
                    'gpu_layers': 0,
                    'threads': max(4, os.cpu_count() - 2) if os.cpu_count() else 4,  # Optimize thread count
                    'batch_size': 8,  # Increased for better throughput
                    'top_k': 30,  # Added for faster sampling
                    'top_p': 0.1  # Added for focused sampling
                }
            )
            logger.info("Model loaded successfully")
            self._setup_prompts()
        except Exception as e:
            logger.error(f"Error initializing ResumeAnalyzer: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    def _setup_prompts(self):
        """Initialize prompt templates for different analysis tasks"""
        self.skill_extraction_prompt = PromptTemplate(
            input_variables=["resume_text"],
            template="""<s>[INST] Extract key information from this resume section. Be brief and specific.

Text: {resume_text}

Format the output as JSON:
{{
    "skills": ["skill1", "skill2"],
    "experience": ["job1", "job2"],
    "education": ["edu1", "edu2"]
}}
[/INST]</s>"""
        )

        self.summary_prompt = PromptTemplate(
            input_variables=["previous_results", "current_section"],
            template="""<s>[INST] Combine and summarize these resume sections. Remove duplicates and maintain the most relevant information.

Previous Results: {previous_results}
Current Section: {current_section}

Format as JSON:
{{
    "skills": ["skill1", "skill2"],
    "experience": ["most_recent_job1", "job2"],
    "education": ["education1", "education2"]
}}
[/INST]</s>"""
        )

        self.match_analysis_prompt = PromptTemplate(
            input_variables=["resume_text", "job_description"],
            template="""<s>[INST] Analyze how well the candidate's profile matches the job requirements. Consider both skills and experience.

Resume Information:
{resume_text}

Job Description:
{job_description}

Provide a detailed analysis in JSON format. The match_score should be between 0.0 and 1.0, where:
- 0.8-1.0: Excellent match (90%+ requirements met)
- 0.6-0.79: Good match (70-89% requirements met)
- 0.4-0.59: Fair match (50-69% requirements met)
- Below 0.4: Poor match (less than 50% requirements met)

Format as JSON:
{{
    "match_score": 0.XX,
    "skill_gaps": ["missing_skill1", "missing_skill2"],
    "suggestions": ["specific_improvement1", "specific_improvement2"],
    "matching_skills": ["matching_skill1", "matching_skill2"],
    "relevant_experience": ["relevant_exp1", "relevant_exp2"]
}}
[/INST]</s>"""
        )

    def _chunk_text(self, text: str, max_chunk_size: int = 800) -> List[str]:
        """Split text into chunks while preserving semantic boundaries"""
        # First, clean and normalize the text
        text = re.sub(r'\s+', ' ', text).strip()  # Remove excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)    # Normalize multiple newlines
        
        # Split on common resume section headers
        section_patterns = [
            r'EDUCATION|ACADEMIC|QUALIFICATION',
            r'EXPERIENCE|EMPLOYMENT|WORK HISTORY',
            r'SKILLS|EXPERTISE|COMPETENCIES',
            r'PROJECTS|ACHIEVEMENTS',
            r'CERTIFICATIONS|CERTIFICATES',
            r'LANGUAGES|INTERESTS'
        ]
        pattern = f"({('|'.join(section_patterns))})"
        sections = re.split(f"(?i){pattern}", text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        
        for section in sections:
            section = section.strip()
            if not section:
                continue
                
            section_size = len(section.split())
            
            if current_size + section_size > max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [section]
                current_size = section_size
            else:
                current_chunk.append(section)
                current_size += section_size
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        # Ensure we don't have empty chunks
        chunks = [chunk for chunk in chunks if chunk.strip()]
        
        return chunks

    def _merge_results(self, results: List[Dict]) -> Dict:
        """Merge multiple analysis results, removing duplicates and keeping most relevant info"""
        if not results:
            return {
                "skills": [],
                "experience": [],
                "education": []
            }

        merged = results[0]
        if len(results) == 1:
            return merged

        # For multiple chunks, use the summary prompt to combine them
        summary_chain = LLMChain(llm=self.llm, prompt=self.summary_prompt)
        
        for next_result in results[1:]:
            try:
                response = summary_chain.invoke({
                    "previous_results": json.dumps(merged),
                    "current_section": json.dumps(next_result)
                })
                
                if isinstance(response, dict) and 'text' in response:
                    response_text = response['text']
                else:
                    response_text = str(response)
                
                merged = self._parse_llm_response(response_text)
                if not merged:
                    merged = next_result
            except Exception as e:
                logger.error(f"Error merging results: {str(e)}")
                logger.error(traceback.format_exc())
        
        return merged

    def analyze_resume(self, resume_text: str, job_description: Optional[str] = None) -> Dict:
        """Analyze resume and return structured data"""
        try:
            logger.info("Starting resume analysis")
            
            # Clean the resume text
            resume_text = re.sub(r'\s+', ' ', resume_text).strip()
            
            # Split resume into chunks
            chunks = self._chunk_text(resume_text)
            logger.info(f"Split resume into {len(chunks)} chunks")
            
            # Process each chunk with timeout
            chunk_results = []
            skill_chain = LLMChain(llm=self.llm, prompt=self.skill_extraction_prompt)
            
            for i, chunk in enumerate(chunks, 1):
                try:
                    logger.info(f"Processing chunk {i}/{len(chunks)}")
                    response = skill_chain.invoke({"resume_text": chunk})
                    
                    if isinstance(response, dict) and 'text' in response:
                        response_text = response['text']
                    else:
                        response_text = str(response)
                    
                    chunk_result = self._parse_llm_response(response_text)
                    if chunk_result:
                        # Remove duplicates within the chunk
                        for key in ['skills', 'experience', 'education']:
                            if key in chunk_result:
                                chunk_result[key] = list(dict.fromkeys(chunk_result[key]))
                        chunk_results.append(chunk_result)
                        logger.info(f"Successfully processed chunk {i}")
                except Exception as e:
                    logger.error(f"Error processing chunk {i}: {str(e)}")
                    continue
            
            # Merge results from all chunks
            basic_info = self._merge_results(chunk_results)
            if not basic_info:
                basic_info = {
                    "skills": [],
                    "experience": [],
                    "education": []
                }
            
            # Process job description if provided
            match_analysis = None
            if job_description:
                try:
                    logger.info("Starting job description analysis")
                    match_chain = LLMChain(llm=self.llm, prompt=self.match_analysis_prompt)
                    
                    # Prepare comprehensive resume summary
                    resume_summary = {
                        "skills": basic_info.get("skills", []),
                        "experience": basic_info.get("experience", []),
                        "education": basic_info.get("education", [])
                    }
                    
                    # Clean and format job description
                    job_desc_clean = re.sub(r'\s+', ' ', job_description).strip()
                    
                    match_response = match_chain.invoke({
                        "resume_text": json.dumps(resume_summary),
                        "job_description": job_desc_clean
                    })
                    
                    if isinstance(match_response, dict) and 'text' in match_response:
                        match_text = match_response['text']
                    else:
                        match_text = str(match_response)
                    
                    match_analysis = self._parse_llm_response(match_text)
                    if match_analysis:
                        # Ensure match_score is a float between 0 and 1
                        try:
                            match_score = float(match_analysis.get("match_score", 0.0))
                            match_score = max(0.0, min(1.0, match_score))  # Clamp between 0 and 1
                        except (ValueError, TypeError):
                            match_score = 0.0
                            
                        match_analysis = {
                            "match_score": match_score,
                            "skill_gaps": match_analysis.get("skill_gaps", [])[:5],
                            "suggestions": match_analysis.get("suggestions", [])[:3],
                            "matching_skills": match_analysis.get("matching_skills", [])[:5],
                            "relevant_experience": match_analysis.get("relevant_experience", [])[:3]
                        }
                    logger.info(f"Job description analysis completed with match score: {match_analysis.get('match_score', 0.0)}")
                except Exception as e:
                    logger.error(f"Error in job matching: {str(e)}")
                    logger.error(traceback.format_exc())
                    match_analysis = {
                        "match_score": 0.0,
                        "skill_gaps": [],
                        "suggestions": [],
                        "matching_skills": [],
                        "relevant_experience": []
                    }
            
            logger.info("Resume analysis completed successfully")
            return {
                "basic_info": basic_info,
                "match_analysis": match_analysis if match_analysis is not None else {
                    "match_score": 0.0,
                    "skill_gaps": [],
                    "suggestions": [],
                    "matching_skills": [],
                    "relevant_experience": []
                }
            }
            
        except Exception as e:
            logger.error(f"Error in analyze_resume: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "basic_info": {
                    "skills": [],
                    "experience": [],
                    "education": []
                },
                "match_analysis": {
                    "match_score": 0.0,
                    "skill_gaps": [],
                    "suggestions": [],
                    "matching_skills": [],
                    "relevant_experience": []
                }
            }

    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response and ensure it's a valid JSON"""
        try:
            logger.debug(f"Parsing response: {response}")
            # Find JSON content between curly braces
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)
                logger.debug(f"Parsed result: {result}")
                return result
            logger.error("No valid JSON found in response")
            return {}
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            logger.error(traceback.format_exc())
            return {}

    def _download_model(self, model_file: str, full_path: str):
        """Download the Mistral model"""
        url = f"https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/{model_file}"
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("Model downloaded successfully!")
        except Exception as e:
            print(f"Error downloading model: {str(e)}")
            raise

    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        if file_path.endswith('.pdf'):
            return self._extract_text_from_pdf(file_path)
        elif file_path.endswith('.docx'):
            return self._extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text.strip()
        except Exception as e:
            print(f"Error extracting PDF text: {str(e)}")
            return ""

    def _extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs]).strip()
        except Exception as e:
            print(f"Error extracting DOCX text: {str(e)}")
            return ""

    def generate_interview_questions(self, resume_analysis: Dict) -> List[str]:
        """Generate interview questions based on resume analysis"""
        try:
            question_chain = LLMChain(llm=self.llm, prompt=self.interview_questions_prompt)
            response = question_chain.invoke({"resume_analysis": json.dumps(resume_analysis)})
            result = self._parse_llm_response(response)
            return result.get("questions", [])
        except Exception as e:
            print(f"Error generating interview questions: {str(e)}")
            return []

    def calculate_match_score(self, resume_text: str, job_description: str) -> float:
        """Calculate match score between resume and job description"""
        try:
            # Use only the first chunk to stay within context limits
            chunk = self._chunk_text(resume_text)[0]
            match_chain = LLMChain(llm=self.llm, prompt=self.match_analysis_prompt)
            response = match_chain.invoke({
                "resume_text": chunk,
                "job_description": job_description
            })
            result = self._parse_llm_response(response)
            return float(result.get("match_score", 0.0))
        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            return 0.0 