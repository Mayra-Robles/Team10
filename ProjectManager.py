from Project import Project
from neo4j import GraphDatabase
import datetime
import ssl

class ProjectManager:
    def __init__(self, uri="neo4j://941e739f.databases.neo4j.io", user="neo4j", password="Team_Blue"):
        context = ssl._create_unverified_context()
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, ssl_context=context)

    def close(self):
        self.driver.close()

    def _run_query(self, query, **params):
        with self.driver.session() as session:
            result = session.run(query, **params)
            return list(result)  # Consume the result into a list within the session

    def create_project(self, project_name, start_date, time, lead_analyst_initials, 
                      description="", file_paths=None):
        project = Project(project_name, start_date, time, lead_analyst_initials, 
                         description, file_paths)
        query = """
        MERGE (p:Project {project_name: $project_name})
        SET p.start_date = $start_date,
            p.time = $time,
            p.description = $description,
            p.file_paths = $file_paths,
            p.is_locked = $is_locked,
            p.status = $status,
            p.created_date = $created_date,
            p.last_edit_date = $last_edit_date,
            p.folder_path = $folder_path
        MERGE (a:Analyst {initials: $lead_analyst_initials})
        MERGE (p)-[:LEAD_ANALYST]->(a)
        RETURN p
        """
        self._run_query(query, **project.get_info())
        return project

    def import_project(self, project_data):
        project = Project(
            project_data["project_name"],
            project_data["start_date"],
            project_data["time"],
            project_data["lead_analyst_initials"],
            project_data.get("description", ""),
            project_data.get("file_paths", []),
            project_data.get("is_locked", False),
            project_data.get("status", "active"),
            project_data.get("created_date"),
            project_data.get("last_edit_date"),
            project_data.get("folder_path")
        )
        self.create_project(
            project.project_name, project.start_date, project.time, 
            project.lead_analyst_initials, project.description, project.file_paths
        )
        return project

    def delete_project(self, project_name):
        query = """
        MATCH (p:Project {project_name: $project_name})
        WHERE p.is_locked = false
        SET p.status = 'inactive'
        SET p.last_edit_date = $last_edit_date
        SET p:DELETED
        RETURN p
        """
        records = self._run_query(query, project_name=project_name, 
                                 last_edit_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return bool(records[0] if records else None)

    def restore_project(self, project_name):
        query = """
        MATCH (p:Project:DELETED {project_name: $project_name})
        REMOVE p:DELETED
        SET p.status = 'active'
        SET p.last_edit_date = $last_edit_date
        RETURN p
        """
        records = self._run_query(query, project_name=project_name, 
                                 last_edit_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return bool(records[0] if records else None)

    def delete_forever(self, project_name):
        query = """
        MATCH (p:Project:DELETED {project_name: $project_name})
        DETACH DELETE p
        """
        records = self._run_query(query, project_name=project_name)
        return bool(records.consume().counters.nodes_deleted if records else False)

    def lock_project(self, project_name):
        query = """
        MATCH (p:Project {project_name: $project_name})
        SET p.is_locked = true
        RETURN p
        """
        records = self._run_query(query, project_name=project_name)
        return bool(records[0] if records else None)

    def unlock_project(self, project_name):
        query = """
        MATCH (p:Project {project_name: $project_name})
        SET p.is_locked = false
        RETURN p
        """
        records = self._run_query(query, project_name=project_name)
        return bool(records[0] if records else None)

    def import_nmap_results(self, project_name, nmap_file_path):
        query = """
        MATCH (p:Project {project_name: $project_name})
        SET p.file_paths = coalesce(p.file_paths, []) + $nmap_file_path
        SET p.last_edit_date = $last_edit_date
        RETURN p
        """
        records = self._run_query(query, project_name=project_name, nmap_file_path=nmap_file_path,
                                 last_edit_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return bool(records[0] if records else None)

    def export_project(self, project_name, filename=None):
        project_info = self.get_project(project_name)
        if project_info and filename:
            import json
            with open(filename, "w") as f:
                json.dump(project_info, f, indent=4)
            print(f"Exported {project_name} to {filename}")
        return project_info

    def get_project(self, project_name):
        query = """
        MATCH (p:Project {project_name: $project_name})-[:LEAD_ANALYST]->(a:Analyst)
        RETURN p, a.initials AS lead_analyst_initials
        """
        records = self._run_query(query, project_name=project_name)
        if records and records[0]:
            p = records[0]["p"]
            info = {key: p[key] for key in p.keys()}
            info["lead_analyst_initials"] = records[0]["lead_analyst_initials"]
            return info
        return None

    def get_all_projects(self):
        query = """
        MATCH (p:Project) WHERE NOT p:DELETED
        RETURN p
        """
        records = self._run_query(query)
        return [{key: r["p"][key] for key in r["p"].keys()} for r in records]

    def get_deleted_projects(self):
        query = """
        MATCH (p:Project:DELETED)
        RETURN p
        """
        records = self._run_query(query)
        return [{key: r["p"][key] for key in r["p"].keys()} for r in records]

    def get_my_projects(self, lead_analyst_initials):
        query = """
        MATCH (p:Project)-[:LEAD_ANALYST]->(a:Analyst {initials: $initials})
        WHERE NOT p:DELETED
        RETURN p
        """
        records = self._run_query(query, initials=lead_analyst_initials)
        return [{key: r["p"][key] for key in r["p"].keys()} for r in records]

    def get_shared_projects(self, lead_analyst_initials):
        query = """
        MATCH (p:Project)-[:LEAD_ANALYST]->(a:Analyst)
        WHERE a.initials <> $initials AND NOT p:DELETED
        RETURN p
        """
        records = self._run_query(query, initials=lead_analyst_initials)
        return [{key: r["p"][key] for key in r["p"].keys()} for r in records]