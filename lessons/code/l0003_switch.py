"""Lesson 0003: your turn. Edit this file, then run l0003_check.py."""


class IosSwitch:
    """One IOS access switch, and the VLANs this run will add to it."""

    max_vlan_id = 4094
    vlans_to_add = []

    def __init__(self, hostname: str) -> None:
        self.hostname = hostname

    def plan_vlan(self, vlan_id: int) -> None:
        if not 1 <= vlan_id <= self.max_vlan_id:
            raise ValueError(f"VLAN ID out of range: {vlan_id}")
        self.vlans_to_add.append(vlan_id)

    def commands(self) -> list[str]:
        return [f"vlan {vlan_id}" for vlan_id in self.vlans_to_add]


if __name__ == "__main__":
    sw1 = IosSwitch("sw1")
    sw2 = IosSwitch("sw2")
    sw1.plan_vlan(10)
    sw2.plan_vlan(20)
    print("sw1:", sw1.commands())
    print("sw2:", sw2.commands())
