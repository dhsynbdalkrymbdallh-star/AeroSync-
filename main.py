import os
from fastapi import FastAPI

app = FastAPI(title="AeroSync AI", description="Aviation Maintenance Diagnostic Engine")

@app.get("/")
def read_root():
    return {"status": "online", "message": "AeroSync AI Cloud Server is running successfully."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
