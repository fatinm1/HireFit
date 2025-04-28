# HireFit AI

An AI-powered career assistant that helps job seekers with resume analysis, interview preparation, and job search tracking.

## Features

- **Resume Analysis**: AI-powered resume analysis with detailed insights
- **Interview Preparation**: Practice with AI-generated interview questions
- **Job Search**: Smart job search and application tracking
- **Analytics Dashboard**: Track your job search progress

## Tech Stack

- Backend: FastAPI
- Frontend: Streamlit
- AI Model: Mistral 7B
- Database: SQLite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HireFit.git
cd HireFit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn app.main:app --reload
```

4. In a new terminal, start the frontend:
```bash
streamlit run app/Home.py
```

## Project Structure

```
HireFit/
├── app/
│   ├── core/           # Core business logic
│   ├── pages/          # Streamlit pages
│   ├── main.py         # FastAPI backend
│   └── Home.py         # Streamlit frontend
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Usage

1. Open your browser and navigate to `http://localhost:8501` for the frontend
2. Upload your resume (PDF or DOCX format)
3. Get AI-powered analysis and suggestions
4. Track your job applications and prepare for interviews

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 