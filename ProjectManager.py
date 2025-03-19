class ProjectManager:
    def __init__(self):
        self.projects = []  # List of active projects
        self.deleted_projects = []  # List of deleted projects

    # Creates a new projecy and adds it to the list of projects
    def create_project(self, project_name, start_date, time, lead_analyst_initials, 
                      description="", file_paths=None):
        new_project = Project(project_name, start_date, time, lead_analyst_initials, 
                             description, file_paths)
        self.projects.append(new_project)
        return new_project
    
    # Imports and existing project from a data dictionary
    def import_project(self, project_data):
        project = Project(
            project_data["project_name"],
            project_data["start_date"],
            project_data["time"],
            project_data["lead_analyst_initials"],
            project_data.get("description", ""),
            project_data.get("file_paths", [])
        )
        project.created_date = project_data.get("created_date", project.created_date)
        project.last_edit_date = project_data.get("last_edit_date", project.last_edit_date)
        project.is_locked = project_data.get("is_locked", False)
        project.status = project_data.get("status", "active")
        self.projects.append(project)
        return project
    
    # Deletes a project if it's not locked and moves it to the deletes_project list
    def delete_project(self, project_name):
        for i, project in enumerate(self.projects):
            if project.project_name == project_name and not project.is_locked:
                deleted_project = self.projects.pop(i)
                deleted_project.status = "inactive"
                deleted_project.last_edit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.deleted_projects.append(deleted_project)
                return True
        return False
    
    # Restore a deleted project from the list of deleted_projects
    def restore_project(self, project_name):
        for i, project in enumerate(self.deleted_projects):
            if project.project_name == project_name:
                restored_project = self.deleted_projects.pop(i)
                restored_project.status = "active"
                restored_project.last_edit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.projects.append(restored_project)
                return True
        return False
    
    # Permanently deletes a project from the delete_projects list
    def delete_forever(self, project_name):
        for i, project in enumerate(self.deleted_projects):
            if project.project_name == project_name:
                self.deleted_projects.pop(i)
                # Simulate permanent deletion (e.g., remove folder)
                return True
        return False
    
    # Locks a project by name
    def lock_project(self, project_name):
        project = self.get_project(project_name)
        if project:
            project.lock()
            return True
        return False
    
    # Imports Nmap results into a project's file_paths
    def import_nmap_results(self, project_name, nmap_file_path):
        project = self.get_project(project_name)
        if project:
            project.file_paths.append(nmap_file_path)
            project.last_edit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True
        return False
    
    # Exports a project as a dictionary (simulating file export)
    # TODO: How do we actually do this to JSON or somethihng like that?
    def export_project(self, project_name):
        project = self.get_project(project_name)
        if project:
            return project.get_info()
        return None
    
    # Helper method to retrieve a project by name
    def get_project(self, project_name):
        for project in self.projects:
            if project.project_name == project_name:
                return project
        return None
    
    # Returns infor for all active projects
    def get_all_projects(self):
        return [project.get_info() for project in self.projects]
    
    # Returns info for all deleted projects
    def get_deleted_projects(self):
        return [project.get_info() for project in self.deleted_projects]
    
    # Returns projects where the user is the lead analyst
    # This way they can see what projects they are the lead analyst for
    def get_my_projects(self, lead_analyst_initials):
        return [project.get_info() for project in self.projects 
                if project.lead_analyst_initials == lead_analyst_initials]
    
    # Returns project where the use is not the lead analyst
    # This is simulating the shared projects
    def get_shared_projects(self, lead_analyst_initials):
        return [project.get_info() for project in self.projects 
                if project.lead_analyst_initials != lead_analyst_initials]