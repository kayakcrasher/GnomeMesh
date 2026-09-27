from node import Node
from network import Network


network = Network()

home = Node("Home")
hilltop = Node("Hilltop")
town = Node("Town")
south_relay = Node("SouthRelay")
gateway = Node("InternetGateway")

for node in [
    home,
    hilltop,
    town,
    south_relay,
    gateway,
]:
    network.add_node(node)


# Primary route
home.connect(hilltop)
hilltop.connect(town)

# Backup route
home.connect(south_relay)
south_relay.connect(town)

# Internet gateway
town.connect(gateway)


print("\n=== GNOMEMESH RESILIENCE TEST ===\n")


print("TEST 1: Normal connection")
network.send_message(
    "Home",
    "Town",
    "Hello, Town!"
)


print("\nTEST 2: Hilltop failure")
network.disable_node("Hilltop")

network.send_message(
    "Home",
    "Town",
    "Still connected!"
)


print("\nTEST 3: Both relays offline")
network.disable_node("SouthRelay")

network.send_message(
    "Home",
    "Town",
    "This should fail."
)


print("\nTEST 4: SouthRelay restored")
network.enable_node("SouthRelay")

network.send_message(
    "Home",
    "Town",
    "Connection restored!"
)


print("\n=== TEST COMPLETE ===")
