# resume_parse.py

import os
import pandas as pd
from docx import Document
import PyPDF2
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

# Set folder paths
RESUME_FOLDER = "resumes"
OUTPUT_FOLDER = "output"
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "parsed_resumes.csv")

# Predefined skill list (expand as needed)
SKILL_LIST = {
    "python", "sql", "excel", "tableau", "power bi", "aws", "spark", "java",
    "communication", "etl", "pandas", "numpy", "scikit-learn", "r", "git"
}

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(path):
    with open(path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_skills(text):
    tokens = word_tokenize(text.lower())
    found_skills = {skill for skill in SKILL_LIST if skill in " ".join(tokens)}
    return list(found_skills)

def parse_resumes():
    parsed_data = []

    for file_name in os.listdir(RESUME_FOLDER):
        path = os.path.join(RESUME_FOLDER, file_name)
        if file_name.endswith(".docx"):
            text = extract_text_from_docx(path)
        elif file_name.endswith(".pdf"):
            text = extract_text_from_pdf(path)
        else:
            continue

        skills = extract_skills(text)
        resume_id = os.path.splitext(file_name)[0]

        parsed_data.append({
            "resume_id": resume_id,
            "skills": "; ".join(skills)
        })

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    pd.DataFrame(parsed_data).to_csv(OUTPUT_FILE, index=False)
    print(f"Parsed resumes saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    parse_resumes()
