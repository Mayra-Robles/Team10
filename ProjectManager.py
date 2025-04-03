from Project import Project
from neo4j import GraphDatabase
import datetime
import ssl
from neo4j_driver import Neo4jInteractive

class ProjectManager:
    def __init__(self, uri="neo4j+s://941e739f.databases.neo4j.io", user="neo4j", password="Team_Blue"):
        context = ssl._create_unverified_context()
        #self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, ssl_context=context)
        self.neo4j = Neo4jInteractive(uri, user, password)

    def close(self):
        if hasattr(self.neo4j, 'driver'):
            self.neo4j.driver.close()

    #def _run_query(self, query, **params):
    #    with self.driver.session() as session:
    #        result = session.run(query, **params)
    #        return list(result)  # Consume the result into a list within the session

    def create_project(self, project_name, start_date, time, lead_analyst_initials,
                    description="", file_paths=None):
        project_id = hash(project_name) % (10**6)  # Simple ID hash
        locked = "false"

        # Step 1: Create the Project node
        self.neo4j.create_projects(project_name, str(project_id), locked)

        # Step 2: Create the OWNS relationship
        self.neo4j.add_ownership(lead_analyst_initials, str(project_id))

        return {
            "project_name": project_name,
            "id": project_id,
            "lead_analyst_initials": lead_analyst_initials
        }

    #no longer using the Project class anymore (at least not atm)
    #def import_project(self, project_data):
    #    project = Project(
    #        project_data["project_name"],
    #        project_data["start_date"],
    #        project_data["time"],
    #        project_data["lead_analyst_initials"],
    #        project_data.get("description", ""),
    #        project_data.get("file_paths", []),
    #        project_data.get("is_locked", False),
    #        project_data.get("status", "active"),
    #        project_data.get("created_date"),
    #        project_data.get("last_edit_date"),
    #        project_data.get("folder_path")
    #    )
    #    self.create_project(
    #        project.project_name, project.start_date, project.time, 
    #        project.lead_analyst_initials, project.description, project.file_paths
    #    )
    #    return project

    def delete_project(self, project_id):
        result = self.neo4j.delete_project(project_id)
        return result.get("status") == "success" if isinstance(result, dict) else True

    #not needed (unlest we implement soft delete again)
    #def restore_project(self, project_name):
    #    query = """
    #    MATCH (p:Project:DELETED {project_name: $project_name})
    #    REMOVE p:DELETED
    #    SET p.status = 'active'
    #    SET p.last_edit_date = $last_edit_date
    #    RETURN p
    #    """
    #    records = self._run_query(query, project_name=project_name, 
    #                             last_edit_date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #    return bool(records[0] if records else None)

    #def delete_forever(self, project_name):
    #    query = """
    #    MATCH (p:Project:DELETED {project_name: $project_name})
    #    DETACH DELETE p
    #    """
    #    records = self._run_query(query, project_name=project_name)
    #    return bool(records.consume().counters.nodes_deleted if records else False)

    def lock_project(self, project_id):
        result = self.neo4j.lock_projects(project_id)
        return result.get("status") == "success" if isinstance(result, dict) else True

    def unlock_project(self, project_id):
        result = self.neo4j.unlock_projects(project_id)
        return result.get("status") == "success" if isinstance(result, dict) else True
    
    def import_nmap_results(self, project_name, nmap_file_path):
        result = self.neo4j.add_placeholderfiles(project_name, [nmap_file_path])
        return result.get("status") == "success" if isinstance(result, dict) else True

    def export_project(self, project_name, filename=None):
        project_info = self.neo4j.get_project(project_name)

        if project_info and filename:
            import json
            with open(filename, "w") as f:
                json.dump(project_info, f, indent=4)
            print(f"Exported {project_name} to {filename}")
        
        return project_info

    def get_project(self, project_name):
        return self.neo4j.get_project(project_name)

    def get_all_projects(self):
        return self.neo4j.get_all_projects()

    #doesnt work anymore
    #def get_deleted_projects(self):
    #    query = """
    #    MATCH (p:Project:DELETED)
    #    RETURN p
    #    """
    #    records = self._run_query(query)
    #    return [{key: r["p"][key] for key in r["p"].keys()} for r in records]

    def get_my_projects(self, lead_analyst_initials):
        return self.neo4j.get_my_projects(lead_analyst_initials)

    def get_shared_projects(self, lead_analyst_initials):
        return self.neo4j.get_shared_projects(lead_analyst_initials)
