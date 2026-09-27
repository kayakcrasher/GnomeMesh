
class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.inbox = []

    def connect(self, other_node):
        if other_node not in self.neighbors:
            self.neighbors.append(other_node)

        if self not in other_node.neighbors:
            other_node.neighbors.append(self)

    def receive_message(self, sender, message):
        self.inbox.append({
            "from": sender,
            "message": message
        })

        print(f"[{self.node_id}] Message from {sender}: {message}")
