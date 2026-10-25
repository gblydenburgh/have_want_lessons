"""Checks for lesson 0004. Run: python3 lessons/code/l0004_check.py"""

from l0004_switch import IosSwitch, plan_push


def main() -> None:
    compliant = IosSwitch("sw2", have_vlans=[1, 10, 20], want_vlans=[10, 20])
    assert plan_push(compliant) == [], (
        f"Check 1: sw2 already has VLANs 10 and 20, but would get "
        f"{plan_push(compliant)!r}, expected []"
    )
    print("Check 1 passed: a switch with every wanted VLAN gets no lines")

    behind = IosSwitch("sw1", have_vlans=[1, 10], want_vlans=[10, 20])
    expected = ["vlan 20", "end", "write memory"]
    assert plan_push(behind) == expected, (
        f"Check 2: sw1 is missing VLAN 20, but would get "
        f"{plan_push(behind)!r}, expected {expected!r}"
    )
    print("Check 2 passed: a switch that's missing VLANs still gets them")

    assert compliant.needs_change() is False, (
        "Check 3: needs_change() should return False for sw2"
    )
    assert behind.needs_change() is True, (
        "Check 3: needs_change() should return True for sw1"
    )
    print("Check 3 passed: needs_change is still a method returning a bool")

    assert compliant.have_vlans == [1, 10, 20], (
        f"Check 4: plan_push changed sw2's HAVE: {compliant.have_vlans!r}"
    )
    assert behind.have_vlans == [1, 10], (
        f"Check 4: plan_push changed sw1's HAVE: {behind.have_vlans!r}"
    )
    print("Check 4 passed: plan_push leaves HAVE as it was observed")
    print("All checks passed.")


if __name__ == "__main__":
    main()
