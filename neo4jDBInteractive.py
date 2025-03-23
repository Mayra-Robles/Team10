import ipaddress
from neo4j import GraphDatabase
from json_builder import json  # Import from your custom module
import ssl

URI = "neo4j://941e739f.databases.neo4j.io"  # Working URI with SSL workaround
USER = "neo4j"
PASSWORD = "Team_Blue"

# Create an unverified SSL context
context = ssl._create_unverified_context()

class Neo4jInteractive:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, ssl_context=context)

    def start(self):
        print("Connected To Neo4j database. Choose a number to begin or 'exit' to close")
        while True:
            print("1. Create Lead Analyst")
            print("2. Show projects")
            print("3. Create Project")
            print("4. Delete Project")
            print("5. Lock Project")
            print("6. Unlock Project")
            print("7. Add lead owner to a project")
            print("8. Add placeholder files to a project")
            print("9. Add IPs to a project")
            query = input("neo4j> ")
            if query.lower() == "exit":
                print("Closing...")
                self.driver.close()
                break
            try:
                if query == '1':
                    print("Type Name and Id separated by a comma")
                    query = input("neo4j> ")
                    queryArr = query.split(",")
                    results = self.create_LeadAnalyst(queryArr[0], queryArr[1])
                    print(results)

                elif query == '2':
                    print("Type the initials of Lead Analyst for specific projects or leave blank to see all projects")
                    query = input("neo4j> ")
                    results = self.show_projects(query)
                    for record in results:
                        print(record)

                elif query == '3':
                    print("Type Id of project, Name of project and locked status separated by commas in that order")
                    query = input("neo4j>")
                    queryArr = query.split(',')
                    results = self.create_projects(queryArr[1], queryArr[0], queryArr[2])
                    print(results)

                elif query == '4':
                    print("Type Id of the project you would like to delete")
                    query = input("neo4j>")
                    results = self.delete_project(int(query))
                    print(results)

                elif query == '5':
                    print("Type Id of the project you would like to lock")
                    query = input("neo4j>")
                    results = self.lock_projects(int(query))
                    print(results)

                elif query == '6':
                    print("Type Id of the project you would like to unlock")
                    query = input("neo4j>")
                    results = self.unlock_projects(int(query))
                    print(results)

                elif query == '7':
                    print("Type Owner name and Id of project")
                    query = input("neo4j>")
                    queryArr = query.split(',')
                    result = self.add_ownership(queryArr[0], queryArr[1])
                    print(result)

                elif query == '8':
                    print("Type project name and all files you want to add to the project separated by a comma")
                    query = input("neo4j>")
                    queryArr = query.split(',')
                    result = self.add_placeholderfiles(queryArr[0], queryArr[1:])
                    print(result)

                elif query == '9':
                    print("Type Id of the project that you would like to add IPs")
                    project_id = input("neo4j>")
                    print("Enter IPs and ports in the following format: 'IP, port'")
                    print("For multiple IPs, separate them with semicolons (ex: '192.168.0.1,80;10.0.0.7,70')")
                    ip_input = input("neo4j>")
                    ip_list = [tuple(ip.split(',')) for ip in ip_input.split(';')]
                    result = self.add_ip_to_project(project_id, ip_list)
                    print(result)

            except Exception as e:
                print(f"Error: {e}")

    def show_projects(self, OwnerInitials=None):
        query = """
        MATCH (u:User)-[:OWNS]->(p:Project)
        """
        if OwnerInitials:
            query += " WHERE u.name STARTS WITH $owner_initials"
        query += " RETURN u.name AS owner, p.name AS project, p.locked AS locked_status"
        with self.driver.session() as session:
            result = session.run(query, owner_initials=OwnerInitials) if OwnerInitials else session.run(query)
            return [{"Owner": record["owner"], "Project": record["project"], "Locked Status": record["locked_status"]} for record in result]

    def create_LeadAnalyst(self, Name, ID):
        query = "CREATE (u:User {id: $Id, name: $name})"
        with self.driver.session() as session:
            session.run(query, name=str(Name), Id=int(ID))
            result = session.run("MATCH (u:User) RETURN u.id AS id, u.name AS name")
            leads = [{"Id": record["id"], "Name": record["name"]} for record in result]
            json_builder = json("success")
            json_builder.set_data(leads)
            return json_builder.build()

    def print_Lead(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u.id AS id, u.name AS name")
            users = [{"ID": record["id"], "Name": record["name"]} for record in result]
            for user in users:
                print(user)

    def create_projects(self, Project_Name, ID, lockedstatus):
        locked_bool = lockedstatus.lower() == "true"
        query = "CREATE (p:Project {id: $Id, name: $name, locked: $locked_status})"
        with self.driver.session() as session:
            session.run(query, Id=int(ID), name=Project_Name, locked_status=locked_bool)
            results = session.run("MATCH (p:Project) RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files")
            projects = [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]} for record in results]
            json_builder = json("success")
            json_builder.set_data(projects)
            return json_builder.build()

    def add_ownership(self, Owner, ID):
        query = """
        MATCH (u:User {name: $name}), (p:Project {id: $Id})
        MERGE (u)-[:OWNS]->(p)
        """
        with self.driver.session() as session:
            session.run(query, name=str(Owner), Id=int(ID))
            result = session.run("MATCH (u:User)-[r:OWNS]->(p:Project) RETURN u.name AS owner, p.name AS project")
            relationships = [{"owner": record["owner"], "project": record["project"]} for record in result]
            json_builder = json("success")
            json_builder.set_data(relationships)
            return json_builder.build()

    def delete_project(self, Project_ID):
        with self.driver.session() as session:
            query = "MATCH (p:Project {id: $id}) DETACH DELETE p"
            session.run(query, id=Project_ID)
            result = session.run("MATCH (p:Project) RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files")
            projects = [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]} for record in result]
            json_builder = json("success")
            json_builder.set_data(projects)
            return json_builder.build()

    def lock_projects(self, Project_ID):
        with self.driver.session() as session:
            lock = "MATCH (p:Project {id: $id}) SET p.locked = true RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files"
            result = session.run(lock, id=Project_ID)
            projects = [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]} for record in result]
            json_builder = json("success")
            json_builder.set_data(projects)
            return json_builder.build()

    def unlock_projects(self, Project_ID):
        with self.driver.session() as session:
            lock = "MATCH (p:Project {id: $id}) SET p.locked = false RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files"
            result = session.run(lock, id=Project_ID)
            projects = [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]} for record in result]
            json_builder = json("success")
            json_builder.set_data(projects)
            return json_builder.build()

    def add_placeholderfiles(self, project_name, files):
        with self.driver.session() as session:
            query = """
            MATCH (p:Project {name: $project})
            SET p.files = $file_list
            RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files
            """
            result = session.run(query, project=project_name, file_list=files)
            projects = [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]} for record in result]
            json_builder = json("success")
            json_builder.set_data(projects)
            return json_builder.build()

    def is_valid_ip(self, ip):
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False

    def add_ip_to_project(self, Project_ID, IP_list):
        ips = [(ip[0], ip[1]) for ip in IP_list if self.is_valid_ip(ip[0])]
        if not ips:
            json_builder = json("error")
            json_builder.set_data({"message": "No valid IPv4 addresses provided"})
            return json_builder.build()
        query = "MATCH (p:Project {id: $Id}) SET p.IP_list = $IP_list"
        with self.driver.session() as session:
            session.run(query, Id=int(Project_ID), IP_list=ips)
            json_builder = json("success")
            json_builder.set_data(ips)
            return json_builder.build()

    def get_ips(self, Project_ID):
        query = "MATCH (p:Project {id: $Id}) RETURN p.IP_list AS IP_list"
        with self.driver.session() as session:
            res = session.run(query, Id=int(Project_ID))
            rec = res.single()
            return rec["IP_list"] if rec else None

neo4j_console = Neo4jInteractive(URI, USER, PASSWORD)
neo4j_console.start()