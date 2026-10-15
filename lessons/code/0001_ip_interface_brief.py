"""Lesson 0001: tracing check. Run this only AFTER your answers are graded."""


class IpInterfaceBrief:
    """Interface facts parsed from `show ip interface brief` output."""

    command: str = "show ip interface brief"

    def __init__(self, hostname: str, raw_output: str) -> None:
        self.hostname = hostname
        self.raw_output = raw_output
        self.interfaces: dict[str, dict[str, str]] = {}

    def gather(self) -> dict[str, dict[str, str]]:
        for line in self.raw_output.splitlines():
            if self.is_data_row(line):
                name, attrs = self.parse_row(line)
                self.interfaces[name] = attrs
        return self.interfaces

    def is_data_row(self, line: str) -> bool:
        return bool(line.strip()) and not line.startswith("Interface")

    def parse_row(self, line: str) -> tuple[str, dict[str, str]]:
        fields = line.split()
        return fields[0], {"ip": fields[1], "protocol": fields[-1]}


class IosIpInterfaceBrief(IpInterfaceBrief):
    network_os: str = "cisco.ios.ios"


class NxosIpInterfaceBrief(IpInterfaceBrief):
    network_os: str = "cisco.nxos.nxos"

    def is_data_row(self, line: str) -> bool:
        is_row = super().is_data_row(line)
        return is_row and not line.startswith("IP Interface Status")

    def parse_row(self, line: str) -> tuple[str, dict[str, str]]:
        name, attrs = super().parse_row(line)
        # NX-OS packs three states in one column: protocol-up/link-up/admin-up
        protocol_state = attrs["protocol"].split("/")[0]
        attrs["protocol"] = protocol_state.removeprefix("protocol-")
        return name, attrs


RAW_IOS = """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     10.0.0.1        YES NVRAM  up                    up
GigabitEthernet0/1     unassigned      YES NVRAM  administratively down down
Loopback0              192.0.2.1       YES manual up                    up
"""

RAW_NXOS = """
IP Interface Status for VRF "default"(1)
Interface            IP Address      Interface Status
Lo0                  192.0.2.11      protocol-up/link-up/admin-up
Eth1/1               10.0.1.1        protocol-down/link-down/admin-up
"""


if __name__ == "__main__":
    nx = NxosIpInterfaceBrief("nx-leaf1", RAW_NXOS)

    print("Question 1")
    print(f"  (a) nx.command                = {nx.command!r}")
    print(f"  (b) nx.network_os             = {nx.network_os!r}")
    print(f"  (c) 'command' in nx.__dict__    = {'command' in nx.__dict__}")
    print(f"      'network_os' in nx.__dict__ = {'network_os' in nx.__dict__}")
    print(f"  (d) nx.interfaces             = {nx.interfaces!r}")

    banner = 'IP Interface Status for VRF "default"(1)'
    print("Question 2")
    print(f"  (c) nx.is_data_row(banner)    = {nx.is_data_row(banner)!r}")

    result = nx.gather()
    print("Question 3")
    print(f"  (a) result                    = {result!r}")
    print(f"  (b) result is nx.interfaces   = {result is nx.interfaces}")
    print(f"  (c) hasattr(nx, 'fields')     = {hasattr(nx, 'fields')}")
    ios = IosIpInterfaceBrief("r1", RAW_IOS)
    ios_row = ios.gather()["GigabitEthernet0/1"]
    print(f"  (d) ios_row                   = {ios_row!r}")
