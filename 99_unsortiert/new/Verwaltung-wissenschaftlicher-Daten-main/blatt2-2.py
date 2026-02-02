import os
from dataclasses import dataclass, field


@dataclass
class Person:
    id: str
    attributeList: list = field(default_factory=list)

@dataclass
class Friend:
    id: str

@dataclass
class FriendEdge:
    fromNode: str
    toNode: list

@dataclass
class CircleEdge:
    circleId: str
    fromNode: str
    member: list

class Loader:
    def __init__(self, path):
        self.path = path

    def load(self):
        persons = []
        friendEdges = {}
        circleEdges = {}
        attributes = {}
        egoUsers = []

        # Load features (attributes)
        for file in os.listdir(self.path):
            if file.endswith(".feat"):
                lines = open(self.path + "/" + file).readlines()
                for line in lines:
                    id = line.split()[0]
                    # Format: id feature1 feature2 ...
                    # But actually we want to store features by index?
                    # The code below seems to assume attributes is a dict of (egoId, attributeIndex) -> nameAndFeature
                    pass # Original code had logic here but it was incomplete in snippet

        # Load edges
        for file in os.listdir(self.path):
            if file.endswith(".edges"):
                lines = open(self.path + "/" + file).readlines()
                for line in lines:
                    nodeA = line.split()[0]
                    nodeB = line.split()[1]
                    if friendEdges.get(nodeA) is not None and Person(nodeB) not in friendEdges[nodeA].toNode:
                        friendEdges[nodeA].toNode.append(Person(nodeB))
                    elif friendEdges.get(nodeA) is None:
                        friendEdges[nodeA] = FriendEdge(nodeA, [Person(nodeB)])

        # Load .feat again for specific logic? (from original code)
        for file in os.listdir(self.path):
            if file.endswith(".feat"):
                lines = open(self.path + "/" + file).readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    nodeB = line.split()[0]
                    if friendEdges.get(egoId) is not None and Person(nodeB) not in friendEdges[egoId].toNode:
                        friendEdges[egoId].toNode.append(Person(nodeB))
                    elif friendEdges.get(egoId) is None:
                        friendEdges[egoId] = FriendEdge(egoId, [Person(nodeB)])

        # Load circles
        for file in os.listdir(self.path):
            if file.endswith(".circles"):
                lines = open(self.path + "/" + file).readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    circleId = line.split()[0]
                    for nodeB in line.split()[1:]:         
                        if circleEdges.get((circleId, egoId)) is not None and nodeB not in circleEdges[(circleId, egoId)].member:
                            circleEdges[(circleId, egoId)].member.append(Friend(nodeB))
                        elif circleEdges.get((circleId, egoId)) is None:
                            circleEdges[(circleId, egoId)] = CircleEdge(circleId, egoId, [Friend(nodeB)])

        # Delete egos from friends (cleanup)
        for ego in egoUsers:
            if friends.get(ego) is not None:
                del friends[ego]

        # Load featnames (attribute names)
        for file in os.listdir(self.path):
            if file.endswith(".featnames"):
                lines = open(self.path + "/" + file).readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    # Logic to parse feature names
                    pass

        # Load egofeat (features of the ego user)
        for file in os.listdir(self.path):
            if file.endswith(".egofeat"):
                lines = open(self.path + "/" + file).readlines()
                egoId = os.path.splitext(file)[0]
                for line in lines:
                    # Logic to parse ego features
                    pass

        return persons, friendEdges, circleEdges
