from neo4j import GraphDatabase
import json

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "foo")
    

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    
    def node_exists(label, property_name, property_value):
        with driver.session() as session:
            query = f"MATCH (n:{label} {{{property_name}: $value}}) RETURN COUNT(n) > 0 AS exists"
            result = session.run(query, value=property_value)
            return result.single()["exists"]   
    
    def relationship_exists(user_id, file_name):
        with driver.session() as session:
            query = (
                f"MATCH (n1:User {{id: $value1}})"
                f"MATCH (n2:File {{name: $value2}})"
                f"RETURN EXISTS((n1)-[:DOWNLOADED]->(n2)) AS exists"
            )
            result = session.run(query, value1=user_id, value2=file_name)
            return result.single()["exists"]
    
    
    with open('sedac_downloads_1st_week.jsonl', 'r', encoding='utf-16') as f:
        for line in f:
            download = json.loads(line)
            # Extract user
            user_id = download['user_id']
            # Does it exist?
            
            if node_exists("User", "id", user_id):     
                print('User exists')
            else:
                print ('User DOES NOT exits')
                summary = driver.execute_query("""
                    CREATE (a:User {id: $userID})
                    """,
                    userID=user_id,
                    database_="neo4j",
                ).summary
                
            # Extract file
            file_name = download['message']['download']['object']
            file_size = download['message']['download']['size']
            # Does it exist?
            if node_exists("File", "name", file_name):     
                print('File exists')
            else:
                print ('File DOES NOT exits')
                summary = driver.execute_query("""
                    CREATE (a:File {name: $fileName, size: $fileSize})
                    """,
                    fileName=file_name, fileSize=file_size,
                    database_="neo4j",
                ).summary
                
            # Does the download edge exist?
            if relationship_exists(user_id, file_name):
                print ('Relationship exits')
                    
            #   Yes - increment download times
                summary = driver.execute_query("""
                        MATCH (a:User), (b:File) 
                        WHERE a.id = $userId AND b.name = $name
                        MERGE (a)-[r:DOWNLOADED]->(b)
                        SET r.times = r.times + 1
                    """,
                    userId=user_id, name=file_name,
                    database_="neo4j",
                ).summary
            else:
                print ('Relationship DOES NOT exits')
            #   No - create edge and set download times to 1 
                summary = driver.execute_query("""
                        MATCH (a:User {id:$userId}), (b:File{name:$name})
                        CREATE (a)-[r:DOWNLOADED {times: 1}]->(b)
                    """,
                    userId=user_id, name=file_name,
                    database_="neo4j",
                ).summary      
            
