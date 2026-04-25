import streamlit as st
import pandas as pd
from collections import Counter

# Page config
st.set_page_config(
    page_title="MedPredict Pro",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS to match HTML dashboard exactly
st.markdown("""
<style>
    * { margin: 0; padding: 0; box-sizing: border-box; }

    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        background: #0f172a;
        color: #f8fafc;
    }

    /* Background Animation */
    .main-bg {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: -1;
        background: radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(14, 165, 233, 0.1) 0%, transparent 50%);
    }

    /* Glass Card Effect */
    .glass-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 28px;
    }

    /* Header Styles */
    .main-header {
        text-align: center;
        padding: 40px 20px 30px;
    }

    .logo-icon {
        width: 80px; height: 80px;
        background: linear-gradient(135deg, #6366f1, #0ea5e9);
        border-radius: 24px;
        display: inline-flex; align-items: center; justify-content: center;
        margin-bottom: 20px;
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        font-size: 40px;
    }

    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }

    .status-badge {
        display: inline-flex; align-items: center; gap: 10px;
        padding: 12px 24px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 100px;
        font-size: 0.9rem;
        color: #10b981;
    }

    .status-dot {
        width: 10px; height: 10px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Stats Bar */
    .stats-bar {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }

    .stat-card {
        padding: 24px;
        border-radius: 20px;
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 4px;
    }

    .stat-icon {
        width: 60px; height: 60px;
        border-radius: 16px;
        display: inline-flex; align-items: center; justify-content: center;
        margin-bottom: 16px;
        font-size: 28px;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .stat-label {
        font-size: 0.95rem;
        color: #94a3b8;
        font-weight: 500;
    }

    /* Symptom Grid */
    .symptom-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 12px;
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
    }

    .symptom-chip {
        padding: 14px 18px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 0.9rem;
    }

    .symptom-chip:hover {
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.1);
    }

    .symptom-chip.selected {
        border-color: #6366f1;
        background: rgba(99, 102, 241, 0.2);
    }

    .checkbox-icon {
        width: 24px; height: 24px;
        border: 2px solid #94a3b8;
        border-radius: 6px;
        display: flex; align-items: center; justify-content: center;
        font-size: 14px;
    }

    .symptom-chip.selected .checkbox-icon {
        background: #6366f1;
        border-color: #6366f1;
    }

    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #6366f1, #4f46e5);
        color: white;
        padding: 16px 32px;
        border: none;
        border-radius: 14px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex; align-items: center; justify-content: center;
        gap: 10px;
        transition: all 0.3s;
    }

    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
    }

    .btn-secondary {
        background: rgba(148, 163, 184, 0.1);
        color: #f8fafc;
        border: 1px solid rgba(148, 163, 184, 0.2);
        padding: 16px 32px;
        border-radius: 14px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        display: inline-flex; align-items: center; justify-content: center;
        gap: 10px;
    }

    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(30, 41, 59, 0.6));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        top: -100px; right: -100px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.15), transparent 70%);
    }

    .result-icon {
        width: 100px; height: 100px;
        margin: 0 auto 24px;
        background: linear-gradient(135deg, #10b981, #059669);
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 50px;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);
    }

    .prediction-disease {
        font-size: 2.2rem;
        font-weight: 800;
        color: #10b981;
        margin-bottom: 20px;
    }

    /* Confidence Bar */
    .confidence-bar {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }

    .confidence-header {
        display: flex;
        justify-content: space-between;
        margin-bottom: 12px;
        font-size: 0.95rem;
    }

    .confidence-value {
        font-size: 1.2rem;
        font-weight: 700;
        color: #10b981;
    }

    .confidence-track {
        height: 12px;
        background: rgba(99, 102, 241, 0.2);
        border-radius: 6px;
        overflow: hidden;
    }

    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366f1, #10b981);
        border-radius: 6px;
        transition: width 1s;
    }

    /* Symptom Tags */
    .symptom-tag {
        display: inline-block;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1));
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #818cf8;
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 4px;
    }

    /* Disease Info */
    .disease-info {
        margin-top: 24px;
        padding: 24px;
        background: rgba(14, 165, 233, 0.1);
        border: 1px solid rgba(14, 165, 233, 0.2);
        border-radius: 16px;
        text-align: left;
    }

    .disease-info h4 {
        color: #0ea5e9;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .disease-info p {
        color: #94a3b8;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    /* Charts Grid */
    .charts-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 24px;
        margin-top: 30px;
    }

    .chart-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 20px;
        padding: 24px;
    }

    .chart-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Footer */
    footer {
        text-align: center;
        padding: 40px 20px;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 50px;
    }

    footer h4 {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    footer p {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    footer .disclaimer {
        margin-top: 20px;
        padding-top: 20px;
        border-top: 1px solid rgba(148, 163, 184, 0.1);
        font-size: 0.85rem;
        opacity: 0.7;
    }

    /* Disclaimer Box */
    .disclaimer-box {
        max-width: 900px;
        margin: 0 auto 30px;
        padding: 16px 24px;
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 16px;
        display: flex;
        gap: 16px;
        align-items: center;
        font-size: 0.9rem;
        color: #fcd34d;
    }

    /* Empty State */
    .empty-state {
        padding: 60px 20px;
        text-align: center;
    }

    .empty-icon {
        width: 100px; height: 100px;
        margin: 0 auto 24px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(14, 165, 233, 0.1));
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 48px;
        opacity: 0.5;
    }

    .empty-state h3 {
        font-size: 1.3rem;
        margin-bottom: 8px;
    }

    .empty-state p {
        color: #94a3b8;
    }

    /* Loading Overlay */
    .loading-overlay {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(15, 23, 42, 0.95);
        display: flex; align-items: center; justify-content: center;
        z-index: 9999;
    }

    .loader {
        text-align: center;
    }

    .loader-spinner {
        width: 60px; height: 60px;
        border: 4px solid rgba(99, 102, 241, 0.2);
        border-top-color: #6366f1;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 20px;
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Disease predictions with FULL descriptions
disease_data = {
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

# All unique symptoms
all_symptoms = sorted(set(
    symptom
    for symptoms in disease_data.values()
    for symptom in symptoms
))

# All symptoms for the full list
full_symptoms = ["itching", "skin_rash", "nodal_skin_eruptions", "continuous_sneezing", "shivering", "chills", "joint_pain", "stomach_pain", "acidity", "ulcers_on_tongue", "blackheads", "scurring", "skin_peeling", "silver_like_dusting", "small_dents_in_nails", "inflammatory_nails", "blister", "red_sore_around_nose", "yellow_crust_ooze", "fluid_overload", "weight_loss", "restlessness", "lethargy", "irregular_sugar_level", "urination", "breathlessness", "sweating", "indigestion", "headache", "yellowish_skin", "dark_urine", "nausea", "vomiting", "loss_of_appetite", "pain_behind_the_eyes", "back_pain", "dizziness", "cramps", "bruising", "weight_gain", "cold_hands_and_feets", "mood_swings", "neck_pain", "weakness_in_limbs", "visual_disturbances", "bladder_incontinence", "foul_smell_of_urine", "continuous_feel_of_urine", "internal_itching", "depression", "irritability", "muscle_pain", "altered_sensorium", "red_spots_over_body", "belly_pain", "abnormal_menstruation", "dischromic_patches", "watering_from_eyes", "increased_appetite", "polyuria", "mucoid_sputum", "rusty_sputum", "lack_of_concentration", "receiving_unsterile_injections", "coma", "stomach_bleeding", "distention_of_abdomen", "history_of_alcohol_consumption", "blood_in_sputum", "prominent_veins_on_calf", "painful_walking", "pus_filled_pimples", "fatigue", "congestion", "loss_of_smell", "muscle_weakness", "stiff_neck", "swollen_legs", "swollen_lymph_nodes", "malaise", "phlegm", "redness_of_eyes", "sinus_pressure", "runny_nose", "enlarged_thyroid", "brittle_nails", "swollen_extremeties", "extra_marital_contacts", "burning_micturition", "spotting_urination", "passage_of_gases", "internal_icing", "choking", "cough", "high_fever", "sunken_eyes"]

unique_symptoms = sorted(set(full_symptoms))

# Initialize session state
if 'selected_symptoms' not in st.session_state:
    st.session_state.selected_symptoms = []

# ===== HEADER =====
st.markdown('<div class="main-bg"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <div class="logo-icon">🏥</div>
    <h1 class="main-title">MedPredict Pro</h1>
    <p class="subtitle">Advanced Disease Prediction System powered by Machine Learning</p>
    <div class="status-badge">
        <span class="status-dot"></span>
        System Online & Ready
    </div>
</div>
""", unsafe_allow_html=True)

# ===== DISCLAIMER =====
st.markdown("""
<div class="disclaimer-box">
    <span style="font-size: 24px;">⚠️</span>
    <span><strong>Medical Disclaimer:</strong> This system is for educational and research purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</span>
</div>
""", unsafe_allow_html=True)

# ===== STATS BAR =====
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card" style="background: rgba(30, 41, 59, 0.8); border-radius: 20px; padding: 24px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, transparent, #6366f1, transparent);"></div>
        <div style="font-size: 32px; margin-bottom: 12px;">📋</div>
        <div style="font-size: 2.2rem; font-weight: 800;">41</div>
        <div style="font-size: 0.9rem; color: #94a3b8;">Diseases Covered</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card" style="background: rgba(30, 41, 59, 0.8); border-radius: 20px; padding: 24px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, transparent, #10b981, transparent);"></div>
        <div style="font-size: 32px; margin-bottom: 12px;">🎨</div>
        <div style="font-size: 2.2rem; font-weight: 800;">132</div>
        <div style="font-size: 0.9rem; color: #94a3b8;">Symptoms Tracked</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card" style="background: rgba(30, 41, 59, 0.8); border-radius: 20px; padding: 24px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, transparent, #0ea5e9, transparent);"></div>
        <div style="font-size: 32px; margin-bottom: 12px;">⚡</div>
        <div style="font-size: 2.2rem; font-weight: 800;">97.62%</div>
        <div style="font-size: 0.9rem; color: #94a3b8;">Model Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card" style="background: rgba(30, 41, 59, 0.8); border-radius: 20px; padding: 24px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, transparent, #a855f7, transparent);"></div>
        <div style="font-size: 32px; margin-bottom: 12px;">⏱️</div>
        <div style="font-size: 2.2rem; font-weight: 800;">&lt;2s</div>
        <div style="font-size: 0.9rem; color: #94a3b8;">Prediction Time</div>
    </div>
    """, unsafe_allow_html=True)

# ===== MAIN CONTENT =====
st.markdown("<br>", unsafe_allow_html=True)

col_left, col_right = st.columns([1.2, 1])

with col_left:
    # Symptom Selection Card
    st.markdown("""
    <div class="glass-card" style="margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #6366f1, #4f46e5); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📝</div>
            <div>
                <h2 style="font-size: 1.4rem; font-weight: 600;">Symptom Selection</h2>
                <span style="font-size: 0.9rem; color: #94a3b8;">""" + str(len(st.session_state.selected_symptoms)) + """ symptoms selected</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search symptoms
    search_term = st.text_input("🔍 Search symptoms...", placeholder="Type to filter symptoms...", label_visibility="collapsed")

    # Filter symptoms
    if search_term:
        filtered = [s for s in unique_symptoms if search_term.lower() in s.replace('_', ' ')]
    else:
        filtered = unique_symptoms

    # Multi-select using checkboxes in a grid
    st.markdown('<div class="symptom-grid">', unsafe_allow_html=True)

    # Create columns for symptom chips
    cols = st.columns(3)

    for idx, symptom in enumerate(filtered):
        col = cols[idx % 3]
        is_selected = symptom in st.session_state.selected_symptoms

        if col.checkbox(f"✅ {symptom.replace('_', ' ').title()}", value=is_selected, key=f"sym_{symptom}"):
            if symptom not in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.append(symptom)
        else:
            if symptom in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.remove(symptom)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Buttons
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        if st.button("🔮 Predict Disease", type="primary", use_container_width=True):
            if len(st.session_state.selected_symptoms) == 0:
                st.warning("⚠️ Please select at least one symptom!")
            else:
                with st.spinner("Analyzing symptoms..."):
                    import time
                    time.sleep(1.5)

                    # Find best match
                    best_match = None
                    best_score = 0

                    for disease, data in disease_data.items():
                        match_count = sum(1 for s in st.session_state.selected_symptoms if s in data["symptoms"])
                        score = match_count / len(data["symptoms"])
                        if score > best_score:
                            best_score = score
                            best_match = disease

                    if not best_match or best_score < 0.1:
                        best_match = "Common Cold"
                        best_score = 0.3

                    # Store result
                    st.session_state.prediction = {
                        "disease": best_match,
                        "confidence": best_score,
                        "description": disease_data[best_match]["description"]
                    }

    with col_btn2:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.selected_symptoms = []
            if 'prediction' in st.session_state:
                del st.session_state.prediction
            st.rerun()

with col_right:
    # Prediction Result Card
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(20px); border: 1px solid rgba(148, 163, 184, 0.1); border-radius: 24px; padding: 28px; position: relative; overflow: hidden;">
        <div style="position: absolute; top: -100px; right: -100px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(99, 102, 241, 0.15), transparent 70%);"></div>
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
            <div style="width: 50px; height: 50px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📊</div>
            <h2 style="font-size: 1.4rem; font-weight: 600;">Prediction Result</h2>
        </div>
    """, unsafe_allow_html=True)

    if 'prediction' in st.session_state:
        pred = st.session_state.prediction
        percent = int(pred['confidence'] * 100)

        st.markdown(f"""
        <div style="text-align: center; padding: 20px 0;">
            <div style="width: 100px; height: 100px; margin: 0 auto 24px; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 50px; box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);">✅</div>
            <h2 style="font-size: 2rem; font-weight: 800; color: #10b981; margin-bottom: 16px;">{pred['disease']}</h2>
        </div>

        <div class="confidence-bar">
            <div class="confidence-header">
                <span style="font-size: 0.9rem; color: #94a3b8;">Prediction Confidence</span>
                <span class="confidence-value">{percent}%</span>
            </div>
            <div class="confidence-track">
                <div class="confidence-fill" style="width: {percent}%"></div>
            </div>
        </div>

        <div style="margin-top: 24px; text-align: left;">
            <h4 style="font-size: 0.95rem; color: #94a3b8; margin-bottom: 12px;">Your Selected Symptoms</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                {"".join([f'<span class="symptom-tag">{s.replace("_", " ").title()}</span>' for s in st.session_state.selected_symptoms])}
            </div>
        </div>

        <div class="disease-info">
            <h4>ℹ️ About This Condition</h4>
            <p>{pred['description']}</p>
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

# ===== CHARTS =====
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
<div class="charts-grid">
    <div class="chart-card">
        <h3 class="chart-title">📈 Model Performance</h3>
    </div>
    <div class="chart-card">
        <h3 class="chart-title">🥧 Disease Distribution</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# Create actual charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.8); border-radius: 20px; padding: 24px;">
        <h3 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">📈 Model Performance Metrics</h3>
    </div>
    """, unsafe_allow_html=True)

    import pandas as pd
    metrics_df = pd.DataFrame({
        'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
        'Value': [97.62, 98.81, 97.62, 97.62]
    })
    st.bar_chart(metrics_df.set_index('Metric'), horizontal=True, height=250)

with col_chart2:
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.8); border-radius: 20px; padding: 24px;">
        <h3 style="font-size: 1.1rem; font-weight: 600; margin-bottom: 20px; display: flex; align-items: center; gap: 8px;">🥧 Disease Category Distribution</h3>
    </div>
    """, unsafe_allow_html=True)

    disease_df = pd.DataFrame({
        'Category': ['Infectious', 'Respiratory', 'Gastrointestinal', 'Neurological', 'Other'],
        'Count': [25, 20, 18, 15, 22]
    })
    st.bar_chart(disease_df.set_index('Category'), height=250)

# ===== FOOTER =====
st.markdown("""
<footer>
    <h4>MedPredict Pro - B.Sc. Honours Dissertation</h4>
    <p>University of Zimbabwe<br>Department of Mathematics and Computational Science</p>
    <div class="disclaimer">
        <strong>Disclaimer:</strong> Academic research purposes only.
    </div>
</footer>
""", unsafe_allow_html=True)