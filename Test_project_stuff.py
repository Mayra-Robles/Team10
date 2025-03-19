from ProjectManager import ProjectManager

def main():
    # Initialize the ProjectManager
    pm = ProjectManager()

    # Create a new project
    pm.create_project("TestProject", "2025-03-19", "14:30", "JD", "A test project", ["file1.txt"])

    # Lock the project
    pm.lock_project("TestProject")

    # Try to delete (will fail because it’s locked)
    print("Delete locked project:", pm.delete_project("TestProject"))  # False

    # Unlock and delete (fixing the previous typo: should be unlock)
    project = pm.get_project("TestProject")
    if project:
        project.unlock()  # Corrected from lock_project to unlock
        print("Delete unlocked project:", pm.delete_project("TestProject"))  # True

    # Restore the project
    print("Restore project:", pm.restore_project("TestProject"))

    # Import Nmap results
    print("Import Nmap:", pm.import_nmap_results("TestProject", "nmap_results.xml"))

    # Export project
    project_data = pm.export_project("TestProject")
    print("Exported project:", project_data)

    # Get all projects
    print("All projects:", pm.get_all_projects())

if __name__ == "__main__":
    main()