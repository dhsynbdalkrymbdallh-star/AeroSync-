import os
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="AeroSync AI", description="Advanced Aviation Maintenance & Diagnostic Engine")

# --- Database Setup (SQLite) ---
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
        <title>AeroSync AI - Advanced Aviation Diagnostics</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }
            .container { max-width: 650px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1 { color: #1e3a8a; font-size: 24px; margin-bottom: 5px; }
            p.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
            label { font-weight: bold; display: block; margin-top: 15px; margin-bottom: 5px; color: #374151; }
            input, textarea, select { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
            button { background-color: #2563eb; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 20px; transition: background 0.2s; }
            button:hover { background-color: #1d4ed8; }
            .result-box { margin-top: 25px; padding: 15px; background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 4px; display: none; }
            .severity-aog { background: #fee2e2; border-left-color: #dc2626; color: #991b1b; padding: 8px; border-radius: 4px; font-weight: bold; margin-bottom: 10px; }
            .severity-crit { background: #fef3c7; border-left-color: #d97706; color: #92400e; padding: 8px; border-radius: 4px; font-weight: bold; margin-bottom: 10px; }
            .severity-min { background: #dcfce7; border-left-color: #16a34a; color: #166534; padding: 8px; border-radius: 4px; font-weight: bold; margin-bottom: 10px; }
            .history-section { margin-top: 30px; border-top: 1px solid #e5e7eb; padding-top: 15px; }
            .history-item { font-size: 12px; background: #f9fafb; padding: 8px; margin-bottom: 6px; border-radius: 4px; border: 1px solid #e5e7eb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AeroSync AI</h1>
            <p class="subtitle">EASA/FAA Compliant Intelligent Maintenance Diagnostic Engine</p>
            
            <form id="diagForm">
                <label for="tail_number">Aircraft Tail Number / Registration:</label>
                <input type="text" id="tail_number" name="tail_number" placeholder="e.g., ST-ASA, N12345" required>

                <label for="system">Aircraft System / Component:</label>
                <input type="text" id="system" name="system" placeholder="e.g., Hydraulic System, Avionics, Engine #1" required>
                
                <label for="symptom">Observed Symptom / Fault Code:</label>
                <textarea id="symptom" name="symptom" rows="3" placeholder="Describe the fault or error code..." required></textarea>

                <label for="lang">Language / اللغة:</label>
                <select id="lang" name="lang">
                    <option value="en">English (AMM Standard)</option>
                    <option value="ar">العربية (Arabic)</option>
                </select>
                
                <button type="submit">Run Advanced Diagnostic Analysis</button>
            </form>

            <div id="resultBox" class="result-box">
                <div id="severityBadge"></div>
                <h3>Diagnostic Recommendation & Report:</h3>
                <p id="resultText"></p>
            </div>

            <div class="history-section">
                <h3>Recent Diagnostic Logs</h3>
                <div id="historyList">Loading history...</div>
            </div>
        </div>

        <script>
            async function loadHistory() {
                try {
                    const res = await fetch('/api/history');
                    const data = await res.json();
                    const listDiv = document.getElementById('historyList');
                    if(data.logs && data.logs.length > 0) {
                        listDiv.innerHTML = data.logs.map(log => 
                            `<div class="history-item"><strong>[${log[1]}] Tail: ${log[2]}</strong> - System: ${log[3]} | Severity: <b>${log[5]}</b></div>`
                        ).join('');
                    } else {
                        listDiv.innerHTML = '<p style="font-size:12px; color:#666;">No prior logs found.</p>';
                    }
                } catch(e) {
                    document.getElementById('historyList').innerHTML = 'Could not load history.';
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
                if(data.severity === 'AOG - Aircraft on Ground') badgeClass = 'severity-aog';
                else if(data.severity === 'Critical') badgeClass = 'severity-crit';

                severityBadge.className = badgeClass;
                severityBadge.innerHTML = `Severity Level: ${data.severity}`;

                resultText.innerHTML = `<strong>Status:</strong> ${data.status}<br><strong>Tail Number:</strong> ${data.tail}<br><strong>Analysis:</strong> ${data.analysis}<br><strong>Recommended Action:</strong> ${data.action}`;
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
    
    # Severity & Risk Analysis Logic
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

    # Save to SQLite DB
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


