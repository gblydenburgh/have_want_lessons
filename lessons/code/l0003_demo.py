class ConfigPush:
    commands = []                  # the config lines to send

    def __init__(self, hostname):
        self.hostname = hostname

    def add(self, line):
        self.commands.append(line)


r1 = ConfigPush("r1")
sw1 = ConfigPush("sw1")
r1.add("ip route 0.0.0.0 0.0.0.0 10.0.0.254")
sw1.add("vlan 10")

print("r1: ", r1.commands)
print("sw1:", sw1.commands)
