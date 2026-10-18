"""Lesson 0002: your turn. Edit this file, then run l0002_check.py."""


def merge_want(have: dict, overrides: dict) -> dict:
    """Return the WANT for one VLAN: the device's settings with the overrides applied."""
    want = have.copy()
    want.update(overrides)
    return want


if __name__ == "__main__":
    have = {"vlan_id": 10, "name": "users", "state": "active"}
    want = merge_want(have, {"name": "staff"})
    assert have == {"vlan_id": 10, "name": "users", "state": "active"}, (
        f"have has changed!: {have}."
    )
    print("HAVE:", have)
    print("WANT:", want)
    print("Needs a change:", want != have)
