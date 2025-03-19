# Test_project_stuff.py
from ProjectManager import ProjectManager

def main():
    pm = ProjectManager()
    print("Loading existing projects...")
    pm.load_from_file()

    print("\nRetrieving all projects:")
    print(pm.get_all_projects())

    print("\nCreating a new project (Save):")
    pm.create_project("DemoProject", "2025-03-20", "09:00", "MR", "Demo for class")
    print("All projects after save:", pm.get_all_projects())

    print("\nRetrieving my projects (MR):")
    print(pm.get_my_projects("MR"))

    print("\nLocking and trying to delete:")
    pm.lock_project("DemoProject")
    print("Delete locked project:", pm.delete_project("DemoProject"))

    print("\nUnlocking and deleting:")
    project = pm.get_project("DemoProject")
    if project:
        project.unlock()
        pm.delete_project("DemoProject")
    print("Deleted projects:", pm.get_deleted_projects())

    print("\nRestoring project:")
    pm.restore_project("DemoProject")
    print("All projects after restore:", pm.get_all_projects())

if __name__ == "__main__":
    main()