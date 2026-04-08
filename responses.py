import random
import re
from database import get_memory, set_memory


def clean(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


knowledge = [
    {
        "topic": "food",
        "keywords": ["food", "diet", "eat", "nutrition", "meal"],
        "responses": [
            "Pregnant women should eat iron-rich foods, fruits, vegetables, dairy products, protein sources, and whole grains.",
            "A balanced pregnancy diet should include folate, iron, calcium, protein, fruits, vegetables, and enough water.",
            "Healthy pregnancy nutrition includes leafy greens, legumes, dairy, eggs, fruits, and whole grains."
        ]
    },
    {
        "topic": "exercise",
        "keywords": ["exercise", "walk", "walking", "yoga", "activity"],
        "responses": [
            "Moderate exercise such as walking and prenatal yoga is generally safe during pregnancy.",
            "Pregnancy-safe activity may include walking, stretching, and prenatal yoga, unless your doctor advises otherwise.",
            "Light physical activity can support health during pregnancy, but avoid risky or painful movements."
        ]
    },
    {
        "topic": "rest",
        "keywords": ["rest", "sleep", "tired", "fatigue", "weak"],
        "responses": [
            "Proper rest and 7 to 9 hours of sleep are important during pregnancy.",
            "Fatigue can be common in pregnancy, so sleep, hydration, and balanced meals are important.",
            "Rest supports both maternal well-being and healthy fetal development."
        ]
    },
    {
        "topic": "precautions",
        "keywords": ["precaution", "precautions", "care", "safety"],
        "responses": [
            "Important precautions include regular antenatal checkups, healthy food, hygiene, and avoiding alcohol and smoking.",
            "Pregnancy care includes balanced nutrition, rest, regular checkups, hygiene, and awareness of danger signs.",
            "Follow healthy routines, attend checkups, and stay alert to warning symptoms during pregnancy."
        ]
    },
    {
        "topic": "danger",
        "keywords": ["bleeding", "pain", "fever", "dizziness", "fainting", "blurred vision", "movement"],
        "responses": [
            "These symptoms may indicate a serious pregnancy complication. Please seek immediate medical attention.",
            "Warning signs like bleeding, severe pain, high fever, dizziness, or reduced baby movement need urgent medical care.",
            "Danger signs during pregnancy should not be ignored. Immediate medical help is recommended."
        ]
    },
    {
        "topic": "baby",
        "keywords": ["baby", "newborn", "infant", "after birth"],
        "responses": [
            "Newborn care includes breastfeeding, hygiene, warmth, immunization, and regular health checkups.",
            "After birth, ensure exclusive breastfeeding, proper hygiene, and timely vaccination.",
            "Baby care should focus on feeding, cleanliness, warmth, and regular medical follow-up."
        ]
    }
]


def get_response(user_input, user_id):
    text = clean(user_input)

    if not text:
        return "Please type your question so I can help you."

    if "first trimester" in text:
        set_memory(user_id, "trimester", "first trimester")
        return "Got it. I will guide you based on the first trimester."

    if "second trimester" in text:
        set_memory(user_id, "trimester", "second trimester")
        return "Got it. I will guide you based on the second trimester."

    if "third trimester" in text:
        set_memory(user_id, "trimester", "third trimester")
        return "Got it. I will guide you based on the third trimester."

    emergency_pairs = [
        ("fever", "dizziness"),
        ("bleeding", "pain"),
        ("reduced", "movement"),
        ("no", "movement")
    ]

    words = text.split()
    for a, b in emergency_pairs:
        if a in words and b in words:
            set_memory(user_id, "last_topic", "danger")
            return "These symptoms may be serious. Please use SOS, call your guardian, or go to the nearest hospital immediately."

    best_item = None
    best_score = 0

    for item in knowledge:
        score = 0
        for keyword in item["keywords"]:
            if keyword in text:
                score += len(keyword.split()) + 1
        if score > best_score:
            best_score = score
            best_item = item

    if best_item:
        set_memory(user_id, "last_topic", best_item["topic"])
        response = random.choice(best_item["responses"])

        trimester = get_memory(user_id, "trimester")
        if trimester and best_item["topic"] in ["food", "exercise", "rest", "precautions"]:
            response += f" Since you mentioned that you are in the {trimester}, follow this guidance according to that stage."

        followups = {
            "food": " Would you like diet tips too?",
            "exercise": " Would you like safe exercise suggestions?",
            "rest": " Are you feeling tired often?",
            "precautions": " Would you like trimester-wise precautions?",
            "baby": " Would you like newborn feeding guidance?"
        }

        if best_item["topic"] in followups:
            response += followups[best_item["topic"]]

        return response

    last_topic = get_memory(user_id, "last_topic")
    if "tell me more" in text and last_topic:
        if last_topic == "food":
            return "Pregnancy food should include iron, folate, calcium, protein, fruits, vegetables, and enough fluids."
        if last_topic == "exercise":
            return "Safe options often include walking, stretching, and prenatal yoga. Avoid overexertion."
        if last_topic == "rest":
            return "Rest is important because pregnancy may increase fatigue. Good sleep and hydration can help."
        if last_topic == "danger":
            return "Danger signs should not be ignored. Please seek urgent care for bleeding, severe pain, fainting, or reduced baby movement."

    return "I can help with pregnancy food, exercise, rest, precautions, baby care, and danger signs. Please ask your question."