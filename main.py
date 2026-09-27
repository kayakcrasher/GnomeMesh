from node import Node
from network import Network


network = Network()

home = Node("Home")
hilltop = Node("Hilltop")
town = Node("Town")
south_relay = Node("SouthRelay")

for node in [
    home,
    hilltop,
    town,
    south_relay,
]:
    network.add_node(node)


home.connect(hilltop)
hilltop.connect(town)

home.connect(south_relay)
south_relay.connect(town)


print("\n=== GNOMEMESH STORE-AND-FORWARD TEST ===\n")


print("TEST 1: Normal message")
network.send_message(
    "Home",
    "Town",
    "Hello from Home!"
)


print("\nTEST 2: All routes disabled")
network.disable_node("Hilltop")
network.disable_node("SouthRelay")

network.send_message(
    "Home",
    "Town",
    "This message must wait."
)


print("\nTEST 3: Restore network")
network.enable_node("SouthRelay")

network.retry_queued_messages()


print("\n=== TEST COMPLETE ===")
