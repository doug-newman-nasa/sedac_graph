# SEDAC downloads knowledge graph
This repository contains two python scripts
## Graph.py
Will convert a JSONL file into a graph describing users and the files they downloaded. Each line of the file describes a download.
## delete_graph.py
Will delete the contents of a graph

## Installation
1. Install [Python 3](https://www.python.org/downloads/)
2. Install neo4j python library
```pip3 install neo4j```
3. Install [Neo4J desktop](https://neo4j.com/download/neo4j-desktop/)
4. Run Neo4J desktop and create db instance
5. Create auth_neo4j.py file
```AUTH = ('neo4j', '<your db password here>')```
6. Run graph.py
```python3 graph.py```
7. [optional] run delete_graph.py 
```python3 delete_graph.py```