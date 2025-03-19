from datetime import datetime
import os

class Project:
    def __init__(self, project_name, start_date, time, lead_analyst_initials, 
                 description="", file_paths=None, is_locked=False, status="active"):
        self.project_name = project_name
        self.start_date = start_date  # Expected format: "YYYY-MM-DD"
        self.time = time  # Expected format: "HH:MM"
        self.lead_analyst_initials = lead_analyst_initials
        self.description = description
        self.file_paths = file_paths if file_paths else []  # List of file paths
        self.is_locked = is_locked  # Prevents deletion if True
        self.status = status  # "active" (green), "errors" (red), "inactive" (gray)
        self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_edit_date = self.created_date
        self.folder_path = f"projects/{project_name}"  # Simulated folder path

        # Create project folder (simulated for now)
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path, exist_ok=True)

    # Returns a dictionary of project information.
    def get_info(self):
        return {
            "project_name": self.project_name,
            "start_date": self.start_date,
            "time": self.time,
            "lead_analyst_initials": self.lead_analyst_initials,
            "description": self.description,
            "file_paths": self.file_paths,
            "is_locked": self.is_locked,
            "status": self.status,
            "created_date": self.created_date,
            "last_edit_date": self.last_edit_date,
            "folder_path": self.folder_path
        }
    
    # Lock the porject to prevent its deletion
    def lock(self):
        self.is_locked = True

    # Unlocks the project
    def unlock(self):
        self.is_locked = False

    # Updates the project status,  it can be active, errors, or incative
    def update_status(self, new_status):
        if new_status in ["active", "errors", "inactive"]:
            self.status = new_status
            self.last_edit_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")