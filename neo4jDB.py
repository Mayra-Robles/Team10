from neo4j import GraphDatabase
from json_builder import json
from datetime import datetime
import ssl

URI="neo4j://941e739f.databases.neo4j.io"
User="neo4j"
Password="Team_Blue"
class Neo4jInteractive:
    def __init__(self, uri, user, password):
        context = ssl._create_unverified_context()
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=True, ssl_context=context)
    """
    def start(self):
        print("Connected To Neo4j database. Choose a number to begin or exit to close")
        while True:
            print("1. Create Lead Analyst")
            print("2. Show projects")
            print("3. Create Project")
            print("4. Delete Project")
            print("5. Lock Project")
            print("6. Unlock Project")
            print("7. Add lead owner to a project")
            print("8. Add placeholder files to a project")
            query = input("neo4j> ")  # Wait for query
            if query.lower() == "exit":
                print("Closing...")
                self.driver.close()
                break
            try:    
                if query=='1':
                    print("Type Name, Id, role and initials separated by a comma")
                    query = input("neo4j> ")
                    queryArr=query.split(",")
                    results = self.create_Analyst(queryArr[0], queryArr[1], queryArr[2], queryArr[3], queryArr[4], queryArr[5])
                    print(results)
                    
                    
                elif query=='2':
                    print("Type the initials of Lead Analyst for specifc projects or leave blanks to see al projects")
                    query = input("neo4j> ")
                    results= self.show_projects(query)
                    for record in results:
                        print(record)  # Print results
                        
                elif query=='3':
                    print("Type Id of project, Name of project and locked status separated by commas in that order")
                    query= input("neo4j>")
                    queryArr= query.split(',')
                    results= self.create_projects(queryArr[0], queryArr[1], queryArr[2], queryArr[3], queryArr[4], queryArr[5])
                    print(results)
                    
                elif query == '4':
                    print("Type Id of the project you would like to delete")
                    query = input("neo4j>")
                    results=self.delete_project(int(query))
                    print(results)
                    
                elif query == '5':
                    print("Type Id of the project you would like to lock")
                    query = input("neo4j>")
                    results=self.lock_projects(int(query))
                    print(results)
                    
                elif query == '6':
                    print("Type Id of the project you would like to unlock")
                    query = input("neo4j>")
                    results=self.unlock_projects(int(query))
                    print(results)
                    
                elif query== '7':
                    print("Type Owner name and Id of project")
                    query= input("neo4j>")
                    queryArr= query.split(',')
                    result=self.add_ownership(queryArr[0], queryArr[1])
                    print(result)
                    
                elif query=='8':
                    print("Type project name and all files you want to add to the project separated by a comma")
                    query=input("neo4j>")
                    queryArr=query.split(',')
                    result=self.add_placeholderfiles(queryArr[0], queryArr[1:len(queryArr)])
                    print(result)
                
                elif query=='9':
                    query=input("neo4j>")
                    queryArr=query.split(',')
                    result= self.join_project(queryArr[0], queryArr[1])
                    print(result)
                
                elif query=='10':
                    query=input("neo4j>")
                    queryArr=query.split(',')
                    result= self.get_my_projects(queryArr[0])
                    print(result)
                    
            except Exception as e:
                print(f"Error: {e}")
                """
            
    #Allows to create a Lead Analyst
    #@params Name: Name of the Analyst, ID: Id of the Analyst
    #@returns JSON with format of all analysts or status error JSON
    def create_Analyst(self, Name, ID, role, initials):
        #if we don't have all the parameters necessary to create an analyst we return a json with error status and erorr Message
        if not all([Name, ID, role, initials]):
            return [{"status": "error"}]
        #initial query to create user
        query="""CREATE (u: Analyst {id: $Id, name: $name, 
                role: $role, initials: $initials})"""
        with self.driver.session() as session:
            #run query with params in safe way using $
            session.run(query, name=str(Name), Id=int(ID), role=str(role), initials=str(initials).upper())
            #return as variables to format it into json
            #session.run("MATCH (u: Analyst) RETURN u.id AS id, u.name AS name, u.role AS role, u.initials AS initials, u.creationDate AS creationDate, u.description AS description, u.MachineIP AS MachineIP")            
            #build json with format, success control message added to ensure correct communication with front end
            return [{"status": "success"}]
    
   
    def delete_Analyst(self, initials):
        query = """
        MATCH (u:Analyst {initials: $initials})
        DETACH DELETE a
        RETURN COUNT(a) AS deleted_count
        """
        with self.neo4j.driver.session() as session:
            result = session.run(query, initials=initials)
            deleted_count = result.single()["deleted_count"]
        
            if deleted_count > 0:
                return [{"status": "success"}]
            else:
                return [{"status": "failure", "error": "No analyst found"}]

    
    #Retreives all  the analysts in the database  
    def print_Analyst(self):
        query = """
        MATCH (u:Analyst)
        RETURN u
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record["u"]) for record in result]
    
    #Allows to create project with name, id and locked status
    #@params: Project_Name: Name of the project, ID: unique id assigned to project, 
    #         Lockedstatus: boolean value for locked status
    #@returns: JSON format of all projects
    def create_projects(self, Project_Name, ID, lockedstatus, description, MachineIP, Lead_Initials):
        locked_bool = lockedstatus.lower() == "true"
        if not is_ip_valid(MachineIP):
            return [{"status": "error"}]
        todayDate=datetime.now()
        formatDate = todayDate.strftime("%Y-%m-%dT%H:%M:%S")
        query= """CREATE (p: Project {id: $Id, name: $name, locked:$locked_status, 
                Stamp_Date: datetime($Stamp_Date), description: $description, MachineIP: $MachineIP, files: [], Lead_Initials: $Lead_Initials})"""
        with self.driver.session() as session:
            session.run(query, Id= int(ID), name=str(Project_Name), locked_status=locked_bool, Stamp_Date=formatDate, description=str(description), MachineIP=str(MachineIP), files=[], Lead_Initials=str(Lead_Initials).upper())
            return [{"status": "success"}]
        
    def join_project(self, project_name, analystInitials):
        query = """
        MATCH (a:Analyst {role: "Analyst", initials: $initials}), (p:Project {name: $name})
        MERGE (a)-[:inProject]->(p)
        RETURN COUNT(a) AS analysts_joined
        """
        with self.driver.session() as session:
            result = session.run(query, initials=str(analystInitials).upper(), name=str(project_name))
            analysts_joined = result.single()["analysts_joined"]

            if analysts_joined > 0:
                return [{"status": "success", "analysts_joined": analysts_joined}]
            else:
                return [{"status": "failure", "error": "No analysts with role 'analyst' or project not found"}]
        
    #Allows to add a relationship of ownership betwwen the analyst and a project
    #@params: Owner: Name of the analyst, ID: unique integer value of the project
    #@returns: JSON format of all relationships
    def add_ownership(self, Owner, ID):
        query=""" MATCH (u:Analyst {name: $name}), (p: Project {id: $Id})
            MERGE (u)-[:OWNS]->(p)"""
        with self.driver.session() as session:
            session.run(query, name=str(Owner), Id=int(ID))
            result=session.run("MATCH p=()-[]->() RETURN p")
            graph_data=[]
            for record in result:
                path = record["p"]  # El camino 'p' es una lista de nodos y relaciones
                path_json = []
                #We search for nodes, neo4j has two different types, nodes or relationship (node such as User or project)
                for element in path.nodes:
                     node_json = {
                     "type": "Node",
                     "labels": list(element.labels),
                     "properties": dict(element)
                    }
                     path_json.append(node_json)
                #We search for relationships (OWNS)
                for relation in path.relationships:
                     relationship_json = {
                      "type": "Relationship",
                      "owner": dict(relation.start_node),
                      "project": dict(relation.end_node),
                      "type": relation.type,
                      "properties": dict(relation)
                    }
                     path_json.append(relationship_json)
                graph_data.append(path_json)
            response_json = json("success")
            response_json.set_data(graph_data)
            return response_json.build()
        
        
    #Allows to delete a specific project from the DB
    #@params: Project_ID: unique id of project to delete
    #@returns: JSON format of all projects updated
    def delete_project(self, Project_ID):
        with self.driver.session() as session:
            Project_ID = int(Project_ID)
            query = "MATCH (p:Project {id: $id}) DETACH DELETE p"
            session.run(query, id=Project_ID)
            session.run("MATCH (p:Project) RETURN p p.id AS id, p.name AS name, p.locked AS locked, p.files AS files")
            return [{"status": "success"}]
        
            
    #Allows to change locked property of a project to true
    #@params: Project_ID: Unique id of project to lock
    #@returns: JSON format of the locked project     
    def lock_projects(self, Project_ID):
        with self.driver.session() as session:
            lock = "MATCH (p:Project {id: $id}) SET p.locked = true RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files"
            result=session.run(lock, id = Project_ID)
            projects= [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]}for record in result]
            json_builder=json("succsess")
            json_builder.set_data(projects)
            return json_builder.build()
            
    #Allows to change the locked property of a project to false
    #@params: Project_ID: Unique id of project to lock
    #@returns: Json format of unlocked project
    def unlock_projects(self, Project_ID):
        with self.driver.session() as session:
            lock = "MATCH (p:Project {id: $id}) SET p.locked = false RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files"
            result=session.run(lock, id = Project_ID)
            projects= [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]}for record in result]
            json_builder=json("succsess")
            json_builder.set_data(projects)
            return json_builder.build()
            
    #Allows to add a list of files into the files property of a project node
    #@params: project_name: name of the project we want to add files, files: list of files to add into the project
    #@returns:JSON format of all projects
    def add_placeholderfiles(self, project_name, files):
        with self.driver.session() as session:
            query= """MATCH (p:Project {name: $project}) 
            SET p.files=$file_list
            RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files"""
            result=session.run(query, project=project_name, file_list=files)
            projects= [{"ID": record["id"], "Name": record["name"], "isLocked": record["locked"], "files": record["files"]}for record in result]
            json_builder=json("succsess")
            json_builder.set_data(projects)
            return json_builder.build()

 #added the following to match project manager file ↓
    def get_project_by_name(self, name):
        query = """
        MATCH (p:Project {name: $name})
        RETURN p.id AS id, p.name AS name, p.locked AS locked, p.files AS files
        """
        with self.driver.session() as session:
            result = session.run(query, name=name)
            return [dict(record) for record in result]
    
    def get_project(self, project_name):
        query = """
        MATCH (p:Project {name: $project_name})<-[:OWNS]-(u:Analyst)
        RETURN p, u.name AS lead_analyst_initials
        """
        with self.driver.session() as session:
            records = session.run(query, project_name=project_name)
            record = records.single()
            if record:
                p = record["p"]
                info = dict(p)
                info["lead_analyst_initials"] = record["lead_analyst_initials"]
                return info
            return None
    def get_all_projects(self):
        query = """
        MATCH (p:Project)
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record["p"]) for record in result]

    def get_my_projects(self, analyst_initials):
        query = """
        MATCH (u:Analyst {initials: $initials})-[:OWNS]->(p:Project)
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, initials=str(analyst_initials).upper())
            return [dict(record["p"]) for record in result]

    def get_shared_projects(self, analyst_initials):
        query = """
        MATCH (other:Analyst)-[:OWNS]->(p:Project)
        WHERE other.name <> $initials
        RETURN p
        """
        with self.driver.session() as session:
            result = session.run(query, initials=analyst_initials)
            return [dict(record["p"]) for record in result]

def is_ip_valid(ip):
    parts = ip.split(".")  
    if len(parts) != 4:  
        return False
    
    for part in parts:
        if not part.isdigit():  
            return False
        
        num = int(part)
        if num < 0 or num > 255: 
            return False
        
        if part != str(num):
            return False
    
    return True
"""        
neo4j_console = Neo4jInteractive(URI, User, Password)
startNeo= neo4j_console.start()
"""
