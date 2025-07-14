from neo4j import GraphDatabase
import json
from auth_neo4j import AUTH

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://127.0.0.1:7687"

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    
    with open('sedac_downloads_1st_week.jsonl', 'r', encoding='utf-16') as f:
        for line in f:
            download = json.loads(line)
            # Extract user
            user_id = download['user_id']
            
            summary = driver.execute_query("""
                MERGE (a:User {id: $userID})
                """,
                userID=user_id,
                database_="neo4j",
            ).summary
                
            # Extract file
            file_name = download['message']['download']['object']
            file_size = download['message']['download']['size']
            
            summary = driver.execute_query("""
                MERGE (a:File {name: $fileName, size: $fileSize})
                """,
                fileName=file_name, fileSize=file_size,
                database_="neo4j",
            ).summary
                
            
            summary = driver.execute_query("""
                MATCH (a:User {id:$userId}), (b:File{name:$name})
                MERGE (a)-[r:DOWNLOADED]->(b)
                ON CREATE SET r.times = 1
                ON MATCH SET r.times = r.times + 1
                """,
                userId=user_id, name=file_name,
                database_="neo4j",
            ).summary
            
            
