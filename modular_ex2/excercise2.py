#!/usr/bin/env python3
from pprint import pprint
from vlan_parser import parse_vlan_config
from vlan_states import (
    build_deleted_state,
    build_merged_state,
    build_overridden_state,
    build_replaced_state,
    index_vlan_data,
)
from vlan_diff import (
    build_vlan_name_changes,
    diff_vlan_name_states,
)
from vlan_renderer import render_vlan_name_commands


have = [
    {"vlan_id": 10, "name": "USERS"},
    {"vlan_id": 20, "name": "SERVERS"},
    {"vlan_id": 30, "name": "VOICE"},
    {"vlan_id": 40, "name": "GUEST"},
    {"vlan_id": 60},
]

want = [
    {"vlan_id": 10, "name": "STAFF"},
    {"vlan_id": 20},
    {"vlan_id": 40, "name": "GUEST"},
    {"vlan_id": 50, "name": "IOT"},
    {"vlan_id": 60, "name": "PRINTERS"},
]

delete_want = [
    {"vlan_id": 10},
    {"vlan_id": 20},
] 

RUNNING_CONFIG = """
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

def main() -> None:
    parsed = parse_vlan_config(RUNNING_CONFIG)
    have_by_id = index_vlan_data(parsed)
    print("Haves:")
    pprint(have_by_id)
    want_by_id = index_vlan_data(want)
    print("Wants:")
    pprint(want_by_id)
    delete_want_by_id = index_vlan_data(delete_want)
    print("Deleted:")
    pprint(delete_want_by_id)
    print("\n" + "-" * 10 + "\n")
    # Keeping around for reference if I have to reliearn this.
    common = have_by_id.keys() & want_by_id.keys()
    print("Common Key Name States:")
    pprint(diff_vlan_name_states(have_by_id, want_by_id, common))
    ####
    print("Merged:")
    merged_by_id = build_merged_state(have_by_id, want_by_id)
    pprint(merged_by_id)
    print("Replaced:")
    replaced_by_id = build_replaced_state(have_by_id, want_by_id)
    pprint(replaced_by_id)
    print("Overridden:")
    overridden_by_id = build_overridden_state(have_by_id, want_by_id)
    pprint(overridden_by_id)
    print("Deleted:")
    deleted_by_id = build_deleted_state(have_by_id, delete_want_by_id)
    pprint(deleted_by_id)
    for state_name, effective_state in [
        ("MERGED", merged_by_id),
        ("REPLACED", replaced_by_id),
        ("OVERRIDDEN", overridden_by_id),
        ("DELETED", deleted_by_id)
        ]:
        print(state_name + ':')
        changes = build_vlan_name_changes(have_by_id, effective_state)
        print("Calculated Changes:")
        pprint(changes)
        print("Rendered Config:")
        pprint(render_vlan_name_commands(changes))
        


if __name__ == "__main__":
    main()
