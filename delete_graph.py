from neo4j import GraphDatabase
import json
from auth_neo4j import AUTH

# URI examples: "neo4j://localhost", "neo4j+s://xxx.databases.neo4j.io"
URI = "neo4j://127.0.0.1:7687"

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    
    summary = driver.execute_query("""
        MATCH (n)
	    DETACH DELETE n
        """,
        database_="neo4j",
        ).summary