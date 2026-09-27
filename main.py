
from node import Node
from network import Network


network = Network()

home = Node("Home")
hilltop = Node("Hilltop")
town = Node("Town")
gateway = Node("InternetGateway")

for node in [home, hilltop, town, gateway]:
    network.add_node(node)

home.connect(hilltop)
hilltop.connect(town)
town.connect(gateway)

print("GNOMEMESH NETWORK ONLINE")
print("------------------------")

network.send_message(
    "Home",
    "Town",
    "Hello from the offline mesh!"
)

network.send_message(
    "Home",
    "InternetGateway",
    "Requesting internet access."
)
