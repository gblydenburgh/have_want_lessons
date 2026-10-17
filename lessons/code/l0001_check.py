"""Checks for lesson 0001. Run: python3 lessons/code/l0001_check.py"""

from l0001_device import Device


def main() -> None:
    try:
        r1 = Device("r1", "10.0.0.1", "ios", "netops")
    except TypeError as error:
        raise SystemExit(f"Step 1 not done yet: Device() rejected a username.\n  {error}")

    assert hasattr(r1, "username"), "Step 1: r1 has no attribute named username"
    assert r1.username == "netops", f"Step 1: r1.username is {r1.username!r}, expected 'netops'"
    print("Step 1 passed: Device stores a username")

    assert hasattr(r1, "ssh_target"), "Step 2: Device has no method named ssh_target"
    target = r1.ssh_target()
    assert target == "netops@10.0.0.1", f"Step 2: r1.ssh_target() returned {target!r}"

    sw1 = Device("sw1", "10.0.0.2", "nxos", "admin")
    assert sw1.ssh_target() == "admin@10.0.0.2", "Step 2: wrong result for a second device"
    assert r1.ssh_target() == "netops@10.0.0.1", "Step 2: r1 changed when sw1 was created"
    print("Step 2 passed: ssh_target works for each device separately")
    print("All checks passed.")


if __name__ == "__main__":
    main()
