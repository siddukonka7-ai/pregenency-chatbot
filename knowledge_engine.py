import re

knowledge_base = [
    {
        "keywords": ["food", "diet", "nutrition", "eat"],
        "topic": "nutrition",
        "response": "Pregnant women should eat iron-rich foods, fruits, vegetables, dairy products, legumes, eggs, and whole grains."
    },
    {
        "keywords": ["exercise", "walk", "yoga"],
        "topic": "exercise",
        "response": "Moderate exercise such as walking and prenatal yoga is generally safe during pregnancy."
    },
    {
        "keywords": ["rest", "sleep", "tired"],
        "topic": "rest",
        "response": "Proper rest and 7 to 9 hours of sleep are important for maternal well-being and fetal development."
    },
    {
        "keywords": ["precaution", "care", "safety"],
        "topic": "care",
        "response": "Important precautions include regular antenatal checkups, avoiding alcohol and smoking, and maintaining hygiene."
    },
    {
        "keywords": ["bleeding", "pain", "fever", "dizziness"],
        "topic": "danger",
        "response": "These symptoms may indicate a serious condition and need immediate medical attention."
    },
    {
        "keywords": ["baby", "newborn"],
        "topic": "baby",
        "response": "After birth, ensure breastfeeding, hygiene, immunization, and regular health checkups for the baby."
    }
]

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text.lower())

def find_best_match(user_input):
    user_input = clean_text(user_input)
    words = user_input.split()

    best_score = 0
    best_item = None

    for item in knowledge_base:
        score = 0
        for keyword in item["keywords"]:
            if keyword in words:
                score += 1

        if score > best_score:
            best_score = score
            best_item = item

    return best_item