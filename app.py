from flask import Flask, render_template, request, redirect, url_for, jsonify
from ProjectManager import ProjectManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #NEEDED FOR SVELTE

# Initialize ProjectManager with Neo4j connection
pm = ProjectManager(uri="neo4j://941e739f.databases.neo4j.io", user="neo4j", password="Team_Blue")

#API ROUTES ↓
@app.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(pm.get_all_projects())

@app.route("/my_projects/<initials>", methods=["GET"])
def get_my_projects(initials):
    return jsonify(pm.get_my_projects(initials))

@app.route("/delete/<project_name>", methods=["POST"])
def delete_project(project_name):
    success = pm.delete_project(project_name)
    if success:
        return redirect(url_for('dashboard'))
    return "Could not delete project", 400

@app.route("/lock/<project_name>", methods=["POST"])
def lock_project(project_name):
    if pm.lock_project(project_name):
        return redirect(url_for('dashboard'))
    return "Could not lock project", 400

@app.route("/unlock/<project_name>", methods=["POST"])
def unlock_project(project_name):
    if pm.unlock_project(project_name):
        return redirect(url_for('dashboard'))
    return "Could not unlock project", 400

@app.route('/')
def dashboard():
    # For now, we'll assume the user is "MR" (you can add login later)
    lead_analyst_initials = "MR"

    # Fetch projects
    my_projects = pm.get_my_projects(lead_analyst_initials)
    shared_projects = pm.get_shared_projects(lead_analyst_initials)

    return render_template('dashboard.html', my_projects=my_projects, shared_projects=shared_projects)

@app.route('/create', methods=['GET', 'POST'])
def create_project():
    if request.method == 'POST':
        project_name = request.form['project_name']
        start_date = request.form['start_date']
        time = request.form['time']
        lead_analyst_initials = request.form['lead_analyst_initials']
        description = request.form['description']
        
        pm.create_project(project_name, start_date, time, lead_analyst_initials, description)
        return redirect(url_for('dashboard'))
    
    return render_template('create_project.html')

#cleanup
@app.teardown_appcontext
def close_db(error):
    pm.close()

if __name__ == '__main__':
    app.run(debug=True)