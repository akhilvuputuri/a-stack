"""Test-only network tripwire, loaded in child Python processes via PYTHONPATH."""
import os
import sys

def reject_network(event, args):
    if event.startswith("socket."):
        marker = os.environ.get("RELAY_NETWORK_ATTEMPTS")
        if marker:
            with open(marker, "a") as stream:
                stream.write(event + "\n")
        raise RuntimeError("Network disabled by Relay test tripwire: " + event)

sys.addaudithook(reject_network)
