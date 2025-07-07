from pdfminer.high_level import extract_text
from flashtext import KeywordProcessor

# ✅ Define your skill keywords (you can load from a file too)
skill_keywords = [
    'python', 'java', 'c++', 'machine learning', 'deep learning',
    'data science', 'sql', 'pandas', 'numpy', 'matplotlib',
    'excel', 'communication', 'teamwork', 'linux', 'tensorflow',
    'keras', 'scikit-learn', 'data analysis', 'nlp', 'computer vision'
]

# ✅ Initialize FlashText
kp = KeywordProcessor()
for skill in skill_keywords:
    kp.add_keyword(skill.lower())

def parse_resume(file_path):
    text = extract_text(file_path)
    found_skills = list(set(kp.extract_keywords(text.lower())))
    return text, found_skills
