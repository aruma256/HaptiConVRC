import time

from pythonosc import udp_client


class RumbleTester:
    IP_ADDRESS = "127.0.0.1"
    PORT = 9001

    def __init__(self, osc_address: str):
        self.osc_client = udp_client.SimpleUDPClient(RumbleTester.IP_ADDRESS,
                                                     RumbleTester.PORT)
        self.osc_address = osc_address

    def send_test_values(self):
        for _ in range(100):
            self.osc_client.send_message(self.osc_address, 1.)
            time.sleep(0.01)
        self.osc_client.send_message(self.osc_address, 0.)
