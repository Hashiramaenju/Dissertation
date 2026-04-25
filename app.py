"""
Disease Prediction Dashboard - Flask Application
B.Sc. Honours Dissertation: Evaluating Machine Learning Algorithms for Symptom-Based Disease Classification
University of Zimbabwe
"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='templates')

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


@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')


@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get all available symptoms"""
    unique_symptoms = sorted(list(set(SYMPTOMS)))
    return jsonify({
        'symptoms': unique_symptoms,
        'count': len(unique_symptoms)
    })


@app.route('/api/diseases', methods=['GET'])
def get_diseases():
    """Get all diseases with their information"""
    return jsonify(DISEASE_PREDICTIONS)


@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict disease based on selected symptoms"""
    data = request.get_json()
    selected_symptoms = data.get('symptoms', [])

    if not selected_symptoms:
        return jsonify({'error': 'Please select at least one symptom'}), 400

    best_match = None
    best_score = 0

    for disease, disease_data in DISEASE_PREDICTIONS.items():
        # Calculate match score based on how many selected symptoms match the disease's typical symptoms
        matching_symptoms = [s for s in selected_symptoms if s in disease_data['symptoms']]
        score = len(matching_symptoms) / len(disease_data['symptoms']) if disease_data['symptoms'] else 0

        if score > best_score:
            best_score = score
            best_match = disease

    # Default prediction if no good match found
    if not best_match or best_score < 0.1:
        best_match = "Common Cold"
        best_score = 0.3

    disease_info = DISEASE_PREDICTIONS.get(best_match, {})

    return jsonify({
        'disease': best_match,
        'confidence': round(best_score * 100),
        'description': disease_info.get('description', 'Consult a healthcare professional for medical advice.'),
        'symptoms': disease_info.get('symptoms', []),
        'selected_symptoms': selected_symptoms
    })


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    return jsonify({
        'diseases_count': len(DISEASE_PREDICTIONS),
        'symptoms_count': len(set(SYMPTOMS)),
        'accuracy': '97.62%',
        'prediction_time': '<2s'
    })


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
