import spacy
from transformers import pipeline
from spacy.matcher import Matcher
from collections import defaultdict
from docx import Document
import random
import openai  # Make sure OpenAI is installed
import logging

# Set OpenAI API key
openai.api_key = "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"

# Initialize NLP models
class NLPModelCache:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.sentiment_analyzer = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

    def process_text(self, text):
        return self.nlp(text)

    def analyze_sentiment(self, text):
        result = self.sentiment_analyzer(text)
        return result[0]['label'], result[0]['score']

nlp_cache = NLPModelCache()

# Function to read a resume from a file
def read_resume(file_path):
    try:
        if file_path.endswith('.pdf'):
            return read_pdf(file_path)
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        else:
            raise ValueError("Unsupported file format")
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        return None

# Text preprocessing
def preprocess_text(text):
    doc = nlp_cache.process_text(text)
    return ' '.join([token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct])

# Customizable function to update skill patterns
def update_skill_patterns(custom_skills):
    return [[{'LOWER': skill.lower()}] for skill in custom_skills]

# Skill extraction
def extract_skills(doc, custom_skills=None):
    skill_patterns = update_skill_patterns(custom_skills) if custom_skills else [[{'LOWER': 'python'}], [{'LOWER': 'java'}], [{'LOWER': 'sql'}]]
    matcher = Matcher(nlp_cache.nlp.vocab)
    matcher.add("SKILLS", skill_patterns)
    skills = defaultdict(list)
    for _, start, end in matcher(doc):
        span = doc[start:end]
        skills[span.text].append(span.sent.text)
    return skills

# Contextual skill and experience extraction
def extract_contextual_skills_experience(doc):
    skills = defaultdict(list)
    experiences = []

    for token in doc:
        if token.pos_ == 'VERB':  # This is a simplification, customize as needed
            experiences.append(token.lemma_)

    skill_matcher = Matcher(nlp_cache.nlp.vocab)
    skill_patterns = update_skill_patterns(["Python", "Java", "SQL"])  # Example skills
    skill_matcher.add("SKILL", skill_patterns)

    for _, start, end in skill_matcher(doc):
        span = doc[start:end]
        skills[span.text].append(span.sent.text)

    return skills, experiences

# Enhanced sentiment analysis using the cached model
def enhanced_sentiment_analysis(text):
    sentiment_label, sentiment_score = nlp_cache.analyze_sentiment(text)
    return sentiment_label, sentiment_score

# Function to process a single resume
def process_resume(resume_text, job_description, key_terms):
    # Generate resume with OpenAI's API
    generated_resume = generate_resume_with_openai(job_description, key_terms, resume_text)
    
    # Evaluate generated resume
    score = evaluate_generated_resume(generated_resume, job_description, key_terms)
    
    # Improve generated resume based on feedback
    improved_resume = improve_resume(generated_resume, job_description, key_terms)
    
    return improved_resume

# Function to read PDF content
def read_pdf(file_path):
    """
    Reads the content of a PDF file and returns it as text.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The text content of the PDF file.
    """
    with open(file_path, 'r') as file:
        pdf_text = file.read()
    return pdf_text

# Define the generate_system_message function
def generate_system_message(key_terms):
    role_descriptions = [
        f"You are a professional in the field of {', '.join(key_terms)}.",
        "You are a knowledgeable expert in this field.",
        "You are an experienced professional with expertise in the required skills.",
        # Add more role descriptions as needed
    ]
    return random.choice(role_descriptions)

# Define the generate_resume_with_openai function
def generate_resume_with_openai(job_description, key_terms, resume_text):
    system_message = generate_system_message(key_terms)
    prompt = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"This is my current resume: {resume_text}. Use this as a template such as name, education, job titles, but generate new information based of the key terms and improvements "},
        {"role": "user", "content": f"Create a professional resume for a role with these requirements: {', '.join(key_terms)}."},
        {"role": "user", "content": job_description}  # Include job description as additional user context
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt
        )
        return response.choices[0].message.content.strip() if response.choices else "Failed to generate resume."
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        return "Error in generating resume. Please try again later."

# Function to evaluate the generated resume
def evaluate_generated_resume(generated_resume, job_description, key_terms):
    """
    Evaluates the quality of the generated resume based on its relevance to the job description and key terms.

    Args:
        generated_resume (str): The text of the generated resume.
        job_description (str): The job description for which the resume was generated.
        key_terms (list of str): The key terms or skills required for the job.

    Returns:
        float: A score representing the quality of the generated resume.
    """
    # Placeholder implementation
    # You can implement a more sophisticated evaluation algorithm here
    return 0.75

# Function to adjust the generated resume based on feedback
def improve_resume(generated_resume, job_description, key_terms):
    """
    Improves the generated resume based on feedback from evaluation.

    Args:
        generated_resume (str): The text of the generated resume.
        job_description (str): The job description for which the resume was generated.
        key_terms (list of str): The key terms or skills required for the job.

    Returns:
        str: The improved resume text.
    """
    # Split the job description into sentences for analysis
    job_sentences = job_description.split('.')
    
    # Identify sentences in the generated resume that lack key terms
    missing_sentences = [sentence.strip() for sentence in job_sentences if not any(term in sentence.lower() for term in key_terms)]
    
    # If missing sentences are found, add them to the generated resume
    if missing_sentences:
        improved_resume = generated_resume + '\n\n' + '. '.join(missing_sentences)
    else:
        improved_resume = generated_resume
    
    # Add introductory sentence if missing
    if not generated_resume.startswith("Objective:"):
        improved_resume = "Objective: " + improved_resume
    
    return improved_resume

# Other functions...
