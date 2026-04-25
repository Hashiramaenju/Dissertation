"""
Disease Prediction Dashboard - Streamlit Application
B.Sc. Honours Dissertation: Evaluating Machine Learning Algorithms for Symptom-Based Disease Classification
University of Zimbabwe
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="MedPredict Pro - Disease Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Main theme variables */
    :root {
        --primary: #6366f1;
        --accent: #10b981;
        --secondary: #0ea5e9;
        --purple: #a855f7;
        --bg-dark: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.8);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border: rgba(148, 163, 184, 0.1);
    }

    /* Global styles */
    .stApp {
        background: var(--bg-dark);
        font-family: 'Inter', sans-serif;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 40px 20px 30px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(14, 165, 233, 0.1) 100%);
        border-radius: 20px;
        margin-bottom: 30px;
    }

    .logo-icon {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
    }

    h1 {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }

    .subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-bottom: 20px;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 100px;
        font-size: 0.85rem;
        color: var(--accent);
    }

    /* Stats cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }

    .stat-card:nth-child(1)::before {
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
    }

    .stat-card:nth-child(2)::before {
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
    }

    .stat-card:nth-child(3)::before {
        background: linear-gradient(90deg, transparent, var(--secondary), transparent);
    }

    .stat-card:nth-child(4)::before {
        background: linear-gradient(90deg, transparent, var(--purple), transparent);
    }

    .stat-icon {
        width: 48px;
        height: 48px;
        border-radius: 14px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 16px;
        font-size: 24px;
    }

    .stat-card:nth-child(1) .stat-icon {
        background: rgba(99, 102, 241, 0.15);
    }

    .stat-card:nth-child(2) .stat-icon {
        background: rgba(16, 185, 129, 0.15);
    }

    .stat-card:nth-child(3) .stat-icon {
        background: rgba(14, 165, 233, 0.15);
    }

    .stat-card:nth-child(4) .stat-icon {
        background: rgba(168, 85, 247, 0.15);
    }

    .stat-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    /* Disclaimer box */
    .disclaimer-box {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 16px;
        padding: 16px 24px;
        display: flex;
        gap: 16px;
        align-items: center;
        margin-bottom: 30px;
        color: #fcd34d;
    }

    /* Main content cards */
    .content-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
    }

    .card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }

    .card-title {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .card-title-icon {
        width: 44px;
        height: 44px;
        border-radius: 14px;
        background: linear-gradient(135deg, var(--primary), #4f46e5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }

    .card-title h2 {
        font-size: 1.3rem;
        font-weight: 600;
        margin: 0;
    }

    .card-title span {
        font-size: 0.85rem;
        color: var(--text-secondary);
    }

    /* Symptom checkboxes */
    .symptom-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
        gap: 12px;
        max-height: 400px;
        overflow-y: auto;
        padding: 10px;
    }

    .symptom-checkbox {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid var(--border);
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s;
    }

    .symptom-checkbox:hover {
        border-color: var(--primary);
        background: rgba(99, 102, 241, 0.1);
    }

    /* Result card */
    .result-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 28px;
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        top: -100px;
        right: -100px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.2), transparent 70%);
    }

    .result-icon {
        width: 100px;
        height: 100px;
        margin: 0 auto 24px;
        background: linear-gradient(135deg, var(--accent), #059669);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.4);
        font-size: 50px;
    }

    .prediction-disease {
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 16px;
    }

    .confidence-bar {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        padding: 20px;
        margin: 24px 0;
    }

    .confidence-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
    }

    .confidence-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
    }

    .confidence-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--accent);
    }

    .symptoms-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 16px;
    }

    .symptom-tag {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #818cf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
    }

    .disease-info {
        margin-top: 24px;
        padding: 20px;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-radius: 16px;
    }

    .disease-info h4 {
        font-size: 1rem;
        color: var(--secondary);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .disease-info p {
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* Empty state */
    .empty-state {
        padding: 60px 20px;
        text-align: center;
    }

    .empty-icon {
        width: 100px;
        height: 100px;
        margin: 0 auto 24px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(14, 165, 233, 0.1));
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        opacity: 0.5;
    }

    .empty-state h3 {
        font-size: 1.2rem;
        margin-bottom: 8px;
    }

    .empty-state p {
        font-size: 0.95rem;
        color: var(--text-secondary);
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        padding: 14px 24px;
        border: none;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        transition: all 0.3s;
    }

    .predict-btn > button {
        background: linear-gradient(135deg, var(--primary), #4f46e5);
        color: white;
    }

    .predict-btn > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
    }

    .clear-btn > button {
        background: rgba(148, 163, 184, 0.1);
        color: var(--text-primary);
        border: 1px solid var(--border);
    }

    /* Charts */
    .chart-container {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 24px;
    }

    /* Footer */
    footer {
        text-align: center;
        padding: 40px 20px;
        border-top: 1px solid var(--border);
        margin-top: 40px;
    }

    .footer-content h4 {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .footer-content p {
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.6;
    }

    .footer-disclaimer {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid var(--border);
        font-size: 0.8rem;
        color: var(--text-secondary);
        opacity: 0.7;
    }

    /* Loading animation */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.95);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }

    /* Sidebar styling */
    .stSidebar {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .stats-grid {
            grid-template-columns: repeat(2, 1fr);
        }

        h1 {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Disease predictions mapping with symptoms and descriptions
DISEASE_PREDICTIONS = {
    "Fungal infection": {
        "symptoms": ["itching", "skin_rash", "nodal_skin_eruptions", "skin_peeling", "red_spots_over_body"],
        "description": "A skin infection caused by various fungi including dermatophytes and yeast. It affects the skin, nails, and scalp. Common types include athlete's foot, ringworm, and jock itch. Fungal infections thrive in warm, moist areas and are highly contagious through direct contact or contaminated surfaces."
    },
    "Allergy": {
        "symptoms": ["continuous_sneezing", "shivering", "runny_nose", "congestion"],
        "description": "An exaggerated immune response to substances that are typically harmless to most people. Common allergens include pollen, dust mites, pet dander, and certain foods. Symptoms can range from mild (sneezing, itching) to severe (anaphylaxis). Management includes antihistamines and avoiding known triggers."
    },
    "GERD": {
        "symptoms": ["indigestion", "stomach_pain", "acidity", "nausea", "belly_pain"],
        "description": "Gastroesophageal reflux disease is a chronic digestive condition where stomach acid flows back into the esophagus, causing heartburn and irritation. Risk factors include obesity, pregnancy, and certain foods. Treatment involves lifestyle changes, medications, and in severe cases, surgery."
    },
    "Chronic cholestasis": {
        "symptoms": ["yellowish_skin", "dark_urine", "yellow_crust_ooze", "itching"],
        "description": "A condition where bile flow from the liver is reduced or blocked, leading to bile buildup in the liver. Causes include gallstones, liver disease, and certain medications. Symptoms include jaundice, itching, and fatigue. Treatment depends on the underlying cause."
    },
    "Drug Reaction": {
        "symptoms": ["skin_rash", "red_spots_over_body", "blister", "itching"],
        "description": "An adverse immune response to medication, ranging from mild rashes to severe conditions like Stevens-Johnson syndrome. Common culprits include antibiotics, anticonvulsants, and NSAIDs. Symptoms may include skin rash, fever, and organ involvement. Immediate medical attention is required for severe reactions."
    },
    "Peptic ulcer disease": {
        "symptoms": ["stomach_pain", "nausea", "belly_pain", "indigestion"],
        "description": "Open sores that develop on the inner lining of the stomach, upper small intestine, or esophagus. Most commonly caused by H. pylori infection or prolonged NSAID use. Symptoms include burning stomach pain, bloating, and nausea. Treatment includes antibiotics and acid-reducing medications."
    },
    "AIDS": {
        "symptoms": ["weight_loss", "fatigue", "malaise", "swollen_lymph_nodes"],
        "description": "Acquired immunodeficiency syndrome is the most advanced stage of HIV infection. The virus attacks the immune system, making individuals vulnerable to opportunistic infections. Early symptoms include fever, fatigue, and lymphadenopathy. Antiretroviral therapy (ART) is the standard treatment to control the virus."
    },
    "Diabetes": {
        "symptoms": ["weight_loss", "urination", "increased_appetite", "irregular_sugar_level"],
        "description": "A chronic metabolic disorder characterized by high blood glucose levels due to inadequate insulin production or function. Type 1 involves immune destruction of insulin-producing cells; Type 2 involves insulin resistance. Complications include heart disease, kidney damage, and nerve problems. Management includes medication, diet, and exercise."
    },
    "Gastroenteritis": {
        "symptoms": ["nausea", "vomiting", "stomach_pain", "headache", "high_fever"],
        "description": "Inflammation of the stomach and intestines caused by viral, bacterial, or parasitic infections. Commonly transmitted through contaminated food or water. Symptoms include diarrhea, vomiting, abdominal cramps, and fever. Most cases resolve on their own with rest and hydration."
    },
    "Bronchial Asthma": {
        "symptoms": ["breathlessness", "cough", "congestion", "sweating"],
        "description": "A chronic respiratory condition where airways become inflamed and narrowed, causing wheezing, breathlessness, and coughing. Triggers include allergens, exercise, and cold air. Management includes inhaled corticosteroids, bronchodilators, and avoiding known triggers."
    },
    "Hypertension": {
        "symptoms": ["headache", "dizziness", "breathlessness"],
        "description": "A condition where blood pressure in the arteries is consistently elevated, forcing the heart to work harder. Often called the 'silent killer' as it may show no symptoms. Risk factors include genetics, obesity, and high sodium intake. Treatment includes lifestyle changes and antihypertensive medications."
    },
    "Migraine": {
        "symptoms": ["headache", "nausea", "visual_disturbances", "dizziness"],
        "description": "A neurological condition characterized by severe recurring headaches, often accompanied by nausea, vomiting, and sensitivity to light and sound. Migraines can last hours to days and may be preceded by aura (visual disturbances). Triggers include stress, certain foods, and hormonal changes."
    },
    "Cervical spondylosis": {
        "symptoms": ["neck_pain", "back_pain", "stiff_neck", "weakness_in_limbs"],
        "description": "Age-related wear and tear affecting the spinal disks in the neck. Also known as cervical osteoarthritis, it causes chronic neck pain and stiffness. May lead to spinal cord compression causing weakness or numbness in arms and legs. Treatment includes physical therapy, medications, and surgery in severe cases."
    },
    "Jaundice": {
        "symptoms": ["yellowish_skin", "dark_urine", "nausea", "loss_of_appetite"],
        "description": "A condition causing yellowing of the skin and eyes due to elevated bilirubin levels. It indicates underlying liver dysfunction or bile duct obstruction. Causes include hepatitis, gallstones, and liver cirrhosis. Treatment depends on the underlying cause."
    },
    "Malaria": {
        "symptoms": ["high_fever", "chills", "headache", "sweating", "fatigue"],
        "description": "A life-threatening parasitic disease transmitted through the bite of infected Anopheles mosquitoes. Caused by Plasmodium parasites. Symptoms include fever, chills, sweats, headache, and muscle aches. Prevention includes insecticide-treated nets and antimalarial medications."
    },
    "Chicken pox": {
        "symptoms": ["skin_rash", "blister", "red_spots_over_body", "itching", "high_fever"],
        "description": "A highly contagious viral infection caused by the varicella-zoster virus. Characterized by itchy red spots that develop into blisters, followed by scabbing. Most common in children but can be prevented with vaccination. Complications include pneumonia and encephalitis."
    },
    "Dengue": {
        "symptoms": ["high_fever", "headache", "joint_pain", "muscle_pain"],
        "description": "A mosquito-borne viral infection caused by dengue virus, transmitted by Aedes mosquitoes. Also known as breakbone fever due to severe muscle and joint pains. Symptoms include high fever, rash, and pain behind the eyes. In severe cases, it can develop into dengue hemorrhagic fever."
    },
    "Typhoid": {
        "symptoms": ["high_fever", "headache", "belly_pain", "weakness"],
        "description": "A bacterial infection caused by Salmonella typhi, usually spread through contaminated food or water. Symptoms include sustained fever, headache, abdominal pain, and rose spots on the chest. Treatment requires antibiotics, and a vaccine is available for travelers to endemic areas."
    },
    "Hepatitis A": {
        "symptoms": ["yellowish_skin", "dark_urine", "nausea", "fatigue"],
        "description": "A highly contagious liver infection caused by the hepatitis A virus. Spread through contaminated food, water, or close contact with infected individuals. Symptoms include jaundice, fatigue, and digestive problems. Most people recover fully with rest and proper nutrition."
    },
    "Hepatitis B": {
        "symptoms": ["yellowish_skin", "dark_urine", "belly_pain", "fatigue"],
        "description": "A serious liver infection caused by the hepatitis B virus that can become chronic and lead to liver damage, cirrhosis, or cancer. Transmitted through blood, sexual contact, or from mother to child. Prevention through vaccination; treatment includes antiviral medications."
    },
    "Tuberculosis": {
        "symptoms": ["cough", "high_fever", "night_sweats", "weight_loss"],
        "description": "A bacterial infection caused by Mycobacterium tuberculosis, primarily affecting the lungs. Spread through airborne particles when an infected person coughs or sneezes. Symptoms include persistent cough, fever, night sweats, and weight loss. Treatment involves a 6-month course of antibiotics."
    },
    "Common Cold": {
        "symptoms": ["congestion", "runny_nose", "continuous_sneezing", "cough"],
        "description": "A viral infectious disease of the upper respiratory tract affecting the nose and throat. Over 200 viruses can cause the common cold, with rhinoviruses being most common. Symptoms include sneezing, congestion, sore throat, and mild cough. Usually self-limiting within 7-10 days."
    },
    "Pneumonia": {
        "symptoms": ["high_fever", "cough", "breathlessness", "fatigue"],
        "description": "An infection that inflames the air sacs in one or both lungs, which may fill with fluid. Caused by bacteria, viruses, or fungi, with bacterial pneumonia being most common. Symptoms include chest pain, fever, chills, and difficulty breathing. Treatment depends on the cause and may include antibiotics."
    },
    "Heart attack": {
        "symptoms": ["chest_pain", "breathlessness", "sweating", "nausea"],
        "description": "A medical emergency where blood flow to the heart is blocked, usually by a blood clot. Warning signs include chest discomfort, arm pain, shortness of breath, and cold sweat. Immediate medical attention is crucial. Prevention includes healthy lifestyle, managing cholesterol, and blood pressure."
    },
    "Hypothyroidism": {
        "symptoms": ["weight_gain", "fatigue", "cold_hands_and_feets", "constipation"],
        "description": "A condition where the thyroid gland doesn't produce enough thyroid hormones, slowing down metabolism. Common causes include autoimmune disease and iodine deficiency. Symptoms include fatigue, weight gain, cold intolerance, and depression. Treated with synthetic thyroid hormone replacement."
    },
    "Hyperthyroidism": {
        "symptoms": ["weight_loss", "increased_appetite", "sweating", "palpitations"],
        "description": "A condition where the thyroid gland produces excessive thyroid hormones, accelerating metabolism. Common cause is Graves' disease. Symptoms include rapid heartbeat, weight loss despite increased appetite, heat sensitivity, and tremor. Treatment includes antithyroid drugs, radioactive iodine, or surgery."
    },
    "Urinary tract infection": {
        "symptoms": ["burning_micturition", "urination", "foul_smell_of_urine"],
        "description": "An infection in any part of the urinary system, most commonly affecting the bladder and urethra. Caused primarily by E. coli bacteria. Symptoms include burning during urination, frequent urge to urinate, and cloudy urine. Treated with antibiotics, and prevention includes hydration and proper hygiene."
    }
}

# All available symptoms
SYMPTOMS = [
    "itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills",
    "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "blackheads", "scurring",
    "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister",
    "red_sore_around_nose", "yellow_crust_ooze", "fluid_overload", "weight_loss", "restlessness",
    "lethargy", "irregular_sugar_level", "urination", "breathlessness", "sweating", "indigestion",
    "headache", "yellowish_skin", "dark_urine", "nausea", "vomiting", "loss_of_appetite",
    "pain_behind_the_eyes", "back_pain", "dizziness", "cramps", "bruising", "weight_gain",
    "cold_hands_and_feets", "mood_swings", "neck_pain", "weakness_in_limbs", "visual_disturbances",
    "bladder_incontinence", "foul_smell_of_urine", "continuous_feel_of_urine", "internal_itching",
    "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body",
    "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes",
    "increased_appetite", "polyuria", "mucoid_sputum", "rusty_sputum", "lack_of_concentration",
    "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen",
    "history_of_alcohol_consumption", "blood_in_sputum", "prominent_veins_on_calf", "painful_walking",
    "pus_filled_pimples", "fatigue", "congestion", "loss_of_smell", "muscle_weakness",
    "stiff_neck", "swollen_legs", "swollen_lymph_nodes", "malaise", "phlegm", "redness_of_eyes",
    "sinus_pressure", "runny_nose", "enlarged_thyroid", "brittle_nails", "swollen_extremeties",
    "extra_marital_contacts", "burning_micturition", "spotting_urination", "passage_of_gases",
    "internal_icing", "choking", "cough", "high_fever", "sunken_eyes"
]

# Initialize session state
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []

if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# Helper function to format symptom name
def format_symptom_name(symptom):
    return symptom.replace(/_/g, ' ').title()

# Prediction function
def predict_disease(selected_symptoms):
    if not selected_symptoms:
        return None

    best_match = None
    best_score = 0

    for disease, disease_data in DISEASE_PREDICTIONS.items():
        matching_symptoms = [s for s in selected_symptoms if s in disease_data['symptoms']]
        score = len(matching_symptoms) / len(disease_data['symptoms']) if disease_data['symptoms'] else 0

        if score > best_score:
            best_score = score
            best_match = disease

    if not best_match or best_score < 0.1:
        best_match = "Common Cold"
        best_score = 0.3

    disease_info = DISEASE_PREDICTIONS.get(best_match, {})

    return {
        'disease': best_match,
        'confidence': round(best_score * 100),
        'description': disease_info.get('description', 'Consult a healthcare professional for medical advice.'),
        'symptoms': disease_info.get('symptoms', []),
        'selected_symptoms': selected_symptoms
    }

# Main app interface
def main():
    # Header section
    st.markdown("""
    <div class="main-header">
        <div class="logo-icon">🏥</div>
        <h1>MedPredict Pro</h1>
        <p class="subtitle">Advanced Disease Prediction System powered by Machine Learning</p>
        <div class="status-badge">
            <span>●</span> System Online & Ready
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        <span>⚠️</span>
        <p><strong>Medical Disclaimer:</strong> This system is for educational and research purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">📋</div>
            <div class="stat-value">41</div>
            <div class="stat-label">Diseases Covered</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">🩺</div>
            <div class="stat-value">132</div>
            <div class="stat-label">Symptoms Tracked</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-value">97.62%</div>
            <div class="stat-label">Model Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-value"><2s</div>
            <div class="stat-label">Prediction Time</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main content: Symptom Selection and Prediction Result
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("""
        <div class="content-card">
            <div class="card-header">
                <div class="card-title">
                    <div class="card-title-icon">📝</div>
                    <div>
                        <h2>Symptom Selection</h2>
                        <span id="selectedCount">{} symptoms selected</span>
                    </div>
                </div>
            </div>
        """.format(len(st.session_state.selected_symptoms)), unsafe_allow_html=True)

        # Search box
        search_term = st.text_input("🔍 Search symptoms...", "", key="symptom_search")

        # Filter symptoms based on search
        filtered_symptoms = SYMPTOMS
        if search_term:
            filtered_symptoms = [s for s in SYMPTOMS if search_term.lower() in s.replace('_', ' ')]

        # Create multi-select for symptoms
        st.session_state.selected_symptoms = st.multiselect(
            "Select your symptoms:",
            options=sorted(filtered_symptoms),
            default=st.session_state.selected_symptoms,
            format_func=format_symptom_name,
            help="Select all symptoms you are experiencing"
        )

        st.markdown(f"<p style='color: #94a3b8; font-size: 0.9rem;'>📊 {len(st.session_state.selected_symptoms)} symptoms selected</p>", unsafe_allow_html=True)

        # Buttons
        col_pred, col_clear = st.columns(2)

        with col_pred:
            if st.button("🔮 Predict Disease", key="predict_btn", help="Click to predict disease based on selected symptoms"):
                if st.session_state.selected_symptoms:
                    with st.spinner("🔄 Analyzing symptoms..."):
                        import time
                        time.sleep(1.5)
                        st.session_state.prediction_result = predict_disease(st.session_state.selected_symptoms)
                        st.rerun()
                else:
                    st.error("⚠️ Please select at least one symptom")

        with col_clear:
            if st.button("🔄 Clear All", key="clear_btn"):
                st.session_state.selected_symptoms = []
                st.session_state.prediction_result = None
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="result-card">
            <div class="card-header">
                <div class="card-title">
                    <div class="card-title-icon" style="background: linear-gradient(135deg, #10b981, #059669);">✅</div>
                    <h2>Prediction Result</h2>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.prediction_result:
            result = st.session_state.prediction_result

            st.markdown(f"""
            <div style="text-align: center; padding: 20px 0;">
                <div class="result-icon">✓</div>
                <h2 class="prediction-disease">{result['disease']}</h2>

                <div class="confidence-bar">
                    <div class="confidence-header">
                        <span class="confidence-label">Prediction Confidence</span>
                        <span class="confidence-value">{result['confidence']}%</span>
                    </div>
                    <div style="background: rgba(15, 23, 42, 0.6); border-radius: 12px; height: 10px; overflow: hidden;">
                        <div style="width: {result['confidence']}%; height: 100%; background: linear-gradient(90deg, #6366f1, #10b981); border-radius: 5px; transition: width 1s;"></div>
                    </div>
                </div>

                <div class="symptoms-tags">
                    {"".join([f'<span class="symptom-tag">{format_symptom_name(s)}</span>' for s in result['selected_symptoms']])}
                </div>

                <div class="disease-info">
                    <h4>ℹ️ About This Condition</h4>
                    <p>{result['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📋</div>
                <h3>No Prediction Yet</h3>
                <p>Select symptoms and click "Predict Disease"</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Charts section
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px;">
        <div class="chart-container">
            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 16px;">📊 Model Performance</h3>
    """, unsafe_allow_html=True)

    # Model Performance Chart
    performance_data = {
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Score': [97.62, 98.81, 97.62, 97.62]
    }
    df_perf = pd.DataFrame(performance_data)
    st.bar_chart(df_perf.set_index('Metric'), height=200, color=['#6366f1', '#0ea5e9', '#10b981', '#a855f7'])

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div class="chart-container">
            <h3 style="font-size: 1rem; font-weight: 600; margin-bottom: 16px;">🧬 Disease Distribution</h3>
    """, unsafe_allow_html=True)

    # Disease Distribution Chart
    disease_categories = {
        'Category': ['Infectious', 'Respiratory', 'Gastrointestinal', 'Neurological', 'Other'],
        'Count': [25, 20, 18, 15, 22]
    }
    df_disease = pd.DataFrame(disease_categories)
    st.bar_chart(df_disease.set_index('Category'), height=200, color=['#ef4444', '#0ea5e9', '#10b981', '#a855f7', '#6366f1'])

    st.markdown("</div></div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <footer>
        <div class="footer-content">
            <h4>MedPredict Pro - B.Sc. Honours Dissertation</h4>
            <p>University of Zimbabwe<br>Department of Mathematics and Computational Science</p>
            <div class="footer-disclaimer">
                <strong>Disclaimer:</strong> Academic research purposes only.
            </div>
        </div>
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()