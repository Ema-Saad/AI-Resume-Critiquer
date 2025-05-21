## AI Resume Critiquer
A Streamlit-based web application that analyzes resumes (PDF or TXT) and provides AI-powered feedback using the Google Gemini API. The app offers constructive feedback on content clarity, skills presentation, experience descriptions, and alignment with a specified job role.

### Features
1- Upload resumes in PDF or TXT format.<br>
2- Optional input for a target job role to tailor feedback.<br>
3- AI-driven analysis powered by Google Gemini API.<br>
6- Structured feedback displayed in a user-friendly Streamlit interface.<br>
5- Managed with uv for fast and reliable dependency management.<br>

### Prerequisites
Python: Version 3.8 or higher.<br>
uv: Modern Python package and project manager.<br>
Google Gemini API Key: Obtain from Google AI Studio.<br>
A .env file with your API key (see Setup).<br>

### Dependencies
-streamlit: Web app framework<br>
-PyPDF2: PDF text extraction<br>
-requests: HTTP requests for Gemini API<br>
-python-dotenv: Environment variable management<br>
-Defined in pyproject.toml<br>
