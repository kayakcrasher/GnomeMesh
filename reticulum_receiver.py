import time
import RNS

APP_NAME = "gnomemesh"
ASPECT = "message"


reticulum = RNS.Reticulum()

identity = RNS.Identity()

destination = RNS.Destination(
    identity,
    RNS.Destination.IN,
    RNS.Destination.SINGLE,
    APP_NAME,
    ASPECT
)


def received_message(message, packet):

    print()
    print("================================")
    print("📡 GNOMEMESH MESSAGE RECEIVED")
    print("================================")
    print()

    try:
        print(message.decode("utf-8"))
    except UnicodeDecodeError:
        print(message)

    print()
    print("Reticulum packet received successfully.")
    print()


destination.set_packet_callback(
    received_message
)

print()
print("================================")
print(" GNOMEMESH RETICULUM RECEIVER")
print("================================")
print()
print("Destination:")
print(RNS.prettyhexrep(destination.hash))
print()
print("Waiting for sender...")
print("Press CTRL+C to stop.")
print()


destination.announce()


while True:
    time.sleep(1)
