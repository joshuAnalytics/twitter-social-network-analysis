from neo4j import GraphDatabase


class Connection:
    """
    connects to a neo4j database instance and executes cypher queries
    https://neo4j.com/docs/cypher-manual/current/
    """

    def __init__(self, uri, user, password, verbose=False):
        """
        connect to the neo4j instance
            uri: neo4j://localhost:7687
            user: neo4j username
            password: neo4j password
            verbose: prints cypher queries
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.verbose = verbose
        self.last_b = None

    def close(self):
        """close the db connection"""
        if self.driver is not None:
            self.driver.close()

    def query(self, query, db=None):
        """
        sends a cypher query to neo4j and handles exceptions
        """
        assert self.driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.driver.session(database=db) if db is not None else self.driver.session()
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()

        if self.verbose:
            print(query)
        return response

    def create_node(self, nodetype, unique_key_fieldname, unique_key):
        """
        create a node if it doesn't already exist
        args:
            nodetype: type of node in neo4j
            unique_key_fieldname: the property on the node to uniquely identify it
            unique_key: the unique key for the node instance being created
        """
        self.query(f"MERGE (a:{nodetype} {{ {unique_key_fieldname}: '{unique_key}' }})")

    def link_users(self, a, b, rtype="FOLLOWS"):
        """
        create directed relationship of <rtype> between a -> b
        """
        # create the a node
        self.create_node("User", "screen_name", a)

        # create the b node if it has changed
        if self.last_b != b:
            self.create_node("User", "screen_name", b)
        self.last_b = b

        # create the a->b relationship
        self.query(
            f"MATCH (a:User {{ screen_name: '{a}' }}),(b:User {{ screen_name: '{b}' }}) \nMERGE (a)-[r:{rtype}]->(b)"
        )
        if self.verbose:
            print(f"linked {a} -> {b}")

    def delete_all(self):
        """
        remove all the nodes in the database
        """
        self.query(f"MATCH (n) DETACH DELETE n;")
