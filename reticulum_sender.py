import time
import RNS

APP_NAME = "gnomemesh"
ASPECT = "message"


class GNOMEMESHAnnounceHandler:

    def __init__(self):
        self.aspect_filter = APP_NAME + "." + ASPECT
        self.found = []

    def received_announce(
        self,
        destination_hash,
        announced_identity,
        app_data
    ):
        if destination_hash not in self.found:

            self.found.append(destination_hash)

            print()
            print("📡 GNOMEMESH NODE FOUND")
            print(
                "Destination:",
                RNS.prettyhexrep(destination_hash)
            )


reticulum = RNS.Reticulum()

handler = GNOMEMESHAnnounceHandler()

RNS.Transport.register_announce_handler(handler)

print()
print("================================")
print("  GNOMEMESH RETICULUM SENDER")
print("================================")
print()
print("Listening for GNOMEMESH nodes...")
print()


while not handler.found:

    time.sleep(1)


destination_hash = handler.found[0]

print()
print(
    "Requesting path to:",
    RNS.prettyhexrep(destination_hash)
)

RNS.Transport.request_path(destination_hash)

print("Waiting for Reticulum path...")

while not RNS.Transport.has_path(destination_hash):

    time.sleep(1)


print("Path found!")
print()


identity = RNS.Identity.recall(destination_hash)

destination = RNS.Destination(
    identity,
    RNS.Destination.OUT,
    RNS.Destination.SINGLE,
    APP_NAME,
    ASPECT
)


message = b"Hello from GNOMEMESH through Reticulum!"

packet = RNS.Packet(
    destination,
    message
)

receipt = packet.send()

print("================================")
print("📡 MESSAGE SENT")
print("================================")
print()
print(message.decode())
print()
print("Packet receipt:", receipt)
print()
