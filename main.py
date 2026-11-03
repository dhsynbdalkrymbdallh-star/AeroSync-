import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="AeroSync AI", description="Aviation Diagnostic & Engineering Platform")

DB_FILE = "aerosync_diagnostics.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnostics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            tail_number TEXT,
            system_name TEXT,
            symptom TEXT,
            severity TEXT,
            action TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class DiagnosticRequest(BaseModel):
    tail_number: str
    system_name: str
    symptom: str
    lang: str = "en"

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AeroSync AI - Next-Gen Aviation Intelligence</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg-primary: #0b132b;
                --bg-card: #1c2541;
                --accent-blue: #00b4d8;
                --accent-glow: #90e0ef;
                --text-main: #f8fafc;
                --text-muted: #94a3b8;
                --border-color: #3a506b;
                --border-radius: 12px;
            }

            * { box-sizing: border-box; margin: 0; padding: 0; }

            body {
                font-family: 'Roboto', -apple-system, sans-serif;
                background-color: var(--bg-primary);
                color: var(--text-main);
                min-height: 100vh;
                padding: 20px 12px;
                display: flex;
                justify-content: center;
                align-items: flex-start;
            }

            .app-container {
                width: 100%;
                max-width: 680px;
                background: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 16px;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.45);
                overflow: hidden;
                position: relative;
            }

            .header {
                background: linear-gradient(135deg, #0b132b 0%, #1c2541 100%);
                padding: 25px 20px 20px 20px;
                text-align: center;
                border-bottom: 2px solid var(--accent-blue);
                position: relative;
            }

            .brand-title {
                font-family: 'Orbitron', sans-serif;
                font-size: 26px;
                font-weight: 900;
                color: #ffffff;
                letter-spacing: 2px;
                text-transform: uppercase;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }

            .brand-title span {
                color: var(--accent-blue);
            }

            .brand-subtitle {
                font-size: 12px;
                color: var(--accent-glow);
                margin-top: 6px;
                letter-spacing: 1px;
                text-transform: uppercase;
                font-weight: 500;
            }

            /* Engineering Tabs */
            .nav-tabs {
                display: flex;
                background: #0b132b;
                border-bottom: 1px solid var(--border-color);
                padding: 4px;
            }

            .tab-btn {
                flex: 1;
                padding: 12px 8px;
                background: transparent;
                border: none;
                color: var(--text-muted);
                font-family: 'Orbitron', sans-serif;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
                cursor: pointer;
                border-radius: 8px;
                transition: all 0.3s ease;
                text-align: center;
            }

            .tab-btn.active {
                background: var(--accent-blue);
                color: #0b132b;
                box-shadow: 0 0 12px rgba(0, 180, 216, 0.4);
            }

            .tab-content {
                display: none;
                padding: 24px 20px;
            }

            .tab-content.active {
                display: block;
            }

            /* Form Elements */
            .form-group {
                margin-bottom: 18px;
            }

            label {
                display: block;
                font-size: 12px;
                font-weight: 500;
                color: var(--accent-glow);
                margin-bottom: 6px;
                text-transform: uppercase;
                letter-spacing: 0.8px;
            }

            input[type="text"], textarea, select {
                width: 100%;
                padding: 12px 14px;
                background: #0b132b;
                border: 1px solid var(--border-color);
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                transition: border-color 0.3s ease;
            }

            input[type="text"]:focus, textarea:focus, select:focus {
                outline: none;
                border-color: var(--accent-blue);
                box-shadow: 0 0 8px rgba(0, 180, 216, 0.3);
            }

            button.submit-btn {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #00b4d8 0%, #0077b6 100%);
                border: none;
                border-radius: 8px;
                color: #ffffff;
                font-family: 'Orbitron', sans-serif;
                font-size: 13px;
                font-weight: 700;
                letter-spacing: 1px;
                cursor: pointer;
                text-transform: uppercase;
                transition: transform 0.2s, box-shadow 0.2s;
                margin-top: 10px;
            }

            button.submit-btn:active {
                transform: scale(0.98);
            }

            /* Results Box */
            .result-box {
                margin-top: 25px;
                padding: 18px;
                background: #0b132b;
                border: 1px solid var(--border-color);
                border-radius: 10px;
                display: none;
                border-left: 4px solid var(--accent-blue);
            }

            .severity-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 20px;
                font-family: 'Orbitron', sans-serif;
                font-size: 11px;
                font-weight: 700;
                text-transform: uppercase;
                margin-bottom: 12px;
            }

            .severity-aog { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
            .severity-crit { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
            .severity-min { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; }

            /* Modern Cards */
            .eng-card {
                background: #0b132b;
                border: 1px solid var(--border-color);
                border-radius: 10px;
                padding: 16px;
                margin-bottom: 14px;
                position: relative;
            }

            .eng-card h4 {
                color: var(--accent-blue);
                font-size: 15px;
                margin-bottom: 8px;
                display: flex;
                align-items: center;
                gap: 8px;
            }

            .eng-card p {
                font-size: 13px;
                color: var(--text-muted);
                line-height: 1.5;
            }

            .history-item {
                font-size: 12px;
                background: #0b132b;
                padding: 10px 12px;
                margin-bottom: 8px;
                border-radius: 6px;
                border: 1px solid var(--border-color);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div class="header">
                <div class="brand-title">✈️ AeroSync <span>AI</span></div>
                <div class="brand-subtitle">EASA/FAA Maintenance & Qualification Hub</div>
            </div>

            <div class="nav-tabs">
                <button class="tab-btn active" onclick="switchTab(event, 'diag')">Diagnostics</button>
                <button class="tab-btn" onclick="switchTab(event, 'training')">Training Hub</button>
                <button class="tab-btn" onclick="switchTab(event, 'glossary')">Glossary</button>
            </div>

            <!-- TAB 1: DIAGNOSTICS -->
            <div id="diag" class="tab-content active">
                <form id="diagForm">
                    <div class="form-group">
                        <label for="tail_number">Tail Number / Aircraft Reg:</label>
                        <input type="text" id="tail_number" placeholder="e.g., ST-ASA, N12345" required>
                    </div>

                    <div class="form-group">
                        <label for="system">Aircraft System / Component:</label>
                        <input type="text" id="system" placeholder="e.g., Hydraulic System, Avionics, Engine #1" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="symptom">Observed Symptom / Fault Code:</label>
                        <textarea id="symptom" rows="3" placeholder="Describe fault code or anomaly..." required></textarea>
                    </div>

                    <div class="form-group">
                        <label for="lang">Language / لغة التقرير:</label>
                        <select id="lang">
                            <option value="en">English (AMM Technical Standard)</option>
                            <option value="ar">العربية (الشرح العربي المعتمد)</option>
                        </select>
                    </div>
                    
                    <button type="submit" class="submit-btn">Execute Diagnostic Engine</button>
                </form>

                <div id="resultBox" class="result-box">
                    <div id="severityBadge" class="severity-badge"></div>
                    <h3 style="color: var(--accent-blue); font-size: 15px; margin-bottom: 8px;">Analysis & Recommended Action:</h3>
                    <p id="resultText" style="font-size: 13px; line-height: 1.6; color: var(--text-main);"></p>
                </div>

                <div style="margin-top: 25px; border-top: 1px solid var(--border-color); padding-top: 15px;">
                    <h3 style="font-size: 14px; color: var(--accent-glow); margin-bottom: 12px; font-family: 'Orbitron', sans-serif;">Recent Maintenance Logs</h3>
                    <div id="historyList">Loading database history...</div>
                </div>
            </div>

            <!-- TAB 2: TRAINING -->
            <div id="training" class="tab-content">
                <h3 style="color: var(--accent-glow); font-size: 14px; margin-bottom: 15px; font-family: 'Orbitron', sans-serif;">Qualification & Training Modules</h3>
                
                <div class="eng-card">
                    <h4>🛠️ EASA Part-145 Maintenance Standards</h4>
                    <p>فهم وتطبيق ضوابط وإجراءات صيانة الطائرات المعتمدة دولياً وتطبيق معايير السلامة للجودة في خطوط الصيانة والحظائر (Hangars).</p>
                </div>
                <div class="eng-card">
                    <h4>📖 AMM & TSM Troubleshooting Workflows</h4>
                    <p>تدريب عملي على قراءة واستكشاف أعطال دليل صيانة الطائرة (Aircraft Maintenance Manual) ودليل استكشاف الأخطاء (Troubleshooting Manual).</p>
                </div>
                <div class="eng-card">
                    <h4>⚡ Avionics & LRU BITE Testing</h4>
                    <p>أساسيات فحص وإجراء الاختبارات الذاتية (BITE Tests) للأنظمة الإلكترونية والمحركات وعزل الوحدات التالفة (LRUs).</p>
                </div>
            </div>

            <!-- TAB 3: GLOSSARY -->
            <div id="glossary" class="tab-content">
                <h3 style="color: var(--accent-glow); font-size: 14px; margin-bottom: 15px; font-family: 'Orbitron', sans-serif;">Technical Aviation Glossary</h3>
                
                <div class="eng-card">
                    <h4>🚨 AOG (Aircraft on Ground)</h4>
                    <p><b>طائرة متوقفة عن العمل:</b> حالة حرج تمنع الطائرة من الطيران لحين استبدال أو إصلاح العطل.</p>
                </div>
                <div class="eng-card">
                    <h4>📋 AMM (Aircraft Maintenance Manual)</h4>
                    <p><b>دليل صيانة الطائرة:</b> المرجع الفني الذي يحتوي على خطوات الفحص والإصلاح المعتمدة.</p>
                </div>
                <div class="eng-card">
                    <h4>🔌 LRU (Line Replaceable Unit)</h4>
                    <p><b>وحدة قابلة للتبديل السريع:</b> عنصر يتم استبداله مباشرة على خط الصيانة لسرعة الجاهزية.</p>
                </div>
                <div class="eng-card">
                    <h4>📊 MEL (Minimum Equipment List)</h4>
                    <p><b>قائمة الحد الأدنى للمعدات:</b> قائمة تسمح بالطيران المؤقت مع وجود بعض الأعطال المحددة دون مساس بالسلامة.</p>
                </div>
            </div>
        </div>

        <script>
            function switchTab(evt, tabId) {
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.getElementById(tabId).classList.add('active');
                evt.currentTarget.classList.add('active');
            }

            async function loadHistory() {
                try {
                    const res = await fetch('/api/history');
                    const data = await res.json();
                    const listDiv = document.getElementById('historyList');
                    if(data.logs && data.logs.length > 0) {
                        listDiv.innerHTML = data.logs.map(log => 
                            `<div class="history-item">
                                <span><strong>[${log[2]}]</strong> ${log[3]}</span>
                                <span style="color: var(--accent-blue); font-weight: bold;">${log[5]}</span>
                             </div>`
                        ).join('');
                    } else {
                        listDiv.innerHTML = '<p style="font-size:12px; color: var(--text-muted);">No prior diagnostic entries found.</p>';
                    }
                } catch(e) {
                    document.getElementById('historyList').innerHTML = 'Error loading history.';
                }
            }

            document.getElementById('diagForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const tail = document.getElementById('tail_number').value;
                const system = document.getElementById('system').value;
                const symptom = document.getElementById('symptom').value;
                const lang = document.getElementById('lang').value;

                const response = await fetch('/api/diagnose', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ tail_number: tail, system_name: system, symptom: symptom, lang: lang })
                });

                const data = await response.json();
                const resultBox = document.getElementById('resultBox');
                const resultText = document.getElementById('resultText');
                const severityBadge = document.getElementById('severityBadge');
                
                let badgeClass = 'severity-min';
                if(data.severity.includes('AOG')) badgeClass = 'severity-aog';
                else if(data.severity.includes('Critical')) badgeClass = 'severity-crit';

                severityBadge.className = 'severity-badge ' + badgeClass;
                severityBadge.innerHTML = `Risk Status: ${data.severity}`;

                resultText.innerHTML = `<strong>Aircraft Tail:</strong> ${data.tail}<br><strong>Evaluation:</strong> ${data.analysis}<br><br><strong>Action Required:</strong> ${data.action}`;
                resultBox.style.display = 'block';
                loadHistory();
            });

            loadHistory();
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/api/diagnose")
def diagnose_fault(req: DiagnosticRequest):
    fault_lower = req.symptom.lower()
    
    if "pressure" in fault_lower or "ضغط" in fault_lower or "leak" in fault_lower:
        severity = "AOG - Aircraft on Ground"
        action_en = "Check hydraulic lines for leaks, inspect pump seals, and verify accumulator pre-charge pressure per AMM Chapter 29."
        action_ar = "فحص خطوط الهيدروليك بحثاً عن تسريبات، فحص سدادات المضخة، والتحقق من ضغط المركم وفقاً لدليل الصيانة AMM الفصل 29."
    elif "temp" in fault_lower or "حرارة" in fault_lower or "fire" in fault_lower:
        severity = "Critical"
        action_en = "Inspect thermal sensors, check cooling air intake blockage, and review EGT limits in accordance with troubleshooting manual."
        action_ar = "فحص المستشعرات الحرارية، التحقق من انسداد مدخل هواء التبريد، ومراجعة حدود حرارة العادم (EGT) طبقاً لدليل استكشاف الأخطاء."
    else:
        severity = "Minor"
        action_en = f"Perform standard BITE test for {req.system_name}, isolate affected LRU, and cross-check fault history in MCDU."
        action_ar = f"إجراء اختبار الفحص الذاتي BITE للنظام {req.system_name}، عزل الوحدة التالفة (LRU)، ومراجعة سجل الأعطال في شاشة MCDU."

    action = action_ar if req.lang == "ar" else action_en
    analysis = f"Evaluated symptom: '{req.symptom}' against EASA/FAA guidelines." if req.lang == "en" else f"تم تقييم العطل: '{req.symptom}' وفقاً لمعايير EASA/FAA."

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO diagnostics (timestamp, tail_number, system_name, symptom, severity, action)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, req.tail_number, req.system_name, req.symptom, severity, action))
    conn.commit()
    conn.close()

    return {
        "status": "Success",
        "tail": req.tail_number,
        "severity": severity,
        "analysis": analysis,
        "action": action
    }

@app.get("/api/history")
def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM diagnostics ORDER BY id DESC LIMIT 5')
    logs = cursor.fetchall()
    conn.close()
    return {"logs": logs}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)



