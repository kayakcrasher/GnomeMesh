import time
import RNS

APP_NAME = "gnomemesh"


print()
print("================================")
print("   GNOMEMESH + RETICULUM TEST")
print("================================")
print()

reticulum = RNS.Reticulum()

identity = RNS.Identity()

destination = RNS.Destination(
    identity,
    RNS.Destination.IN,
    RNS.Destination.SINGLE,
    APP_NAME,
    "node"
)

destination.set_proof_strategy(
    RNS.Destination.PROVE_ALL
)

print("Reticulum: ONLINE")
print("GNOMEMESH identity created")
print()
print(
    "Destination:",
    RNS.prettyhexrep(destination.hash)
)
print()
print("Waiting for messages...")
print("Press CTRL+C to stop.")
print()


def received_message(message):
    print()
    print("📡 MESSAGE RECEIVED")
    print("-------------------")
    print(message.decode("utf-8"))
    print()


destination.set_packet_callback(
    received_message
)

destination.announce()

while True:
    time.sleep(1)
