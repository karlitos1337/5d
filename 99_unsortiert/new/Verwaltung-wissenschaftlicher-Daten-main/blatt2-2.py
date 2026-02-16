from dataclasses import dataclass, field
import os
from neo4j import GraphDatabase

#########################Aufgabe 2) a)####################################


@dataclass
class Person:
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Person):
            return self.id == value.id

    id: str
    attributeList: list = field(default_factory=list)


@dataclass
class EgoUser(Person):
    def __eq__(self, value: object) -> bool:
        if isinstance(value, EgoUser):
            return self.id == value.id


@dataclass
class Friend(Person):
    def __eq__(self, value: object) -> bool:
        if isinstance(value, Friend):
            return self.id == value.id


@dataclass
class FriendEdge:
    fromNode: str
    toNode: list[Friend]


@dataclass
class CircleEdge:
    id: str
    owner: EgoUser
    member: list[Friend]


egoUsers = {}
friends = {}
friendEdges = {}
circleEdges = {}


class Parser:
    def __init__(self, path):
        self.path = path

    def parse(self):
        raise NotImplementedError()


class EgoUserParser(Parser):
    # Parses all ego users by the file names and stores them in egoUsers
    def parse(self):
        for file in os.listdir(self.path):
            id = os.path.splitext(file)[0]
            egoUsers[id] = EgoUser(id)


class FriendParser(Parser):
    # Parses all friends by iterating through the feat files and stores them in friends
    def parse(self):
        for file in os.listdir(self.path):
            if file.endswith(".feat"):
                lines = open(self.path + "/" + file, "r").readlines()
                for line in lines:
                    id = line.split()[0]
                    friends[id] = Friend(id)


class FriendEdgeParser(Parser):
    # Parses all edges of type IS_FRIEND by iterating through edges and feat files and stores them in friendEdges
    def parse(self):
        for file in os.listdir(self.path):
            if file.endswith(".edges"):
                lines = open(self.path + "/" + file, "r").readlines()
                for line in lines:
                    nodeA = line.split()[0]
                    nodeB = line.split()[1]
                    if (
                        friendEdges.get(nodeA) != None
                        and Person(nodeB) not in friendEdges[nodeA].toNode
                    ):
                        friendEdges[nodeA].toNode.append(Person(nodeB))
                    elif friendEdges.get(nodeA) == None:
                        friendEdges[nodeA] = FriendEdge(nodeA, [Person(nodeB)])

            elif file.endswith(".feat"):
                lines = open(self.path + "/" + file, "r").readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    nodeB = line.split()[0]
                    if (
                        friendEdges.get(egoId) != None
                        and Person(nodeB) not in friendEdges[egoId].toNode
                    ):
                        friendEdges[egoId].toNode.append(Person(nodeB))
                    elif friendEdges.get(egoId) == None:
                        friendEdges[egoId] = FriendEdge(egoId, [Person(nodeB)])


class CircleEdgeParser(Parser):
    # Parses all edges of type IN_CIRCLE by iterating through the circles file and stores them in circleEdges
    def parse(self):
        for file in os.listdir(self.path):
            if file.endswith(".circles"):
                lines = open(self.path + "/" + file, "r").readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    circleId = line.split()[0]
                    for nodeB in line.split()[1:]:
                        if (
                            circleEdges.get((circleId, egoId)) != None
                            and nodeB not in circleEdges[(circleId, egoId)].member
                        ):
                            circleEdges[(circleId, egoId)].member.append(Friend(nodeB))
                        elif circleEdges.get((circleId, egoId)) == None:
                            circleEdges[(circleId, egoId)] = CircleEdge(
                                circleId, egoId, [Friend(nodeB)]
                            )


path = "C:/Users/danie/Downloads/facebook.tar/facebook"

egoUserParser = EgoUserParser(path)
egoUserParser.parse()

friendParser = FriendParser(path)
friendParser.parse()

friendEdgeParser = FriendEdgeParser(path)
friendEdgeParser.parse()

circleEdgeParser = CircleEdgeParser(path)
circleEdgeParser.parse()

# Delete egos from friends
for ego in egoUsers:
    if friends.get(ego) != None:
        del friends[ego]


#########################Aufgabe 2) b)####################################

attributes = {}
attributeNames = set()


class AttributeParser(Parser):
    def parse(self):
        # Read all attributes and write in dict of type (egoId, attribute index) -> (attribute name, feature)
        for file in os.listdir(self.path):
            if file.endswith(".featnames"):
                lines = open(self.path + "/" + file, "r").readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    index = line.split()[0]
                    attributeName = ";".join(
                        line.split()[1].split(sep=";")[:-1]
                    ).replace(";", "_")
                    attributeNames.add(attributeName)
                    anonFeature = "anonymized feature " + line.split()[-1]
                    attributes[(egoId, index)] = (attributeName, anonFeature)

        # Read and assign attributes to friends
        for file in os.listdir(self.path):
            if file.endswith(".feat"):
                lines = open(self.path + "/" + file, "r").readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    friendId = line.split()[0]
                    attributeIndex = 0
                    for attribute in line.split()[1:]:
                        if attribute == "0":
                            attributeIndex += 1
                            continue
                        if attribute == "1" and friends.get(friendId) != None:
                            nameAndFeature = attributes[(egoId, str(attributeIndex))]
                            friends[friendId].attributeList.append(nameAndFeature)
                            attributeIndex += 1

        # Read and assign attributes to ego user
        for file in os.listdir(self.path):
            if file.endswith(".egofeat"):
                lines = open(self.path + "/" + file, "r").readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    attributeIndex = 0
                    for attribute in line.split():
                        if attribute == "0":
                            attributeIndex += 1
                            continue
                        if attribute == "1":
                            nameAndFeature = attributes[(egoId, str(attributeIndex))]
                            egoUsers[egoId].attributeList.append(nameAndFeature)
                            attributeIndex += 1


attributeParser = AttributeParser(path)
attributeParser.parse()


#########################Aufgabe 2) c)####################################


class EgoUserDAO:
    def __init__(self, driver):
        self.driver = driver

    def create(self, dto: EgoUser):
        records, summary, keys = driver.execute_query(
            "CREATE (p:Person:Ego {id: $id})",
            id=dto.id,
            database_="neo4j",
        )
        for attName, attValue in dto.attributeList:
            queryStr = (
                "MATCH (p:Person:Ego {id: $id}) SET p."
                + attName
                + ' = "'
                + attValue
                + '"'
            )
            records, summary, keys = driver.execute_query(
                queryStr,
                id=dto.id,
                database_="neo4j",
            )


class FriendDAO:
    def __init__(self, driver):
        self.driver = driver

    def create(self, dto: Friend):
        records, summary, keys = driver.execute_query(
            "CREATE (p:Person:Friend {id: $id})",
            id=dto.id,
            database_="neo4j",
        )
        for attName, attValue in dto.attributeList:
            queryStr = (
                "MATCH (p:Person:Friend {id: $id}) SET p."
                + attName
                + ' = "'
                + attValue
                + '"'
            )
            records, summary, keys = driver.execute_query(
                queryStr,
                id=dto.id,
                database_="neo4j",
            )


class CircleEdgeDAO:
    def __init__(self, driver):
        self.driver = driver

    def create(self, dto: CircleEdge):
        for toNode in dto.member:
            records, summary, keys = driver.execute_query(
                "MATCH (fromP:Person {id: $fromID}), (toP:Person {id: $toID}) CREATE (fromP)-[r:IN_CIRCLE {id: $circleID, owner: $circleOwner}]->(toP) RETURN r, fromP, toP",
                fromID=dto.owner,
                toID=toNode.id,
                circleID=dto.id,
                circleOwner=dto.owner,
                database_="neo4j",
            )


class FriendEdgeDAO:
    def __init__(self, driver):
        self.driver = driver

    def create(self, dto: FriendEdge):
        for toNode in dto.toNode:
            records, summary, keys = driver.execute_query(
                "MATCH (fromP:Person {id: $fromID}), (toP:Person {id: $toID}) CREATE (fromP)-[r:IS_FRIEND]->(toP) RETURN r, fromP, toP",
                fromID=dto.fromNode,
                toID=toNode.id,
                database_="neo4j",
            )


URI = "bolt://localhost:7687"
AUTH = ("neo4j", "12345678")

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

    friendDAO = FriendDAO(driver)
    for friendKey in friends:
        friendDAO.create(friends[friendKey])

    egoDAO = EgoUserDAO(driver)
    for egoKey in egoUsers:
        egoDAO.create(egoUsers[egoKey])

    friendEdgeDAO = FriendEdgeDAO(driver)
    for friendEdgeKey in friendEdges:
        friendEdgeDAO.create(friendEdges[friendEdgeKey])

    circleEdgeDAO = CircleEdgeDAO(driver)
    for circleEdgeKey in circleEdges:
        circleEdgeDAO.create(circleEdges[circleEdgeKey])
