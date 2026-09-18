"""Controlled input fixtures for Lesson 5 idempotency exercises.

These fixtures intentionally contain no reconciliation logic.  They exist so
Lesson 5 can inject failures through observed/input state without modifying the
working implementation in ``excercise2.py``.

Use them only after the normal Lesson 5 path has first demonstrated a clean
second pass where the rendered command list is empty.

The fault cases are synthetic teaching inputs.  They are not claims about how
a particular Cisco platform will necessarily return configuration.
"""

from typing import Any


# Control case: the device reflects the full intended MERGED state after the
# first pass.  Re-running the same MERGED intent against this observation
# should result in no commands.
CONVERGED_MERGED_RUNNING_CONFIG = """
hostname SW01
!
interface GigabitEthernet1/0/1
 description SERVER_PORT
 switchport access vlan 10
!
vlan 10
 name STAFF
!
vlan 20
 name SERVERS
!
vlan 30
 name VOICE
!
vlan 40
 name GUEST
!
vlan 50
 name IOT
!
vlan 60
 name PRINTERS
!
"""


# Fault case 1: the first pass was only partially applied.  VLAN 60 never
# received its intended name.  A second pass SHOULD still produce a command for
# VLAN 60.  This is a legitimate remaining change, not a false idempotency
# failure.
PARTIAL_APPLY_RUNNING_CONFIG = """
hostname SW01
!
interface GigabitEthernet1/0/1
 description SERVER_PORT
 switchport access vlan 10
!
vlan 10
 name STAFF
!
vlan 20
 name SERVERS
!
vlan 30
 name VOICE
!
vlan 40
 name GUEST
!
vlan 50
 name IOT
!
vlan 60
!
"""


# Fault case 2: the device is logically converged, but the gathered VLAN name
# contains trailing whitespace that the parser currently preserves. The extra
# line keeps that whitespace inside the VLAN block after block-level stripping,
# allowing the exercise to expose a false second-pass change caused by incomplete
# normalization rather than by real device drift.
TRAILING_WHITESPACE_RUNNING_CONFIG = """
hostname SW01
!
vlan 10
 name STAFF 
 state active
!
vlan 20
 name SERVERS
!
vlan 30
 name VOICE
!
vlan 40
 name GUEST
!
vlan 50
 name IOT
!
vlan 60
 name PRINTERS
!
"""


# Fault case 3: the second gather returns the original pre-change observation.
# This simulates stale/cached observation or a gather path that did not see the
# applied configuration.  The reconciliation engine should therefore believe
# the original changes are still required.
STALE_SECOND_GATHER_CONFIG = """
hostname SW01
!
interface GigabitEthernet1/0/1
 description SERVER_PORT
 switchport access vlan 10
!
vlan 10
 name USERS
!
vlan 20
 name SERVERS
!
vlan 30
 name VOICE
!
vlan 40
 name GUEST
!
vlan 60
!
"""


# Fault case 4: the logical device state is converged, but one resource identity
# violates the normalized internal contract by using strings instead of ints.
# In the merged path, this malformed identity causes the state builder to fail
# when it attempts to sort mixed integer and string keys. The fixture demonstrates
# why reconciliation code depends on normalized internal state.
BAD_TYPE_HAVE_BY_ID: dict[int | str, dict[str, Any]] = {
    "10": {"vlan_id": "10", "name": "STAFF"},
    20: {"vlan_id": 20, "name": "SERVERS"},
    30: {"vlan_id": 30, "name": "VOICE"},
    40: {"vlan_id": 40, "name": "GUEST"},
    50: {"vlan_id": 50, "name": "IOT"},
    60: {"vlan_id": 60, "name": "PRINTERS"},
}


# Control for the normalization fault above.  This represents the same logical
# state with the internal contract satisfied.
NORMALIZED_CONVERGED_HAVE_BY_ID: dict[int, dict[str, Any]] = {
    10: {"vlan_id": 10, "name": "STAFF"},
    20: {"vlan_id": 20, "name": "SERVERS"},
    30: {"vlan_id": 30, "name": "VOICE"},
    40: {"vlan_id": 40, "name": "GUEST"},
    50: {"vlan_id": 50, "name": "IOT"},
    60: {"vlan_id": 60, "name": "PRINTERS"},
}
