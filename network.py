
from collections import deque


class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def send_message(self, source_id, destination_id, message):
        if source_id not in self.nodes:
            print(f"Unknown source: {source_id}")
            return False

        if destination_id not in self.nodes:
            print(f"Unknown destination: {destination_id}")
            return False

        queue = deque([(source_id, [source_id])])
        visited = {source_id}

        while queue:
            current_id, path = queue.popleft()

            if current_id == destination_id:
                print("Route:", " -> ".join(path))

                self.nodes[destination_id].receive_message(
                    source_id, message
                )
                return True

            current_node = self.nodes[current_id]

            for neighbor in current_node.neighbors:
                neighbor_id = neighbor.node_id

                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append(
                        (neighbor_id, path + [neighbor_id])
                    )

        print("No route available.")
        return False
