import streamlit as st
import PyPDF2
import io
import os
import requests
import time
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit configuration
st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")
st.title("AI Resume Critiquer")
st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")

# Get Gemini API key
GEMINI_API_KEY = os.getenv("API_KEY")

# Initialize session state for metrics
if 'metrics' not in st.session_state:
    st.session_state.metrics = {
        'total_analyses': 0,
        'job_role_counts': {},
        'api_response_times': [],
        'successful_analyses': 0,
        'failed_analyses': 0
    }

# Load metrics from file (if exists)
METRICS_FILE = 'metrics.json'
if os.path.exists(METRICS_FILE):
    with open(METRICS_FILE, 'r') as f:
        st.session_state.metrics = json.load(f)

# File uploader and job role input
uploaded_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targeting (optional)")
analyze = st.button("Analyze Resume")

# Function to save metrics to file
def save_metrics():
    with open(METRICS_FILE, 'w') as f:
        json.dump(st.session_state.metrics, f, indent=4)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to extract text from file
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

# Display metrics
st.sidebar.header("Metrics Dashboard")
st.sidebar.metric("Total Resumes Analyzed", st.session_state.metrics['total_analyses'])
st.sidebar.metric("Successful Analyses", st.session_state.metrics['successful_analyses'])
st.sidebar.metric("Failed Analyses", st.session_state.metrics['failed_analyses'])
st.sidebar.metric("Average API Response Time (s)", 
                 f"{sum(st.session_state.metrics['api_response_times']) / len(st.session_state.metrics['api_response_times']) if st.session_state.metrics['api_response_times'] else 0:.2f}")
st.sidebar.subheader("Job Role Frequency")
for role, count in st.session_state.metrics['job_role_counts'].items():
    st.sidebar.text(f"{role}: {count}")

# Main logic
if analyze and uploaded_file:
    try:
        # Extract resume content
        file_content = extract_text_from_file(uploaded_file)
        
        if not file_content.strip():
            st.error("File does not have any content...")
            st.session_state.metrics['failed_analyses'] += 1
            save_metrics()
            st.stop()
        
        # Update job role count
        job_role_key = job_role if job_role else "General"
        st.session_state.metrics['job_role_counts'][job_role_key] = \
            st.session_state.metrics['job_role_counts'].get(job_role_key, 0) + 1
        
        # Construct prompt
        prompt = f"""Please analyze this resume and provide constructive feedback. 
        Focus on the following aspects:
        1. Content clarity and impact
        2. Skills presentation
        3. Experience descriptions
        4. Specific improvements for {job_role if job_role else 'general job applications'}
        
        Resume content:
        {file_content}
        
        Please provide your analysis in a clear, structured format with specific recommendations."""
        
        # Gemini API call with timing
        start_time = time.time()
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1000
            }
        }
        response = requests.post(f"{url}?key={GEMINI_API_KEY}", json=data, headers=headers)
        response_time = time.time() - start_time
        
        # Update metrics
        st.session_state.metrics['total_analyses'] += 1
        st.session_state.metrics['api_response_times'].append(response_time)
        
        # Check for API errors
        if response.status_code != 200:
            st.error(f"Gemini API error: {response.json().get('error', {}).get('message', 'Unknown error')}")
            st.session_state.metrics['failed_analyses'] += 1
            save_metrics()
            st.stop()
        
        # Extract response
        result = response.json().get("candidates")[0].get("content").get("parts")[0].get("text")
        st.session_state.metrics['successful_analyses'] += 1
        save_metrics()
        
        # Display results
        st.markdown("### Analysis Results")
        st.markdown(result)
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.session_state.metrics['failed_analyses'] += 1
        save_metrics()
