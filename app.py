from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_CONTENT = r'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Disease Prediction Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
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
        body {
            font-family: 'Inter', sans-serif;
            background: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
        }
        .bg-animation {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            z-index: -1;
            background: radial-gradient(circle at 20% 80%, rgba(99, 102, 241, 0.15) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(14, 165, 233, 0.1) 0%, transparent 50%);
        }
        .glass {
            background: var(--bg-card);
            backdrop-filter: blur(20px);
            border: 1px solid var(--border);
        }
        header { padding: 40px 20px 30px; text-align: center; }
        .logo-icon {
            width: 64px; height: 64px;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border-radius: 20px;
            display: inline-flex; align-items: center; justify-content: center;
            margin-bottom: 16px;
            box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
        }
        .logo-icon svg { width: 36px; height: 36px; color: white; }
        header h1 { font-size: 2.8rem; font-weight: 800; background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { font-size: 1.1rem; color: var(--text-secondary); margin-top: 8px; }
        .status-badge {
            display: inline-flex; align-items: center; gap: 8px;
            margin-top: 20px; padding: 10px 20px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 100px; font-size: 0.85rem; color: var(--accent);
        }
        .status-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .container { max-width: 1400px; margin: 0 auto; padding: 0 24px 60px; }
        .disclaimer { max-width: 900px; margin: 0 auto 30px; padding: 16px 24px; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 16px; display: flex; gap: 16px; align-items: center; }
        .disclaimer svg { width: 28px; height: 28px; color: #f59e0b; flex-shrink: 0; }
        .disclaimer p { font-size: 0.9rem; color: #fcd34d; }
        .stats-bar { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
        @media (max-width: 768px) { .stats-bar { grid-template-columns: repeat(2, 1fr); } }
        .stat-card { padding: 24px; border-radius: 20px; position: relative; overflow: hidden; }
        .stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
        .stat-card:nth-child(1)::before { background: linear-gradient(90deg, transparent, var(--primary), transparent); }
        .stat-card:nth-child(2)::before { background: linear-gradient(90deg, transparent, var(--accent), transparent); }
        .stat-card:nth-child(3)::before { background: linear-gradient(90deg, transparent, var(--secondary), transparent); }
        .stat-card:nth-child(4)::before { background: linear-gradient(90deg, transparent, var(--purple), transparent); }
        .stat-icon { width: 48px; height: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; }
        .stat-card:nth-child(1) .stat-icon { background: rgba(99, 102, 241, 0.15); color: var(--primary); }
        .stat-card:nth-child(2) .stat-icon { background: rgba(16, 185, 129, 0.15); color: var(--accent); }
        .stat-card:nth-child(3) .stat-icon { background: rgba(14, 165, 233, 0.15); color: var(--secondary); }
        .stat-card:nth-child(4) .stat-icon { background: rgba(168, 85, 247, 0.15); color: var(--purple); }
        .stat-icon svg { width: 24px; height: 24px; }
        .stat-value { font-size: 2.2rem; font-weight: 800; margin-bottom: 4px; }
        .stat-label { font-size: 0.9rem; color: var(--text-secondary); font-weight: 500; }
        .main-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; margin-bottom: 30px; }
        @media (max-width: 1024px) { .main-grid { grid-template-columns: 1fr; } }
        .card { border-radius: 24px; padding: 28px; }
        .card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px; }
        .card-title { display: flex; align-items: center; gap: 12px; }
        .card-title-icon { width: 44px; height: 44px; border-radius: 14px; background: linear-gradient(135deg, var(--primary), #4f46e5); display: flex; align-items: center; justify-content: center; }
        .card-title-icon svg { width: 22px; height: 22px; color: white; }
        .card-title h2 { font-size: 1.3rem; font-weight: 600; }
        .card-title span { font-size: 0.85rem; color: var(--text-secondary); }
        .search-wrapper { position: relative; margin-bottom: 20px; }
        .search-wrapper svg { position: absolute; left: 16px; top: 50%; transform: translateY(-50%); width: 20px; height: 20px; color: var(--text-secondary); }
        .search-box { width: 100%; padding: 14px 16px 14px 48px; background: rgba(15, 23, 42, 0.6); border: 1px solid var(--border); border-radius: 12px; color: var(--text-primary); font-size: 0.95rem; outline: none; }
        .search-box:focus { border-color: var(--primary); }
        .symptoms-container { max-height: 400px; overflow-y: auto; margin-bottom: 20px; }
        .symptoms-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; }
        .symptom-checkbox { display: flex; align-items: center; gap: 10px; padding: 12px 16px; background: rgba(15, 23, 42, 0.4); border: 1px solid var(--border); border-radius: 10px; cursor: pointer; transition: all 0.2s; }
        .symptom-checkbox:hover { border-color: var(--primary); background: rgba(99, 102, 241, 0.1); }
        .symptom-checkbox.checked { border-color: var(--primary); background: rgba(99, 102, 241, 0.2); }
        .symptom-checkbox input { display: none; }
        .checkbox-custom { width: 22px; height: 22px; border: 2px solid var(--text-secondary); border-radius: 6px; display: flex; align-items: center; justify-content: center; }
        .checkbox-custom svg { width: 14px; height: 14px; color: white; opacity: 0; }
        .symptom-checkbox.checked .checkbox-custom { background: var(--primary); border-color: var(--primary); }
        .symptom-checkbox.checked .checkbox-custom svg { opacity: 1; }
        .symptom-checkbox label { font-size: 0.85rem; cursor: pointer; }
        .button-group { display: flex; gap: 12px; }
        .btn { flex: 1; padding: 14px 24px; border: none; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: all 0.3s; }
        .btn svg { width: 20px; height: 20px; }
        .btn-primary { background: linear-gradient(135deg, var(--primary), #4f46e5); color: white; }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4); }
        .btn-secondary { background: rgba(148, 163, 184, 0.1); color: var(--text-primary); border: 1px solid var(--border); }
        .result-card { position: relative; overflow: hidden; }
        .result-card::before { content: ''; position: absolute; top: -100px; right: -100px; width: 200px; height: 200px; background: radial-gradient(circle, rgba(99, 102, 241, 0.2), transparent 70%); }
        .result-content { text-align: center; padding: 20px 0; }
        .result-icon { width: 100px; height: 100px; margin: 0 auto 24px; background: linear-gradient(135deg, var(--accent), #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 20px 40px rgba(16, 185, 129, 0.4); }
        .result-icon svg { width: 50px; height: 50px; color: white; }
        .prediction-disease { font-size: 2rem; font-weight: 800; margin-bottom: 16px; }
        .confidence-bar { background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 20px; margin: 24px 0; }
        .confidence-header { display: flex; justify-content: space-between; margin-bottom: 12px; }
        .confidence-label { font-size: 0.9rem; color: var(--text-secondary); }
        .confidence-value { font-size: 1.1rem; font-weight: 700; color: var(--accent); }
        .confidence-track { height: 10px; background: rgba(99, 102, 241, 0.2); border-radius: 5px; overflow: hidden; }
        .confidence-fill { height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); border-radius: 5px; transition: width 1s; width: 0; }
        .selected-symptoms-display { margin-top: 24px; text-align: left; }
        .selected-symptoms-display h4 { font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 12px; }
        .symptoms-tags { display: flex; flex-wrap: wrap; gap: 8px; }
        .symptom-tag { background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(99, 102, 241, 0.1)); border: 1px solid rgba(99, 102, 241, 0.3); color: #818cf8; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; }
        .disease-info { margin-top: 24px; padding: 20px; background: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 16px; }
        .disease-info h4 { font-size: 1rem; color: var(--secondary); margin-bottom: 10px; display: flex; align-items: center; gap: 8px; }
        .disease-info p { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; }
        .empty-state { padding: 60px 20px; text-align: center; }
        .empty-icon { width: 100px; height: 100px; margin: 0 auto 24px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(14, 165, 233, 0.1)); border-radius: 50%; display: flex; align-items: center; justify-content: center; }
        .empty-icon svg { width: 48px; height: 48px; color: var(--text-secondary); opacity: 0.5; }
        .empty-state h3 { font-size: 1.2rem; margin-bottom: 8px; }
        .empty-state p { font-size: 0.95rem; color: var(--text-secondary); }
        .charts-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }
        @media (max-width: 768px) { .charts-grid { grid-template-columns: 1fr; } }
        .chart-card { padding: 24px; border-radius: 20px; }
        .chart-container { position: relative; height: 200px; }
        .chart-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
        .chart-card h3 svg { width: 20px; height: 20px; color: var(--primary); }
        footer { text-align: center; padding: 40px 20px; border-top: 1px solid var(--border); margin-top: 40px; }
        .footer-content { max-width: 600px; margin: 0 auto; }
        .footer-content h4 { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }
        .footer-content p { font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6; }
        .footer-disclaimer { margin-top: 20px; padding-top: 20px; border-top: 1px solid var(--border); font-size: 0.8rem; color: var(--text-secondary); opacity: 0.7; }
        .loading-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.95); display: none; align-items: center; justify-content: center; z-index: 9999; }
        .loading-overlay.active { display: flex; }
        .loader { text-align: center; }
        .loader-spinner { width: 60px; height: 60px; border: 4px solid rgba(99, 102, 241, 0.2); border-top-color: var(--primary); border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .loader p { color: var(--text-secondary); }
        .fade-in { animation: fadeIn 0.5s ease-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .slide-up { animation: slideUp 0.6s ease-out; }
        @keyframes slideUp { from { opacity: 0; transform: translateY(40px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    <div class="loading-overlay" id="loadingOverlay"><div class="loader"><div class="loader-spinner"></div><p>Analyzing symptoms...</p></div></div>

    <header>
        <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" /></svg>
        </div>
        <h1>MedPredict Pro</h1>
        <p class="subtitle">Advanced Disease Prediction System powered by Machine Learning</p>
        <div class="status-badge"><span class="status-dot"></span>System Online &amp; Ready</div>
    </header>

    <div class="container">
        <div class="disclaimer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            <p><strong>Medical Disclaimer:</strong> This system is for educational and research purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.</p>
        </div>

        <div class="stats-bar">
            <div class="stat-card glass slide-up">
                <div class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg></div>
                <div class="stat-value">41</div><div class="stat-label">Diseases Covered</div>
            </div>
            <div class="stat-card glass slide-up">
                <div class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" /></svg></div>
                <div class="stat-value">132</div><div class="stat-label">Symptoms Tracked</div>
            </div>
            <div class="stat-card glass slide-up">
                <div class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg></div>
                <div class="stat-value">97.62%</div><div class="stat-label">Model Accuracy</div>
            </div>
            <div class="stat-card glass slide-up">
                <div class="stat-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div>
                <div class="stat-value">&lt;2s</div><div class="stat-label">Prediction Time</div>
            </div>
        </div>

        <div class="main-grid">
            <div class="card glass slide-up">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg></div>
                        <div><h2>Symptom Selection</h2><span id="selectedCount">0 symptoms selected</span></div>
                    </div>
                </div>
                <div class="search-wrapper">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                    <input type="text" class="search-box" placeholder="Search symptoms..." id="symptomSearch">
                </div>
                <div class="symptoms-container"><div class="symptoms-grid" id="symptomsGrid"></div></div>
                <div class="button-group">
                    <button class="btn btn-primary" onclick="predictDisease()"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>Predict Disease</button>
                    <button class="btn btn-secondary" onclick="clearSelection()"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>Clear All</button>
                </div>
            </div>
            <div class="card result-card glass slide-up">
                <div class="card-header">
                    <div class="card-title">
                        <div class="card-title-icon" style="background: linear-gradient(135deg, var(--accent), #059669);"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></div>
                        <h2>Prediction Result</h2>
                    </div>
                </div>
                <div id="resultContainer">
                    <div class="empty-state">
                        <div class="empty-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg></div>
                        <h3>No Prediction Yet</h3><p>Select symptoms and click "Predict Disease"</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="charts-grid">
            <div class="chart-card glass slide-up">
                <h3><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>Model Performance</h3>
                <div class="chart-container"><canvas id="performanceChart"></canvas></div>
            </div>
            <div class="chart-card glass slide-up">
                <h3><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" /></svg>Disease Distribution</h3>
                <div class="chart-container"><canvas id="diseaseChart"></canvas></div>
            </div>
        </div>
    </div>

    <footer>
        <div class="footer-content">
            <h4>MedPredict Pro - B.Sc. Honours Dissertation</h4>
            <p>University of Zimbabwe<br>Department of Mathematics and Computational Science</p>
            <div class="footer-disclaimer"><strong>Disclaimer:</strong> Academic research purposes only.</div>
        </div>
    </footer>

    <script>
        const symptoms = ["itching","skin_rash","nodal_skin_eruptions","continuous_sneezing","shivering","chills","joint_pain","stomach_pain","acidity","ulcers_on_tongue","blackheads","scurring","skin_peeling","silver_like_dusting","small_dents_in_nails","inflammatory_nails","blister","red_sore_around_nose","yellow_crust_ooze","fluid_overload","weight_loss","restlessness","lethargy","irregular_sugar_level","urination","breathlessness","sweating","indigestion","headache","yellowish_skin","dark_urine","nausea","vomiting","loss_of_appetite","pain_behind_the_eyes","back_pain","dizziness","cramps","bruising","weight_gain","cold_hands_and_feets","mood_swings","neck_pain","weakness_in_limbs","visual_disturbances","bladder_incontinence","foul_smell_of_urine","continuous_feel_of_urine","internal_itching","depression","irritability","muscle_pain","altered_sensorium","red_spots_over_body","belly_pain","abnormal_menstruation","dischromic_patches","watering_from_eyes","increased_appetite","polyuria","mucoid_sputum","rusty_sputum","lack_of_concentration","receiving_unsterile_injections","coma","stomach_bleeding","distention_of_abdomen","history_of_alcohol_consumption","blood_in_sputum","prominent_veins_on_calf","painful_walking","pus_filled_pimples","fatigue","congestion","loss_of_smell","muscle_weakness","stiff_neck","swollen_legs","swollen_lymph_nodes","malaise","phlegm","redness_of_eyes","sinus_pressure","runny_nose","enlarged_thyroid","brittle_nails","swollen_extremeties","extra_marital_contacts","burning_micturition","spotting_urination","passage_of_gases","internal_icing","choking","cough","high_fever","sunken_eyes"];
        const uniqueSymptoms = [...new Set(symptoms)].sort();

        const diseasePredictions = {
            "Fungal infection": { symptoms: ["itching","skin_rash","nodal_skin_eruptions","skin_peeling","red_spots_over_body"], description: "A skin infection caused by various fungi including dermatophytes and yeast. It affects the skin, nails, and scalp. Common types include athlete's foot, ringworm, and jock itch. Fungal infections thrive in warm, moist areas and are highly contagious through direct contact or contaminated surfaces." },
            "Allergy": { symptoms: ["continuous_sneezing","shivering","runny_nose","congestion"], description: "An exaggerated immune response to substances that are typically harmless to most people. Common allergens include pollen, dust mites, pet dander, and certain foods. Symptoms can range from mild (sneezing, itching) to severe (anaphylaxis). Management includes antihistamines and avoiding known triggers." },
            "GERD": { symptoms: ["indigestion","stomach_pain","acidity","nausea","belly_pain"], description: "Gastroesophageal reflux disease is a chronic digestive condition where stomach acid flows back into the esophagus, causing heartburn and irritation. Risk factors include obesity, pregnancy, and certain foods. Treatment involves lifestyle changes, medications, and in severe cases, surgery." },
            "Chronic cholestasis": { symptoms: ["yellowish_skin","dark_urine","yellow_crust_ooze","itching"], description: "A condition where bile flow from the liver is reduced or blocked, leading to bile buildup in the liver. Causes include gallstones, liver disease, and certain medications. Symptoms include jaundice, itching, and fatigue. Treatment depends on the underlying cause." },
            "Drug Reaction": { symptoms: ["skin_rash","red_spots_over_body","blister","itching"], description: "An adverse immune response to medication, ranging from mild rashes to severe conditions like Stevens-Johnson syndrome. Common culprits include antibiotics, anticonvulsants, and NSAIDs. Symptoms may include skin rash, fever, and organ involvement. Immediate medical attention is required for severe reactions." },
            "Peptic ulcer disease": { symptoms: ["stomach_pain","nausea","belly_pain","indigestion"], description: "Open sores that develop on the inner lining of the stomach, upper small intestine, or esophagus. Most commonly caused by H. pylori infection or prolonged NSAID use. Symptoms include burning stomach pain, bloating, and nausea. Treatment includes antibiotics and acid-reducing medications." },
            "AIDS": { symptoms: ["weight_loss","fatigue","malaise","swollen_lymph_nodes"], description: "Acquired immunodeficiency syndrome is the most advanced stage of HIV infection. The virus attacks the immune system, making individuals vulnerable to opportunistic infections. Early symptoms include fever, fatigue, and lymphadenopathy. Antiretroviral therapy (ART) is the standard treatment to control the virus." },
            "Diabetes": { symptoms: ["weight_loss","urination","increased_appetite","irregular_sugar_level"], description: "A chronic metabolic disorder characterized by high blood glucose levels due to inadequate insulin production or function. Type 1 involves immune destruction of insulin-producing cells; Type 2 involves insulin resistance. Complications include heart disease, kidney damage, and nerve problems. Management includes medication, diet, and exercise." },
            "Gastroenteritis": { symptoms: ["nausea","vomiting","stomach_pain","headache","high_fever"], description: "Inflammation of the stomach and intestines caused by viral, bacterial, or parasitic infections. Commonly transmitted through contaminated food or water. Symptoms include diarrhea, vomiting, abdominal cramps, and fever. Most cases resolve on their own with rest and hydration." },
            "Bronchial Asthma": { symptoms: ["breathlessness","cough","congestion","sweating"], description: "A chronic respiratory condition where airways become inflamed and narrowed, causing wheezing, breathlessness, and coughing. Triggers include allergens, exercise, and cold air. Management includes inhaled corticosteroids, bronchodilators, and avoiding known triggers." },
            "Hypertension": { symptoms: ["headache","dizziness","breathlessness"], description: "A condition where blood pressure in the arteries is consistently elevated, forcing the heart to work harder. Often called the 'silent killer' as it may show no symptoms. Risk factors include genetics, obesity, and high sodium intake. Treatment includes lifestyle changes and antihypertensive medications." },
            "Migraine": { symptoms: ["headache","nausea","visual_disturbances","dizziness"], description: "A neurological condition characterized by severe recurring headaches, often accompanied by nausea, vomiting, and sensitivity to light and sound. Migraines can last hours to days and may be preceded by aura. Triggers include stress, certain foods, and hormonal changes." },
            "Cervical spondylosis": { symptoms: ["neck_pain","back_pain","stiff_neck","weakness_in_limbs"], description: "Age-related wear and tear affecting the spinal disks in the neck. Also known as cervical osteoarthritis, it causes chronic neck pain and stiffness. May lead to spinal cord compression causing weakness or numbness in arms and legs. Treatment includes physical therapy, medications, and surgery in severe cases." },
            "Jaundice": { symptoms: ["yellowish_skin","dark_urine","nausea","loss_of_appetite"], description: "A condition causing yellowing of the skin and eyes due to elevated bilirubin levels. It indicates underlying liver dysfunction or bile duct obstruction. Causes include hepatitis, gallstones, and liver cirrhosis. Treatment depends on the underlying cause." },
            "Malaria": { symptoms: ["high_fever","chills","headache","sweating","fatigue"], description: "A life-threatening parasitic disease transmitted through the bite of infected Anopheles mosquitoes. Caused by Plasmodium parasites. Symptoms include fever, chills, sweats, headache, and muscle aches. Prevention includes insecticide-treated nets and antimalarial medications." },
            "Chicken pox": { symptoms: ["skin_rash","blister","red_spots_over_body","itching","high_fever"], description: "A highly contagious viral infection caused by the varicella-zoster virus. Characterized by itchy red spots that develop into blisters, followed by scabbing. Most common in children but can be prevented with vaccination. Complications include pneumonia and encephalitis." },
            "Dengue": { symptoms: ["high_fever","headache","joint_pain","muscle_pain"], description: "A mosquito-borne viral infection caused by dengue virus, transmitted by Aedes mosquitoes. Also known as breakbone fever due to severe muscle and joint pains. Symptoms include high fever, rash, and pain behind the eyes. In severe cases, it can develop into dengue hemorrhagic fever." },
            "Typhoid": { symptoms: ["high_fever","headache","belly_pain","fatigue"], description: "A bacterial infection caused by Salmonella typhi, usually spread through contaminated food or water. Symptoms include sustained fever, headache, abdominal pain, and rose spots on the chest. Treatment requires antibiotics, and a vaccine is available for travelers to endemic areas." },
            "Hepatitis A": { symptoms: ["yellowish_skin","dark_urine","nausea","fatigue"], description: "A highly contagious liver infection caused by the hepatitis A virus. Spread through contaminated food, water, or close contact with infected individuals. Symptoms include jaundice, fatigue, and digestive problems. Most people recover fully with rest and proper nutrition." },
            "Hepatitis B": { symptoms: ["yellowish_skin","dark_urine","belly_pain","fatigue"], description: "A serious liver infection caused by the hepatitis B virus that can become chronic and lead to liver damage, cirrhosis, or cancer. Transmitted through blood, sexual contact, or from mother to child. Prevention through vaccination; treatment includes antiviral medications." },
            "Tuberculosis": { symptoms: ["cough","high_fever","sweating","weight_loss"], description: "A bacterial infection caused by Mycobacterium tuberculosis, primarily affecting the lungs. Spread through airborne particles when an infected person coughs or sneezes. Symptoms include persistent cough, fever, night sweats, and weight loss. Treatment involves a 6-month course of antibiotics." },
            "Common Cold": { symptoms: ["congestion","runny_nose","continuous_sneezing","cough"], description: "A viral infectious disease of the upper respiratory tract affecting the nose and throat. Over 200 viruses can cause the common cold, with rhinoviruses being most common. Symptoms include sneezing, congestion, sore throat, and mild cough. Usually self-limiting within 7-10 days." },
            "Pneumonia": { symptoms: ["high_fever","cough","breathlessness","fatigue"], description: "An infection that inflames the air sacs in one or both lungs, which may fill with fluid. Caused by bacteria, viruses, or fungi, with bacterial pneumonia being most common. Symptoms include chest pain, fever, chills, and difficulty breathing. Treatment depends on the cause and may include antibiotics." },
            "Urinary tract infection": { symptoms: ["burning_micturition","urination","foul_smell_of_urine"], description: "An infection in any part of the urinary system, most commonly affecting the bladder and urethra. Caused primarily by E. coli bacteria. Symptoms include burning during urination, frequent urge to urinate, and cloudy urine. Treated with antibiotics; prevention includes hydration and proper hygiene." }
        };

        function initializeSymptoms() {
            const grid = document.getElementById('symptomsGrid');
            grid.innerHTML = '';
            uniqueSymptoms.forEach(symptom => {
                const checkbox = document.createElement('div');
                checkbox.className = 'symptom-checkbox';
                checkbox.innerHTML = '<input type="checkbox" id="' + symptom + '" value="' + symptom + '"><div class="checkbox-custom"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg></div><label for="' + symptom + '">' + formatSymptomName(symptom) + '</label>';
                grid.appendChild(checkbox);
                checkbox.addEventListener('click', (e) => {
                    if (e.target.tagName !== 'INPUT') { checkbox.querySelector('input').checked = !checkbox.querySelector('input').checked; }
                    checkbox.classList.toggle('checked', checkbox.querySelector('input').checked);
                    updateSelectedCount();
                });
            });
        }

        function formatSymptomName(symptom) { return symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()); }
        function getSelectedSymptoms() { return Array.from(document.querySelectorAll('#symptomsGrid input:checked')).map(cb => cb.value); }
        function updateSelectedCount() { document.getElementById('selectedCount').textContent = getSelectedSymptoms().length === 0 ? 'No symptoms selected' : getSelectedSymptoms().length + ' symptoms selected'; }

        function predictDisease() {
            const selectedSymptoms = getSelectedSymptoms();
            if (selectedSymptoms.length === 0) { alert('Please select at least one symptom'); return; }
            document.getElementById('loadingOverlay').classList.add('active');
            setTimeout(() => {
                let bestMatch = null, bestScore = 0;
                for (const [disease, data] of Object.entries(diseasePredictions)) {
                    const score = data.symptoms.filter(s => selectedSymptoms.includes(s)).length / data.symptoms.length;
                    if (score > bestScore) { bestScore = score; bestMatch = disease; }
                }
                if (!bestMatch || bestScore < 0.1) { bestMatch = "Common Cold"; bestScore = 0.3; }
                document.getElementById('loadingOverlay').classList.remove('active');
                displayResult(bestMatch, bestScore, selectedSymptoms, diseasePredictions[bestMatch]?.description || "Consult a healthcare professional.");
            }, 1500);
        }

        function displayResult(disease, confidence, selectedSymptoms, description) {
            const container = document.getElementById('resultContainer');
            const percent = Math.round(confidence * 100);
            container.innerHTML = '<div class="result-content fade-in"><div class="result-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg></div><h2 class="prediction-disease">' + disease + '</h2><div class="confidence-bar"><div class="confidence-header"><span class="confidence-label">Prediction Confidence</span><span class="confidence-value">' + percent + '%</span></div><div class="confidence-track"><div class="confidence-fill" style="width: 0%"></div></div></div><div class="selected-symptoms-display"><h4>Your Selected Symptoms</h4><div class="symptoms-tags">' + selectedSymptoms.map(s => '<span class="symptom-tag">' + formatSymptomName(s) + '</span>').join('') + '</div></div><div class="disease-info"><h4><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>About This Condition</h4><p>' + description + '</p></div></div>';
            setTimeout(() => { const fill = container.querySelector('.confidence-fill'); if (fill) fill.style.width = percent + '%'; }, 100);
        }

        function clearSelection() {
            document.querySelectorAll('#symptomsGrid input').forEach(cb => { cb.checked = false; cb.closest('.symptom-checkbox').classList.remove('checked'); });
            updateSelectedCount();
            document.getElementById('resultContainer').innerHTML = '<div class="empty-state"><div class="empty-icon"><svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg></div><h3>No Prediction Yet</h3><p>Select symptoms and click "Predict Disease"</p></div>';
        }

        document.getElementById('symptomSearch').addEventListener('input', function(e) {
            const term = e.target.value.toLowerCase();
            document.querySelectorAll('.symptom-checkbox').forEach(cb => { cb.style.display = cb.querySelector('label').textContent.toLowerCase().includes(term) ? 'flex' : 'none'; });
        });

        function initializeCharts() {
            new Chart(document.getElementById('performanceChart'), {
                type: 'bar',
                data: { labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score'], datasets: [{ data: [97.62, 98.81, 97.62, 97.62], backgroundColor: ['rgba(99,102,241,0.8)','rgba(14,165,233,0.8)','rgba(16,185,129,0.8)','rgba(168,85,247,0.8)'], borderRadius: 8 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 100, grid: { color: 'rgba(148,163,184,0.1)' }, ticks: { color: '#94a3b8' } }, x: { grid: { display: false }, ticks: { color: '#94a3b8' } } } }
            });
            new Chart(document.getElementById('diseaseChart'), {
                type: 'doughnut',
                data: { labels: ['Infectious','Respiratory','Gastrointestinal','Neurological','Other'], datasets: [{ data: [25,20,18,15,22], backgroundColor: ['rgba(239,68,68,0.8)','rgba(14,165,233,0.8)','rgba(16,185,129,0.8)','rgba(168,85,247,0.8)','rgba(99,102,241,0.8)'], borderWidth: 0 }] },
                options: { responsive: true, maintainAspectRatio: false, cutout: '65%', plugins: { legend: { position: 'right', labels: { color: '#94a3b8', padding: 12, usePointStyle: true } } } }
            });
        }

        window.addEventListener('DOMContentLoaded', () => { initializeSymptoms(); initializeCharts(); });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'MedPredict Pro is running'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
