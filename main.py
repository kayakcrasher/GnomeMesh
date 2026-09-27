from node import Node
from network import Network


network = Network()

home = Node("Home")
hilltop = Node("Hilltop")
town = Node("Town")
south_relay = Node("SouthRelay")
community = Node("CommunityCenter")

for node in [
    home,
    hilltop,
    town,
    south_relay,
    community,
]:
    network.add_node(node)


home.connect(hilltop)
hilltop.connect(town)

home.connect(south_relay)
south_relay.connect(town)

town.connect(community)


print("\n=== GNOMEMESH NODE DISCOVERY TEST ===")

network.network_status()


print("TEST 1: Take Hilltop offline")

network.disable_node("Hilltop")

network.network_status()


print("TEST 2: Route around Hilltop")

network.send_message(
    "Home",
    "CommunityCenter",
    "GNOMEMESH is alive!"
)


print("TEST 3: Restore Hilltop")

network.enable_node("Hilltop")

network.network_status()


print("=== TEST COMPLETE ===")
