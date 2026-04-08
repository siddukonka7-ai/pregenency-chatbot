import re

# Knowledge base (WHO-style structured data)
knowledge_base = [

    {
        "keywords": ["food", "diet", "nutrition", "eat"],
        "response": """Pregnant women should consume a balanced diet rich in iron, folic acid, calcium, and protein. 
Include green leafy vegetables, fruits, dairy products, eggs, legumes, and whole grains. Adequate hydration is also important."""
    },

    {
        "keywords": ["exercise", "walk", "yoga", "activity"],
        "response": """WHO recommends at least 150 minutes of moderate physical activity per week during pregnancy. 
Safe activities include walking, stretching, and prenatal yoga. Avoid high-risk activities."""
    },

    {
        "keywords": ["rest", "sleep", "tired"],
        "response": """Pregnant women should get 7–9 hours of sleep daily. Proper rest helps in fetal development and reduces stress."""
    },

    {
        "keywords": ["precaution", "care", "safety"],
        "response": """Important precautions include regular antenatal checkups, avoiding alcohol and smoking, maintaining hygiene, and monitoring body changes."""
    },

    {
        "keywords": ["danger", "bleeding", "pain", "fever", "dizziness"],
        "response": """Danger signs during pregnancy include vaginal bleeding, severe abdominal pain, high fever, dizziness, and reduced fetal movement. 
Immediate medical attention is required."""
    },

    {
        "keywords": ["baby", "newborn", "child"],
        "response": """After birth, exclusive breastfeeding is recommended for the first six months. Ensure proper hygiene, vaccination, and regular health checkups."""
    }
]

# Clean input
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text.lower())

# Knowledge search engine
def find_best_match(user_input):

    user_input = clean_text(user_input)
    words = user_input.split()

    best_score = 0
    best_response = None

    for item in knowledge_base:
        score = 0

        for keyword in item["keywords"]:
            if keyword in words:
                score += 1

        if score > best_score:
            best_score = score
            best_response = item["response"]

    return best_response if best_response else None