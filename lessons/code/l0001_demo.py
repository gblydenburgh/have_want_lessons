class Device:
    def __init__(self, hostname, mgmt_ip, platform):
        self.hostname = hostname
        self.mgmt_ip = mgmt_ip
        self.platform = platform

    def describe(self):
        return f"{self.hostname} ({self.platform}) at {self.mgmt_ip}"


r1 = Device("r1", "10.0.0.1", "ios")
sw1 = Device("sw1", "10.0.0.2", "nxos")
print(r1.describe())
