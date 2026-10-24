"""Lesson 0004: your turn. Edit this file, then run l0004_check.py."""


class IosSwitch:
    """One IOS access switch: the VLANs it has, and the VLANs we want."""

    def __init__(
        self, hostname: str, have_vlans: list[int], want_vlans: list[int]
    ) -> None:
        self.hostname = hostname
        self.have_vlans = have_vlans
        self.want_vlans = want_vlans

    def missing_vlans(self) -> list[int]:
        """The wanted VLAN IDs that the switch doesn't have yet."""
        return [
            vlan_id for vlan_id in self.want_vlans
            if vlan_id not in self.have_vlans
        ]

    def needs_change(self) -> bool:
        return len(self.missing_vlans()) > 0


def plan_push(switch: IosSwitch) -> list[str]:
    """The lines to send to one switch; empty if it already matches."""
    if switch.needs_change:
        lines = [f"vlan {vlan_id}" for vlan_id in switch.missing_vlans()]
        return lines + ["end", "write memory"]
    return []


if __name__ == "__main__":
    sw1 = IosSwitch("sw1", have_vlans=[1, 10], want_vlans=[10, 20])
    sw2 = IosSwitch("sw2", have_vlans=[1, 10, 20], want_vlans=[10, 20])
    print("sw1:", plan_push(sw1))
    print("sw2:", plan_push(sw2))
