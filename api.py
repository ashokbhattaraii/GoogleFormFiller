from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import os

# Import the GoogleFormSubmitter from the original script
from main import GoogleFormSubmitter

app = FastAPI(title="Google Form Filler API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Setup submitter
CONFIG_PATH = 'mapping_social.json'
try:
    submitter = GoogleFormSubmitter(CONFIG_PATH)
except FileNotFoundError:
    print(f"Warning: {CONFIG_PATH} not found. Please create it before running.")
    submitter = None

class FormData(BaseModel):
    data: List[Dict[str, Any]]
    config_path: Optional[str] = None

class JobStatus:
    def __init__(self):
        self.jobs = {}

    def create_job(self, job_id, total):
        self.jobs[job_id] = {
            "status": "processing",
            "total": total,
            "success": 0,
            "failed": 0,
            "completed": False
        }

    def update_job(self, job_id, success=True):
        if success:
            self.jobs[job_id]["success"] += 1
        else:
            self.jobs[job_id]["failed"] += 1
        
        if self.jobs[job_id]["success"] + self.jobs[job_id]["failed"] == self.jobs[job_id]["total"]:
            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["completed"] = True

    def get_job(self, job_id):
        return self.jobs.get(job_id)

job_manager = JobStatus()

def process_submissions(job_id: str, data_list: List[Dict[str, Any]], custom_submitter=None):
    active_submitter = custom_submitter or submitter
    if not active_submitter:
        job_manager.jobs[job_id]["status"] = "failed"
        job_manager.jobs[job_id]["error"] = "Submitter not configured properly."
        return

    import time
    for i, entry in enumerate(data_list, start=1):
        if active_submitter.submit(entry, index=i):
            job_manager.update_job(job_id, success=True)
        else:
            job_manager.update_job(job_id, success=False)
        time.sleep(2)  # Delay to prevent rate limiting

@app.post("/api/v1/submit")
async def submit_form(payload: FormData, background_tasks: BackgroundTasks):
    import uuid
    job_id = str(uuid.uuid4())
    
    custom_submitter = None
    if payload.config_path:
        if not os.path.exists(payload.config_path):
             raise HTTPException(status_code=400, detail=f"Config file not found: {payload.config_path}")
        custom_submitter = GoogleFormSubmitter(payload.config_path)
    
    if not submitter and not custom_submitter:
         raise HTTPException(status_code=500, detail="Default Submitter not configured and no config provided.")

    job_manager.create_job(job_id, len(payload.data))
    
    background_tasks.add_task(process_submissions, job_id, payload.data, custom_submitter)
    
    return {"message": "Form filling job started", "job_id": job_id, "total_records": len(payload.data)}


@app.get("/api/v1/status/{job_id}")
async def get_status(job_id: str):
    status = job_manager.get_job(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
