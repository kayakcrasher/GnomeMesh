import time


class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = []
        self.inbox = []
        self.outbox = []
        self.online = True
        self.last_seen = time.time()

    def connect(self, other_node):
        if other_node not in self.neighbors:
            self.neighbors.append(other_node)

        if self not in other_node.neighbors:
            other_node.neighbors.append(self)

    def set_online(self):
        self.online = True
        self.last_seen = time.time()

    def set_offline(self):
        self.online = False

    def heartbeat(self):
        if self.online:
            self.last_seen = time.time()

    def status(self):
        state = "ONLINE" if self.online else "OFFLINE"
        return {
            "node": self.node_id,
            "status": state,
            "neighbors": [
                neighbor.node_id
                for neighbor in self.neighbors
            ],
            "last_seen": self.last_seen
        }

    def receive_message(self, sender, message):
        self.inbox.append({
            "from": sender,
            "message": message
        })

        self.heartbeat()

        print(
            f"[{self.node_id}] Message from "
            f"{sender}: {message}"
        )

    def queue_message(self, destination, message):
        self.outbox.append({
            "destination": destination,
            "message": message
        })

        print(
            f"[{self.node_id}] Message queued for "
            f"{destination}"
        )
