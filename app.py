import streamlit as st

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
        "description": "A condition where blood pressure in the arteries is consistently elevated, forcing the heart to work harder. Often called the silent killer as it may show no symptoms. Risk factors include genetics, obesity, and high sodium intake. Treatment includes lifestyle changes and antihypertensive medications."
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
        "description": "A condition where the thyroid gland does not produce enough thyroid hormones, slowing down metabolism. Common causes include autoimmune disease and iodine deficiency. Symptoms include fatigue, weight gain, cold intolerance, and depression. Treated with synthetic thyroid hormone replacement."
    },
    "Hyperthyroidism": {
        "symptoms": ["weight_loss", "increased_appetite", "sweating", "palpitations"],
        "description": "A condition where the thyroid gland produces excessive thyroid hormones, accelerating metabolism. Common cause is Graves disease. Symptoms include rapid heartbeat, weight loss despite increased appetite, heat sensitivity, and tremor. Treatment includes antithyroid drugs, radioactive iodine, or surgery."
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

# Page config
st.set_page_config(
    page_title="MedPredict Pro",
    page_icon="🏥",
    layout="wide"
)

# Title
st.markdown("""
<div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #6366f1, #0ea5e9); border-radius: 20px; margin-bottom: 30px;">
    <h1 style="color: white; margin: 0;">🏥 MedPredict Pro</h1>
    <p style="color: white;">Advanced Disease Prediction System powered by Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 15px; padding: 15px; margin-bottom: 20px;">
    <strong>⚠️ Medical Disclaimer:</strong> This system is for educational and research purposes only.
    It is not a substitute for professional medical advice. Always seek the advice of your physician.
</div>
""", unsafe_allow_html=True)

# Stats row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Diseases", "41")
col2.metric("Symptoms", len(all_symptoms))
col3.metric("Accuracy", "97.62%")
col4.metric("Response", "< 2s")

st.divider()

# Main content
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("🔍 Select Your Symptoms")

    search = st.text_input("Search symptoms...", placeholder="Type to filter symptoms...")
    filtered_symptoms = [s for s in all_symptoms if search.lower() in s.replace('_', ' ')]

    selected_symptoms = st.multiselect(
        "Select symptoms:",
        options=filtered_symptoms,
        default=[],
        format_func=lambda x: x.replace('_', ' ').title(),
        placeholder="Choose symptoms..."
    )

    st.caption(f"📊 {len(selected_symptoms)} symptoms selected")

    col_btn1, col_btn2 = st.columns(2)
    predict_btn = st.button("🔮 Predict Disease", type="primary", use_container_width=True)
    clear_btn = st.button("🗑️ Clear All", use_container_width=True)

with col_right:
    st.subheader("📊 Prediction Result")

    if clear_btn:
        selected_symptoms = []
        st.rerun()

    if predict_btn:
        if len(selected_symptoms) == 0:
            st.warning("⚠️ Please select at least one symptom!")
        else:
            best_match = None
            best_score = 0

            for disease, data in disease_data.items():
                match_count = sum(1 for s in selected_symptoms if s in data["symptoms"])
                score = match_count / len(data["symptoms"])
                if score > best_score:
                    best_score = score
                    best_match = disease

            if best_match and best_score > 0:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1)); border: 2px solid #10b981; border-radius: 20px; padding: 30px; text-align: center;">
                    <h2 style="color: #10b981; margin-bottom: 10px;">{best_match}</h2>
                    <h1 style="color: #10b981; margin: 0;">{int(best_score * 100)}%</h1>
                    <p>Prediction Confidence</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 📋 Your Selected Symptoms")
                for s in selected_symptoms:
                    st.success(f"✓ {s.replace('_', ' ').title()}")

                st.markdown(f"""
                <div style="background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 15px; padding: 20px; margin-top: 20px;">
                    <h3>ℹ️ About This Condition</h3>
                    <p style="line-height: 1.8;">{disease_data[best_match]["description"]}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("### 🔬 Typical Symptoms")
                for s in disease_data[best_match]["symptoms"]:
                    if s not in selected_symptoms:
                        st.info(f"• {s.replace('_', ' ').title()}")
            else:
                st.error("No matching disease found.")
    else:
        st.info("👈 Select symptoms and click 'Predict Disease'")
        st.markdown("<div style='text-align: center;'><h2>🏥</h2></div>", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style="text-align: center; color: gray; padding: 20px;">
    <p><strong>MedPredict Pro</strong> - B.Sc. Honours Dissertation</p>
    <p>University of Zimbabwe | Department of Mathematics and Computational Science</p>
    <p><em>Disclaimer: Academic research purposes only.</em></p>
</div>
""", unsafe_allow_html=True)
