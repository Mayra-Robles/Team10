from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ProjectManager import ProjectManager
import neo4j.time
from SQLInjectionManager import SQLInjectionManager
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS setup, insecure for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pm = ProjectManager(uri="neo4j://941e739f.databases.neo4j.io", user="neo4j", password="Team_Blue")

def serialize_datetime(obj):
    if isinstance(obj, neo4j.time.DateTime):
        return obj.iso_format()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

@app.get("/dashboard/{initials}")
async def dashboard(initials):
    lead_analyst_initials = "MR"
    my_projects = pm.get_my_projects(initials)
    shared_projects = pm.get_shared_projects(lead_analyst_initials)
    for project in my_projects:
        if "last_edit_date" in project and isinstance(project["last_edit_date"], neo4j.time.DateTime):
            project["last_edit_date"] = project["last_edit_date"].iso_format()
        if "Stamp_Date" in project and isinstance(project["Stamp_Date"], neo4j.time.DateTime):
            project["Stamp_Date"] = project["Stamp_Date"].iso_format()
        if "deleted_date" in project and isinstance(project["deleted_date"], neo4j.time.DateTime):
            project["deleted_date"]=project["deleted_date"].iso_format()
    for project in shared_projects:
        if "last_edit_date" in project and isinstance(project["last_edit_date"], neo4j.time.DateTime):
            project["last_edit_date"] = project["last_edit_date"].iso_format()
        if "Stamp_Date" in project and isinstance(project["Stamp_Date"], neo4j.time.DateTime):
            project["Stamp_Date"] = project["Stamp_Date"].iso_format()
    return {"my_projects": my_projects, "shared_projects": shared_projects}

@app.get("/folders/")
async def get_folders():
    result=pm.get_folders()
    for folders in result:
        if "creation_date" in folders and isinstance(folders["creation_date"], neo4j.time.DateTime):
            folders["creation_date"]=folders["creation_date"].iso_format()
    return {"my_folders": result}

@app.post("/delete/{projectName}")
async def delete_project(projectName:str):
    result=pm.delete_project(projectName)
    return result

@app.post("/restore/{projectName}")
async def restore_project(projectName: str):
    return pm.restore_project(projectName)

@app.post("/lock/{projectName}/{analyst_initials}")
async def lock_project(projectName: str, analyst_initials: str):
    analyst_initials = "MR"
    result = pm.lock_project(projectName, analyst_initials)
    return {"status": "success", "project": projectName}

@app.post("/unlock/{projectName}/{analyst_initials}")
async def unlock_project(projectName: str, analyst_initials:str):
    analyst_intials="MR"
    result = pm.unlock_project(projectName, analyst_initials)
    return {"status": "success", "project": projectName}

@app.post("/create/")
async def create_project(project_name: str = Form(...),
    description: str = Form(...),
    machine_IP: str = Form(...),
    status: str = Form(...),
    lead_analyst_initials: str = Form(...),
    locked: str = Form(...),
    files: list[UploadFile] = File(default=[])):
    result=pm.create_project(project_name, locked, description, machine_IP, status, lead_analyst_initials, files)
    return {"status": "success"}

@app.post("/analyst/{initials}/")
async def check_login(initials:str):
    result= pm.check_login(initials)
    return result

@app.get("/export/{projectName}")
async def export_project(projectName: str):
    try:
        result = pm.export_project(projectName)
        if result["status"] == "success":
            # Serialize any datetime objects in the result
            for project in [result["data"]["project"]]:
                if "stamp_date" in project and isinstance(project["stamp_date"], neo4j.time.DateTime):
                    project["stamp_date"] = project["stamp_date"].iso_format()
                if "last_edit_date" in project and isinstance(project["last_edit_date"], neo4j.time.DateTime):
                    project["last_edit_date"] = project["last_edit_date"].iso_format()
                if "deleted_date" in project and project["deleted_date"] and isinstance(project["deleted_date"], neo4j.time.DateTime):
                    project["deleted_date"] = project["deleted_date"].iso_format()
            return result
        else:
            return {"status": "failure", "error": result.get("error", "Failed to export project")}
    except Exception as e:
        return {"status": "failure", "error": f"Export failed: {str(e)}"}
    
@app.post("/api/sql_injection")
async def run_sql_injection(request: Request):
    data = await request.json()
    print("[SQLInjectionAPI] Received request:", data)

    target_url = data.get("target_url")
    port = data.get("port", 80)
    timeout = data.get("timeout", 5)
    headers = data.get("headers", {})
    enum_level = data.get("enum_level", 0)

    manager = SQLInjectionManager()
    result = manager.perform_sql_injection(
        target_url=target_url,
        port=port,
        timeout=timeout,
        headers=headers,
        enum_level=enum_level
    )

    return JSONResponse(content=result)