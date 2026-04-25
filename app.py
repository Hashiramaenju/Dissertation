"""
Disease Prediction Dashboard - Streamlit Application
B.Sc. Honours Dissertation: Evaluating Machine Learning Algorithms for Symptom-Based Disease Classification
University of Zimbabwe
"""

import streamlit as st
import streamlit.components.v1 as components
import time

# Page configuration
st.set_page_config(
    page_title="MedPredict Pro - Disease Prediction Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── DATA ────────────────────────────────────────────────────────────────────

SYMPTOMS = sorted([
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
    "internal_icing", "choking", "cough", "high_fever", "sunken_eyes", "night_sweats",
    "palpitations", "constipation", "chest_pain", "muscle_wasting"
])

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
        "symptoms": ["high_fever", "headache", "belly_pain", "weakness_in_limbs"],
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
    },
    "Psoriasis": {
        "symptoms": ["skin_rash", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails"],
        "description": "A chronic autoimmune skin condition that speeds up the skin cell life cycle, causing cells to build up rapidly on the skin surface. Characterized by red patches covered with thick, silvery scales. Treatment includes topical treatments, light therapy, and systemic medications."
    },
    "Impetigo": {
        "symptoms": ["skin_rash", "blister", "red_sore_around_nose", "yellow_crust_ooze"],
        "description": "A highly contagious bacterial skin infection, most common in young children. Causes red sores or blisters that burst and develop honey-colored crusts. Treated with antibiotic creams or oral antibiotics. Maintain good hygiene to prevent spread."
    },
}


def format_symptom(s):
    return s.replace('_', ' ').title()


def predict_disease(selected_symptoms):
    if not selected_symptoms:
        return None
    best_match, best_score = None, 0
    for disease, data in DISEASE_PREDICTIONS.items():
        matching = [s for s in selected_symptoms if s in data['symptoms']]
        score = len(matching) / len(data['symptoms']) if data['symptoms'] else 0
        if score > best_score:
            best_score = score
            best_match = disease
    if not best_match or best_score < 0.1:
        best_match, best_score = "Common Cold", 0.3
    info = DISEASE_PREDICTIONS.get(best_match, {})
    return {
        'disease': best_match,
        'confidence': round(best_score * 100),
        'description': info.get('description', 'Consult a healthcare professional for medical advice.'),
        'selected_symptoms': selected_symptoms,
    }


# ─── SESSION STATE ────────────────────────────────────────────────────────────

if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []
if 'prediction_result' not in st.session_state:
    st.session_state.prediction_result = None

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary:#6366f1; --accent:#10b981; --secondary:#0ea5e9;
    --purple:#a855f7; --bg-dark:#0f172a;
    --bg-card:rgba(30,41,59,.8); --text-primary:#f8fafc;
    --text-secondary:#94a3b8; --border:rgba(148,163,184,.1);
}

html,body,.stApp { background:var(--bg-dark)!important; font-family:'Inter',sans-serif!important; color:var(--text-primary); }
.stApp::before {
    content:''; position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;
    background:
        radial-gradient(circle at 20% 80%,rgba(99,102,241,.15) 0%,transparent 50%),
        radial-gradient(circle at 80% 20%,rgba(14,165,233,.10) 0%,transparent 50%);
}
section.main .block-container { padding-top:0!important; max-width:1400px; }
.stToolbar,#MainMenu,footer { visibility:hidden; }
header[data-testid="stHeader"] { background:transparent!important; }

h1 { font-size:2.8rem!important; font-weight:800!important;
     background:linear-gradient(135deg,#fff 0%,#c7d2fe 100%);
     -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
h2,h3,h4 { color:var(--text-primary)!important; }

.glass { background:var(--bg-card); backdrop-filter:blur(20px); border:1px solid var(--border); }

@keyframes pulse  { 0%,100%{opacity:1} 50%{opacity:.5} }
@keyframes fadeIn { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
@keyframes slideUp{ from{opacity:0;transform:translateY(40px)} to{opacity:1;transform:translateY(0)} }
.slide-up { animation:slideUp .6s ease-out; }
.fade-in  { animation:fadeIn  .5s ease-out; }

/* Header */
.mp-header { text-align:center; padding:40px 20px 30px; }
.logo-icon { width:64px; height:64px; background:linear-gradient(135deg,var(--primary),var(--secondary));
    border-radius:20px; display:inline-flex; align-items:center; justify-content:center;
    margin-bottom:16px; box-shadow:0 20px 40px rgba(99,102,241,.3); }
.logo-icon svg { width:36px; height:36px; color:white; }
.mp-subtitle { font-size:1.1rem; color:var(--text-secondary); margin-top:8px; }
.status-badge { display:inline-flex; align-items:center; gap:8px; margin-top:20px; padding:10px 20px;
    background:rgba(16,185,129,.1); border:1px solid rgba(16,185,129,.3);
    border-radius:100px; font-size:.85rem; color:var(--accent); }
.status-dot { width:8px; height:8px; background:var(--accent); border-radius:50%;
    animation:pulse 2s infinite; display:inline-block; }

/* Disclaimer */
.disclaimer { max-width:900px; margin:0 auto 30px; padding:16px 24px;
    background:rgba(245,158,11,.1); border:1px solid rgba(245,158,11,.3);
    border-radius:16px; display:flex; gap:16px; align-items:center; }
.disclaimer svg { width:28px; height:28px; flex-shrink:0; }
.disclaimer p { font-size:.9rem; color:#fcd34d; margin:0; }

/* Stats */
.stats-bar { display:grid; grid-template-columns:repeat(4,1fr); gap:20px; margin-bottom:30px; }
.stat-card { padding:24px; border-radius:20px; position:relative; overflow:hidden; text-align:center; }
.stat-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; }
.stat-card:nth-child(1)::before { background:linear-gradient(90deg,transparent,var(--primary),transparent); }
.stat-card:nth-child(2)::before { background:linear-gradient(90deg,transparent,var(--accent),transparent); }
.stat-card:nth-child(3)::before { background:linear-gradient(90deg,transparent,var(--secondary),transparent); }
.stat-card:nth-child(4)::before { background:linear-gradient(90deg,transparent,var(--purple),transparent); }
.stat-icon { width:48px; height:48px; border-radius:14px; display:inline-flex;
    align-items:center; justify-content:center; margin-bottom:16px; }
.stat-card:nth-child(1) .stat-icon { background:rgba(99,102,241,.15); color:var(--primary); }
.stat-card:nth-child(2) .stat-icon { background:rgba(16,185,129,.15); color:var(--accent); }
.stat-card:nth-child(3) .stat-icon { background:rgba(14,165,233,.15); color:var(--secondary); }
.stat-card:nth-child(4) .stat-icon { background:rgba(168,85,247,.15); color:var(--purple); }
.stat-icon svg { width:24px; height:24px; }
.stat-value { font-size:2.2rem; font-weight:800; margin-bottom:4px; }
.stat-label { font-size:.9rem; color:var(--text-secondary); font-weight:500; }

/* Cards */
.card { border-radius:24px; padding:28px; }
.card-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:24px; }
.card-title { display:flex; align-items:center; gap:12px; }
.card-title-icon { width:44px; height:44px; border-radius:14px;
    background:linear-gradient(135deg,var(--primary),#4f46e5);
    display:flex; align-items:center; justify-content:center; }
.card-title-icon svg { width:22px; height:22px; color:white; }
.card-title h2 { font-size:1.3rem!important; font-weight:600!important; margin:0; }
.card-title span { font-size:.85rem; color:var(--text-secondary); }

/* Result card */
.result-card { position:relative; overflow:hidden; }
.result-card::before { content:''; position:absolute; top:-100px; right:-100px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(99,102,241,.2),transparent 70%); }
.result-content { text-align:center; padding:20px 0; animation:fadeIn .5s ease-out; }
.result-icon { width:100px; height:100px; margin:0 auto 24px;
    background:#10b981; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 20px 40px rgba(16,185,129,.4); }
.result-icon svg { width:52px; height:52px; color:white; stroke-width:3; }
.prediction-disease { font-size:2rem!important; font-weight:800!important; margin-bottom:16px;
    color:#ffffff!important; -webkit-text-fill-color:#ffffff!important; }
.confidence-bar { background:rgba(15,23,42,.6); border-radius:12px; padding:20px; margin:24px 0; }
.confidence-header { display:flex; justify-content:space-between; margin-bottom:12px; }
.confidence-label { font-size:.9rem; color:var(--text-secondary); }
.confidence-value { font-size:1.1rem; font-weight:700; color:var(--accent); }
.confidence-track { height:10px; background:rgba(99,102,241,.2); border-radius:5px; overflow:hidden; }
.confidence-fill { height:100%; background:linear-gradient(90deg,var(--primary),var(--accent));
    border-radius:5px; transition:width 1s; }
.selected-symptoms-display { margin-top:24px; text-align:left; }
.selected-symptoms-display h4 { font-size:.9rem; color:var(--text-secondary); margin-bottom:12px; font-weight:600; }
.symptoms-tags { display:flex; flex-wrap:wrap; gap:8px; }
.symptom-tag { background:linear-gradient(135deg,rgba(99,102,241,.2),rgba(99,102,241,.1));
    border:1px solid rgba(99,102,241,.3); color:#818cf8;
    padding:6px 14px; border-radius:20px; font-size:.8rem; }
.disease-info { margin-top:24px; padding:24px;
    background:rgba(14,165,233,.08);
    border:1px solid rgba(14,165,233,.2); border-radius:16px; }
.disease-info-top { display:flex; align-items:center; gap:20px; margin-bottom:20px; }
.disease-info-icon { flex-shrink:0; width:90px; height:90px;
    border:4px solid #0ea5e9; border-radius:50%;
    display:flex; align-items:center; justify-content:center; }
.disease-info-icon svg { width:50px; height:50px; color:#0ea5e9; }
.disease-info-title { font-size:1.1rem; font-weight:700; color:#0ea5e9; line-height:1.3; }
.disease-info p { font-size:.9rem; color:var(--text-secondary); line-height:1.8; margin:0; text-align:center; }

/* Empty state */
.empty-state { padding:60px 20px; text-align:center; }
.empty-icon { width:100px; height:100px; margin:0 auto 24px;
    background:linear-gradient(135deg,rgba(99,102,241,.1),rgba(14,165,233,.1));
    border-radius:50%; display:flex; align-items:center; justify-content:center; }
.empty-icon svg { width:48px; height:48px; color:var(--text-secondary); opacity:.5; }
.empty-state h3 { font-size:1.2rem; margin-bottom:8px; }
.empty-state p { font-size:.95rem; color:var(--text-secondary); }

/* Footer */
.mp-footer { text-align:center; padding:40px 20px;
    border-top:1px solid var(--border); margin-top:40px; }
.footer-content { max-width:600px; margin:0 auto; }
.footer-content h4 { font-size:1.1rem; font-weight:700; margin-bottom:8px; }
.footer-content p { font-size:.9rem; color:var(--text-secondary); line-height:1.6; }
.footer-disclaimer { margin-top:20px; padding-top:20px;
    border-top:1px solid var(--border); font-size:.8rem; color:var(--text-secondary); opacity:.7; }

/* Streamlit overrides */
div[data-testid="stTextInput"] input {
    background:rgba(8,12,28,.85)!important; border:1px solid rgba(148,163,184,.15)!important;
    border-radius:12px!important; color:var(--text-primary)!important;
    padding:14px 14px 14px 48px!important; font-size:.95rem!important;
}
div[data-testid="stTextInput"] input::placeholder { color:#4a5568!important; }
div[data-testid="stTextInput"] input:focus { border-color:var(--primary)!important; box-shadow:0 0 0 2px rgba(99,102,241,.2)!important; }
div[data-testid="stTextInput"] label { display:none!important; }

/* Unchecked checkbox pill */
div[data-testid="stCheckbox"] > label {
    background:rgba(15,23,42,.5)!important; border:1px solid rgba(148,163,184,.12)!important;
    border-radius:10px!important; padding:10px 14px!important; width:100%!important;
    cursor:pointer!important; font-size:.85rem!important; color:var(--text-primary)!important;
    transition:all .2s!important; display:flex!important; align-items:center!important;
}
div[data-testid="stCheckbox"] > label:hover {
    border-color:#0ea5e9!important; background:rgba(14,165,233,.08)!important;
}
/* Checked checkbox pill — cyan/blue highlight matching screenshot */
div[data-testid="stCheckbox"]:has(input:checked) > label {
    border-color:#0ea5e9!important;
    background:rgba(14,165,233,.15)!important;
    color:#38bdf8!important;
}
div[data-testid="stCheckbox"]:has(input:checked) > label span { color:#38bdf8!important; }
/* Checkbox tick mark color */
div[data-testid="stCheckbox"]:has(input:checked) svg { color:#0ea5e9!important; fill:#0ea5e9!important; }

/* Predict button */
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:first-child button {
    background:#6366f1!important;
    color:white!important; border:none!important; border-radius:12px!important;
    font-weight:600!important; width:100%!important; padding:14px!important;
    transition:all .3s!important;
}
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:first-child button:hover {
    background:#4f46e5!important;
    transform:translateY(-2px)!important;
    box-shadow:0 10px 30px rgba(99,102,241,.4)!important;
}
/* Clear button */
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]:last-child button {
    background:rgba(30,41,59,.6)!important; color:var(--text-primary)!important;
    border:1px solid rgba(148,163,184,.15)!important; border-radius:12px!important;
    font-weight:600!important; width:100%!important; padding:14px!important;
}

/* Scrollable symptom area — visible scrollbar like screenshot */
.symptom-scroll {
    max-height:400px; overflow-y:scroll; margin-bottom:16px; padding-right:6px;
}
.symptom-scroll::-webkit-scrollbar { width:6px; }
.symptom-scroll::-webkit-scrollbar-track { background:rgba(15,23,42,.5); border-radius:4px; }
.symptom-scroll::-webkit-scrollbar-thumb { background:#334155; border-radius:4px; }
.symptom-scroll::-webkit-scrollbar-thumb:hover { background:#475569; }
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="mp-header slide-up">
  <div class="logo-icon">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0
           01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622
           5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
    </svg>
  </div>
  <h1>MedPredict Pro</h1>
  <p class="mp-subtitle">Advanced Disease Prediction System powered by Machine Learning</p>
  <div class="status-badge">
    <span class="status-dot"></span>&nbsp;System Online &amp; Ready
  </div>
</div>
""", unsafe_allow_html=True)

# ─── DISCLAIMER ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="disclaimer">
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#f59e0b">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
      d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4
         c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
  </svg>
  <p><strong>Medical Disclaimer:</strong> This system is for educational and research purposes only.
  It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the
  advice of your physician or other qualified health provider with any questions you may have
  regarding a medical condition.</p>
</div>
""", unsafe_allow_html=True)

# ─── STATS BAR ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="stats-bar">
  <div class="stat-card glass slide-up">
    <div class="stat-icon">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0
             00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
      </svg>
    </div>
    <div class="stat-value">41</div>
    <div class="stat-label">Diseases Covered</div>
  </div>
  <div class="stat-card glass slide-up">
    <div class="stat-icon">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0
             0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0
             012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
      </svg>
    </div>
    <div class="stat-value">132</div>
    <div class="stat-label">Symptoms Tracked</div>
  </div>
  <div class="stat-card glass slide-up">
    <div class="stat-icon">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
      </svg>
    </div>
    <div class="stat-value">97.62%</div>
    <div class="stat-label">Model Accuracy</div>
  </div>
  <div class="stat-card glass slide-up">
    <div class="stat-icon">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
      </svg>
    </div>
    <div class="stat-value">&lt;2s</div>
    <div class="stat-label">Prediction Time</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── MAIN GRID ───────────────────────────────────────────────────────────────

col_left, col_right = st.columns([1.2, 1], gap="medium")

# ── LEFT ─────────────────────────────────────────────────────────────────────
with col_left:
    n = len(st.session_state.selected_symptoms)
    count_text = f"{n} symptom{'s' if n != 1 else ''} selected" if n else "No symptoms selected"

    st.markdown(f"""
    <div class="card glass slide-up">
      <div class="card-header">
        <div class="card-title">
          <div class="card-title-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0
                   01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
          </div>
          <div>
            <h2>Symptom Selection</h2>
            <span>{count_text}</span>
          </div>
        </div>
      </div>
    """, unsafe_allow_html=True)

    # Search input with overlaid magnifier icon
    st.markdown("""
    <div style="position:relative;margin-bottom:4px;">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#94a3b8"
           style="position:absolute;left:16px;top:14px;width:20px;height:20px;z-index:10;pointer-events:none;">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
    </div>
    """, unsafe_allow_html=True)
    search_term = st.text_input("search", "", key="symptom_search",
                                label_visibility="collapsed",
                                placeholder="Search symptoms...",
                                on_change=None)  # triggers rerun on every keystroke automatically

    filtered = [s for s in SYMPTOMS
                if not search_term or search_term.lower() in s.replace('_', ' ')]

    st.markdown('<div class="symptom-scroll">', unsafe_allow_html=True)
    cols3 = st.columns(3)
    newly_selected = []
    for i, symptom in enumerate(filtered):
        checked = cols3[i % 3].checkbox(
            format_symptom(symptom),
            value=symptom in st.session_state.selected_symptoms,
            key=f"cb_{symptom}"
        )
        if checked:
            newly_selected.append(symptom)
    st.markdown('</div>', unsafe_allow_html=True)

    st.session_state.selected_symptoms = newly_selected

    bcol1, bcol2 = st.columns(2)
    with bcol1:
        if st.button("⚡  Predict Disease", key="predict_btn"):
            if st.session_state.selected_symptoms:
                with st.spinner("Analyzing symptoms..."):
                    time.sleep(1.5)
                    st.session_state.prediction_result = predict_disease(
                        st.session_state.selected_symptoms)
                st.rerun()
            else:
                st.error("Please select at least one symptom first.")
    with bcol2:
        if st.button("↺  Clear All", key="clear_btn"):
            st.session_state.selected_symptoms = []
            st.session_state.prediction_result = None
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)  # close card

# ── RIGHT ─────────────────────────────────────────────────────────────────────
with col_right:
    st.markdown("""
    <div class="card result-card glass slide-up">
      <div class="card-header">
        <div class="card-title">
          <div class="card-title-icon" style="background:linear-gradient(135deg,#10b981,#059669);">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <h2>Prediction Result</h2>
        </div>
      </div>
    """, unsafe_allow_html=True)

    result = st.session_state.prediction_result
    if result:
        tags_html = "".join(
            f'<span class="symptom-tag">{format_symptom(s)}</span>'
            for s in result['selected_symptoms']
        )
        st.markdown(f"""
        <div class="result-content fade-in">
          <div class="result-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="white" stroke-width="3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
            </svg>
          </div>
          <h2 class="prediction-disease">{result['disease']}</h2>
          <div class="confidence-bar">
            <div class="confidence-header">
              <span class="confidence-label">Prediction Confidence</span>
              <span class="confidence-value">{result['confidence']}%</span>
            </div>
            <div class="confidence-track">
              <div class="confidence-fill" style="width:{result['confidence']}%"></div>
            </div>
          </div>
          <div class="selected-symptoms-display">
            <h4>Your Selected Symptoms</h4>
            <div class="symptoms-tags">{tags_html}</div>
          </div>
          <div class="disease-info">
            <div class="disease-info-top">
              <div class="disease-info-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#0ea5e9" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div class="disease-info-title">About This<br>Condition</div>
            </div>
            <p>{result['description']}</p>
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0
                   00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
            </svg>
          </div>
          <h3>No Prediction Yet</h3>
          <p>Select symptoms and click "Predict Disease"</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close card

# ─── CHARTS (Chart.js via embedded iframe) ────────────────────────────────────

charts_html = """
<!DOCTYPE html><html><head>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:transparent;font-family:'Inter',sans-serif;color:#f8fafc;}
  .charts-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:24px;padding:4px;}
  .chart-card{background:rgba(30,41,59,.8);border:1px solid rgba(148,163,184,.1);
    border-radius:20px;padding:24px;}
  .chart-card h3{font-size:1rem;font-weight:600;margin-bottom:16px;
    display:flex;align-items:center;gap:8px;color:#f8fafc;}
  .chart-card h3 svg{width:20px;height:20px;}
  .chart-wrap{position:relative;height:220px;}
</style></head><body>
<div class="charts-grid">
  <div class="chart-card">
    <h3>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#6366f1">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0
             002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2
             2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
      </svg>
      Model Performance
    </h3>
    <div class="chart-wrap"><canvas id="perfChart"></canvas></div>
  </div>
  <div class="chart-card">
    <h3>
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="#6366f1">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
          d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/>
      </svg>
      Disease Distribution
    </h3>
    <div class="chart-wrap"><canvas id="distChart"></canvas></div>
  </div>
</div>
<script>
  new Chart(document.getElementById('perfChart'),{
    type:'bar',
    data:{
      labels:['Accuracy','Precision','Recall','F1-Score'],
      datasets:[{
        data:[97.62,98.81,97.62,97.62],
        backgroundColor:['rgba(99,102,241,.8)','rgba(14,165,233,.8)','rgba(16,185,129,.8)','rgba(168,85,247,.8)'],
        borderRadius:8
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      plugins:{legend:{display:false}},
      scales:{
        y:{beginAtZero:true,max:100,grid:{color:'rgba(148,163,184,.1)'},ticks:{color:'#94a3b8'}},
        x:{grid:{display:false},ticks:{color:'#94a3b8'}}
      }
    }
  });
  new Chart(document.getElementById('distChart'),{
    type:'doughnut',
    data:{
      labels:['Infectious','Respiratory','Gastrointestinal','Neurological','Other'],
      datasets:[{
        data:[25,20,18,15,22],
        backgroundColor:['rgba(239,68,68,.8)','rgba(14,165,233,.8)','rgba(16,185,129,.8)','rgba(168,85,247,.8)','rgba(99,102,241,.8)'],
        borderWidth:0
      }]
    },
    options:{
      responsive:true,maintainAspectRatio:false,
      cutout:'65%',
      plugins:{legend:{position:'right',labels:{color:'#94a3b8',padding:12,usePointStyle:true}}}
    }
  });
</script>
</body></html>
"""

components.html(charts_html, height=310, scrolling=False)

# ─── FOOTER ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="mp-footer">
  <div class="footer-content">
    <h4>MedPredict Pro - B.Sc. Honours Dissertation</h4>
    <p>University of Zimbabwe<br>Department of Mathematics and Computational Science</p>
    <div class="footer-disclaimer">
      <strong>Disclaimer:</strong> Academic research purposes only.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
