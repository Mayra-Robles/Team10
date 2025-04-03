from neo4j import GraphDatabase

class DBEnumerator:
    def __init__(self, uri="neo4j+s://941e739f.databases.neo4j.io", user="neo4j", password="Team_Blue"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.tableNames = []
        self.columnNames = []
        self.table = {}
        self.enumerate_database()

    def enumerate_database(self):
        with self.driver.session() as session:
            result = session.run("CALL db.labels()")
            self.tableNames = [record["label"] for record in result]

            result = session.run("CALL db.propertyKeys()")
            self.columnNames = [record["propertyKey"] for record in result]

            for label in self.tableNames:
                result = session.run(f"MATCH (n:{label}) RETURN n")
                self.table[label] = [dict(record["n"]) for record in result]

    def process_responses(self, machine_data):
        pass

    def save_results(self):
        pass

    def reset(self):
        self.tableNames = []
        self.columnNames = []
        self.table = {}
        self.enumerate_database()

    def display_results(self):
        print("Node Labels (Tables):", self.tableNames)
        print("Property Keys (Columns):", self.columnNames)
        print("Node Data (Table):", self.table)

if __name__ == "__main__":
    db_enum = DBEnumerator()
    db_enum.display_results()