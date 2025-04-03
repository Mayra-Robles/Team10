# Placeholder ProjectManager using in-memory data
class ProjectManager:
    def __init__(self):
        self.projects = []

    def get_projects(self, initials):
        return [p for p in self.projects if p['initials'] == initials]

    def add_project(self, project):
        self.projects.append(project)