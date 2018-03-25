from neo4j.v1 import GraphDatabase

from pprint import pprint
uri = "bolt://localhost:7687/"
driver = GraphDatabase.driver(uri, auth=("neo4j2", "neo4j"))
session = driver.session()

# Find a user with name Jon Skeet
query = "MATCH (a:User {name:'Jon Skeet'}) RETURN a"
# Get all posts that have a tag by user named Jon Skeet
query1 = "MATCH (a:User {name:'Jon Skeet'})-[:POSTED]->(p:Post)-[:HAS_TAG]->(t:Tag) RETURN a,p"
# Run the query above and change the url of the user 
query2 = "MATCH (a:User {name: 'Jon Skeet'})-[:POSTED]->(p:Post)-[:HAS_TAG]->(t:Tag) SET a.url = 'http://csharpindepth.com' RETURN a,p"
# Search for users named Jon Skeet and order their posts by date created from most resent to oldest
query3 = "MATCH (a:User {name:'Jon Skeet'})-[:POSTED]->(p:Post) RETURN p ORDER BY p.createdAt DESC"
# Runs the query above and also changes the user's url
query4 = "MATCH (a:User {name:'Jon Skeet'})-[:POSTED]->(p:Post) SET a.url = 'http://csharpindepth2.com' RETURN p ORDER BY p.createdAT DESC"
# Search for all of the users named Jeff Atwood's posts after 2009
query5 = "MATCH (a:User {name:'Jeff Atwood'})-[:POSTED]->(p:Post) WHERE p.createdAt > '2009' RETURN p"
# Runs the query above and also changes the name of one of the films
query6 = "MATCH (a:User {name:'Jeff Atwood'})-[:POSTED]->(p:Post) WHERE p.createdAt > '2009' SET a.url='https://codinghorrors.com'"
# Search for user Jeff Atwood and return all the posts created between 2009 and 2014
query7 = "MATCH (a:User {name:'Jeff Atwood'})-[:POSTED]->(p:Post) WHERE p.createdAt > '2009' AND p.createdAt < '2014' RETURN p"
# Runs the query above and also changes the name of one of its films
query8 = "MATCH (a:User {name:'Jeff Atwood'})-[:POSTED]->(p:Post) WHERE p.createdAt > '2009' AND p.createdAt < '2014' SET a.url = 'https://codinghorros2.com' RETURN p"
# aggregation test for everyone and their posts
#query9 = "MATCH (a:User)-[:POSTED]->(p:Post) RETURN count(a)"
# find the shortest path in which the posts of Jon Skeet and Jeff Atwood are connected
query10 = "MATCH path = allShortestPaths ((u:User {name: 'Jon Skeet'})-[*]-(a:User {name: 'Jeff Atwood'})) RETURN path"
# creates a brand new user and post
query11 = "CREATE (a:User {name:'Faker McFakeFace'}) CREATE (p:Post {body:'Faker McFakeFace post', createdAt:'2018'}) CREATE (a)-[:POSTED]->(p)"
# delete a newly created user and the relationship 
query12 = "MATCH (a:User {name:'Faker MCFakeFace'})-[:POSTED]->(p:Post) DETACH DELETE (a), (p)" 

QUERIES = [query, query1, query2, query3, query4, query5, query6, query7, query8, query10, query11, query12]

for q in QUERIES:
	print("executing query: {}".format(q))
	results = [[], []]

	num_results = 0
	for i in range(10):
		result = session.run(q)
		num_results = result.detach()
		results[0].append(result.consume().result_available_after)
		results[1].append(result.consume().result_consumed_after)

	print("_______________________________________________________")
	print("QUERY: {}\n".format(q))
	print("RESULTS RETURNED: {}\n".format(num_results))
	print("AVERAGE RESULT AVAILABILITY FOR QUERY IS: {}\n".format(sum(results[0])/10))
	print("AVERAGE RESULT CONSUMPTION FOR QUERY IS: {}\n".format(sum(results[1])/10))

