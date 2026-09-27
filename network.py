from collections import deque


class Network:
    def __init__(self):
        self.nodes = {}
        self.disabled_nodes = set()

    def add_node(self, node):
        self.nodes[node.node_id] = node

    def disable_node(self, node_id):
        if node_id in self.nodes:
            self.disabled_nodes.add(node_id)
            print(f"[NETWORK] {node_id} is OFFLINE")

    def enable_node(self, node_id):
        self.disabled_nodes.discard(node_id)
        print(f"[NETWORK] {node_id} is ONLINE")

    def find_route(self, source_id, destination_id):
        if source_id not in self.nodes:
            return None

        if destination_id not in self.nodes:
            return None

        if source_id in self.disabled_nodes:
            return None

        if destination_id in self.disabled_nodes:
            return None

        queue = deque([(source_id, [source_id])])
        visited = {source_id}

        while queue:
            current_id, path = queue.popleft()

            if current_id == destination_id:
                return path

            for neighbor in self.nodes[current_id].neighbors:
                neighbor_id = neighbor.node_id

                if (
                    neighbor_id not in visited
                    and neighbor_id not in self.disabled_nodes
                ):
                    visited.add(neighbor_id)
                    queue.append(
                        (neighbor_id, path + [neighbor_id])
                    )

        return None

    def send_message(self, source_id, destination_id, message):
        route = self.find_route(
            source_id,
            destination_id
        )

        if route is None:
            self.nodes[source_id].queue_message(
                destination_id,
                message
            )

            print(
                f"[NETWORK] No route. "
                f"Message stored at {source_id}."
            )

            return False

        print("Route:", " -> ".join(route))

        self.nodes[destination_id].receive_message(
            source_id,
            message
        )

        return True

    def retry_queued_messages(self):
        print("\n[NETWORK] Checking queued messages...")

        for node in self.nodes.values():
            remaining = []

            for item in node.outbox:
                delivered = self.send_message(
                    node.node_id,
                    item["destination"],
                    item["message"]
                )

                if not delivered:
                    remaining.append(item)
                else:
                    print(
                        f"[NETWORK] Delivered queued message "
                        f"from {node.node_id}"
                    )

            node.outbox = remaining
