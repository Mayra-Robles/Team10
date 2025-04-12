from flask import Flask, Response
from flask_cors import CORS
from ProjectManager import ProjectManager
import neo4j.time
import json

app = Flask(__name__)
print("Initializing Flask app")
CORS(app)  # Keep as fallback
print("CORS initialized for all origins")

pm = ProjectManager(uri="neo4j://941e739f.databases.neo4j.io", user="neo4j", password="Team_Blue")

def serialize_datetime(obj):
    if isinstance(obj, neo4j.time.DateTime):
        return obj.iso_format()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

@app.route('/')
def dashboard():
    print("Handling GET / request")
    lead_analyst_initials = "MR"
    my_projects = pm.get_all_projects()
    shared_projects = pm.get_shared_projects(lead_analyst_initials)
    for project in my_projects:
        if "last_edit_date" in project and isinstance(project["last_edit_date"], neo4j.time.DateTime):
            project["last_edit_date"] = project["last_edit_date"].iso_format()
        if "Stamp_Date" in project and isinstance(project["Stamp_Date"], neo4j.time.DateTime):
            project["Stamp_Date"] = project["Stamp_Date"].iso_format()
    for project in shared_projects:
        if "last_edit_date" in project and isinstance(project["last_edit_date"], neo4j.time.DateTime):
            project["last_edit_date"] = project["last_edit_date"].iso_format()
        if "Stamp_Date" in project and isinstance(project["Stamp_Date"], neo4j.time.DateTime):
            project["Stamp_Date"] = project["Stamp_Date"].iso_format()
    data = {
        'my_projects': my_projects,
        'shared_projects': shared_projects
    }
    # Use plain Response with manual JSON
    response_body = json.dumps(data)
    resp = Response(response_body, status=200, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    print("Response headers before return:", dict(resp.headers))
    return resp

@app.teardown_appcontext
def close_db(error):
    pm.close()

if __name__ == '__main__':
    app.run(debug=True)