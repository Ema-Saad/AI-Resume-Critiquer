## AI Resume Critiquer
A Streamlit-based web application that analyzes resumes (PDF or TXT) and provides AI-powered feedback using the Google Gemini API. The app offers constructive feedback on content clarity, skills presentation, experience descriptions, and alignment with a specified job role.

**Features**
Upload resumes in PDF or TXT format.
Optional input for a target job role to tailor feedback.
AI-driven analysis powered by Google Gemini API.
Structured feedback displayed in a user-friendly Streamlit interface.
Managed with uv for fast and reliable dependency management.

**Prerequisites**
Python: Version 3.8 or higher.
uv: Modern Python package and project manager.
Google Gemini API Key: Obtain from Google AI Studio.
A .env file with your API key (see Setup).

**Dependencies**
streamlit: Web app framework
PyPDF2: PDF text extraction
requests: HTTP requests for Gemini API
python-dotenv: Environment variable management
Defined in pyproject.toml