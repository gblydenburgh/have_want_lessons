"""Checks for lesson 0003. Run: python3 lessons/code/l0003_check.py"""

from l0003_switch import IosSwitch


def main() -> None:
    sw1 = IosSwitch("sw1")
    sw2 = IosSwitch("sw2")
    sw1.plan_vlan(10)
    sw2.plan_vlan(20)
    sw2.plan_vlan(30)

    assert sw1.commands() == ["vlan 10"], (
        f"Check 1: sw1 would get {sw1.commands()!r}, expected ['vlan 10']"
    )
    assert sw2.commands() == ["vlan 20", "vlan 30"], (
        f"Check 1: sw2 would get {sw2.commands()!r}, "
        "expected ['vlan 20', 'vlan 30']"
    )
    print("Check 1 passed: each switch gets only its own VLANs")

    assert sw1.vlans_to_add is not sw2.vlans_to_add, (
        "Check 2: sw1 and sw2 still share one vlans_to_add list"
    )
    print("Check 2 passed: each switch has its own vlans_to_add list")

    assert "vlans_to_add" not in vars(IosSwitch), (
        "Check 3: IosSwitch still has a class attribute vlans_to_add. "
        "Per-switch data belongs on each instance, so it reads as shared."
    )
    print("Check 3 passed: no shared vlans_to_add is left on the class")

    assert "max_vlan_id" in vars(IosSwitch), (
        "Check 4: max_vlan_id is no longer a class attribute"
    )
    assert "max_vlan_id" not in vars(sw1), (
        "Check 4: each instance stores its own max_vlan_id"
    )
    print("Check 4 passed: max_vlan_id is stored once, on the class")

    try:
        sw1.plan_vlan(4095)
    except ValueError:
        pass
    else:
        raise AssertionError("Check 5: VLAN 4095 was accepted")
    assert sw1.commands() == ["vlan 10"], (
        f"Check 5: a rejected VLAN changed sw1's plan: {sw1.commands()!r}"
    )
    print("Check 5 passed: out-of-range VLAN IDs are still rejected")
    print("All checks passed.")


if __name__ == "__main__":
    main()
