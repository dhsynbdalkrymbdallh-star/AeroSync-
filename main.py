import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="AeroSync AI", description="Aviation Maintenance Diagnostic Engine")

class DiagnosticRequest(BaseModel):
    system_name: str
    symptom: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AeroSync AI - Aviation Diagnostics</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f4f6f9; color: #333; margin: 0; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
            h1 { color: #1e3a8a; font-size: 24px; margin-bottom: 5px; }
            p.subtitle { color: #666; font-size: 14px; margin-bottom: 25px; }
            label { font-weight: bold; display: block; margin-top: 15px; margin-bottom: 5px; color: #374151; }
            input, textarea { width: 100%; padding: 10px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 14px; box-sizing: border-box; }
            button { background-color: #2563eb; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; width: 100%; margin-top: 20px; transition: background 0.2s; }
            button:hover { background-color: #1d4ed8; }
            .result-box { margin-top: 25px; padding: 15px; background: #eff6ff; border-left: 4px solid #2563eb; border-radius: 4px; display: none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>AeroSync AI</h1>
            <p class="subtitle">Aviation Maintenance & Diagnostic Assistant</p>
            
            <form id="diagForm">
                <label for="system">Aircraft System / Component:</label>
                <input type="text" id="system" name="system" placeholder="e.g., Hydraulic System, Avionics, Engine #1" required>
                
                <label for="symptom">Observed Symptom / Fault Code:</label>
                <textarea id="symptom" name="symptom" rows="4" placeholder="Describe the fault or error code..." required></textarea>
                
                <button type="submit">Run Diagnostic Analysis</button>
            </form>

            <div id="resultBox" class="result-box">
                <h3>Diagnostic Recommendation:</h3>
                <p id="resultText"></p>
            </div>
        </div>

        <script>
            document.getElementById('diagForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                const system = document.getElementById('system').value;
                const symptom = document.getElementById('symptom').value;

                const response = await fetch('/api/diagnose', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ system_name: system, symptom: symptom })
                });

                const data = await response.json();
                const resultBox = document.getElementById('resultBox');
                const resultText = document.getElementById('resultText');
                
                resultText.innerHTML = `<strong>Status:</strong> ${data.status}<br><strong>Analysis:</strong> ${data.analysis}<br><strong>Recommended Action:</strong> ${data.action}`;
                resultBox.style.display = 'block';
            });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/api/diagnose")
def diagnose_fault(req: DiagnosticRequest):
    fault_lower = req.symptom.lower()
    if "pressure" in fault_lower or "ضغط" in fault_lower:
        action = "Check hydraulic lines for leaks, inspect pump seals, and verify accumulator pre-charge pressure per AMM Chapter 29."
    elif "temp" in fault_lower or "حرارة" in fault_lower:
        action = "Inspect thermal sensors, check cooling air intake blockage, and review EGT limits in accordance with troubleshooting manual."
    else:
        action = f"Perform standard BITE test for {req.system_name}, isolate affected LRU (Line Replaceable Unit), and cross-check fault history in MCDU."

    return {
        "status": "Success",
        "system": req.system_name,
        "analysis": f"Evaluated symptom: '{req.symptom}' against historical maintenance guidelines.",
        "action": action
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

