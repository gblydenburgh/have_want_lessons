"""Checks for lesson 0002. Run: python3 lessons/code/l0002_check.py"""

from l0002_want import merge_want


def main() -> None:
    have = {"vlan_id": 10, "name": "users", "state": "active"}
    overrides = {"name": "staff"}
    want = merge_want(have, overrides)

    expected_want = {"vlan_id": 10, "name": "staff", "state": "active"}
    assert want == expected_want, f"Check 1: merge_want returned {want!r}, expected {expected_want!r}"
    print("Check 1 passed: WANT has the override applied")

    assert have == {"vlan_id": 10, "name": "users", "state": "active"}, (
        f"Check 2: HAVE was changed; it is now {have!r}"
    )
    assert want is not have, "Check 2: merge_want returned the HAVE dict itself"
    print("Check 2 passed: HAVE is unchanged, and WANT is a separate dict")

    assert overrides == {"name": "staff"}, f"Check 3: the overrides dict was changed: {overrides!r}"
    print("Check 3 passed: the overrides are unchanged")
    print("All checks passed.")


if __name__ == "__main__":
    main()
