from flask import Flask, jsonify, request
from flask_cors import CORS
from ProjectManager import ProjectManager

app = Flask(__name__)
CORS(app) #enable CORS
pm = ProjectManager()
pm.load_from_file()

@app.route("/projects", methods=["GET"])
def get_projects():
    return jsonify(pm.get_all_projects())

@app.route("/my_projects/<initials>", methods=["GET"])
def get_my_projects(initials):
    return jsonify(pm.get_my_projects(initials))

@app.route("/create", methods=["POST"])
def create_project():
    data = request.json
    pm.create_project(data["name"], data["date"], data["time"], "MR", data.get("description", ""))
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)