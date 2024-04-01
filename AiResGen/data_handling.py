import requests
from bs4 import BeautifulSoup
import spacy
import openai
import logging
import PyPDF2
import random

# Initialize NLP model
def get_nlp_model():
    return spacy.load("en_core_web_sm")

nlp_model = get_nlp_model()

# Set the OpenAI API key
openai.api_key = "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"

# Function to scrape job description from a URL
def scrape_job_description(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text(strip=True)
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error: {e}")
        return None

# Function to extract key terms from text
def extract_key_terms(text):
    doc = nlp_model(text)
    key_terms = {token.lemma_.lower() for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ"]}
    return key_terms

# Function to read and extract text from a PDF file
def extract_pdf_text(pdf_file_path):
    try:
        with open(pdf_file_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            return "".join([page.extract_text() for page in reader.pages])
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to generate a resume with OpenAI API
def generate_resume_with_openai(job_description, key_terms, pdf_text, existing_resume):
    system_message = "Create a new resume that highlights the following key skills and experiences, making sure to craft original content that aligns with the job description."
    
    resume_prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "I am looking for a professional resume that showcases my skills and experience in a new light. Below are some details about my background and the job requirements."},
        {"role": "user", "content": f"Current resume details: {existing_resume}."},
        {"role": "user", "content": f"Key requirements for the new role: {', '.join(list(key_terms))}."},
        {"role": "user", "content": f"Additional context from job description: {job_description}"}
    ]
    
    try:
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=resume_prompt)
        
        resume_content = response.choices[0].message.content.strip() if response.choices else "Failed to generate resume."
        
        return resume_content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "Error in generating resume. Please try again later."


# Function to generate a dynamic system message
def generate_system_message(key_terms):
    role_descriptions = [
        f"You are a professional in the field of {', '.join(key_terms)}.",
        "You are a knowledgeable expert in this field.",
        "You are an experienced professional with expertise in the required skills."
    ]
    return random.choice(role_descriptions)

# Function to improve the generated resume based on feedback
def improve_resume(generated_resume, job_description, key_terms):
    job_sentences = job_description.split('.')
    missing_sentences = [sentence.strip() for sentence in job_sentences if not any(term in sentence.lower() for term in key_terms)]
    
    if isinstance(missing_sentences, tuple):
        missing_sentences = list(missing_sentences)

    improved_resume = generated_resume + '\n\n' + '. '.join(missing_sentences) if missing_sentences else generated_resume

    if not generated_resume.startswith("Objective:"):
        improved_resume = "Objective: " + improved_resume

    return improved_resume
