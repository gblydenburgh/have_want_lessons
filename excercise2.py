#!/usr/bin/env python3
from typing import Any, TypeVar
import argparse
import copy
from pprint import pprint
import re
T = TypeVar("T")

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

bad_have_by_id = {
    "10": {"vlan_id": "10", "name": "USERS"}
}

normalized_have_by_id = {
    10: {"vlan_id": 10, "name": "USERS"}
}

normalized_effective_by_id = {
    10: {"vlan_id": 10, "name": "USERS"}
}

# Representation of the portion of the running config retrieved
# from a cisco_ios device
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
# Representation of the portion of the running config retrieved
# from a cisco_ios device, after a merge change was successfully run.
POST_MERGE_RUNNING_CONFIG = """
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

VALID_VLAN_CONFIG = """
vlan 10
 name USERS
!
"""

NON_INTEGER_VLAN_CONFIG = """
vlan BAD
 name BROKEN
!
"""

MIXED_VLAN_ID_CONFIG = """
vlan 33BAD
 name OH_CMON
!
"""

OUT_OF_RANGE_VLAN_CONFIG = """
vlan 9999
 name OUT_OF_RANGE
!
"""
INDEX_TEST_INPUT = [
    {"vlan_id": 10, "name": "USERS"},
    {"vlan_id": 20, "name": "SERVERS"},
]

VLAN_ID_PATTERN = re.compile(r"^vlan\s+(?P<vlan_id>\S+)")
VLAN_NAME_PATTERN = re.compile(r"^\s+name\s+(?P<vlan_name>.+)$", re.MULTILINE)

def simple_result_compare(expected_result: T, test_result: T, title: str) -> None:
    print(f"\n####\n# {title}\n####")
    if test_result == expected_result:
        print(f"{title}: PASS")
    else:
        print(f"{title}: FAIL")
        print(f"EXPECTED: {expected_result}")
        print(f"RESULT: {test_result}")


def run_idempotency_test() -> None:
    '''
    This is a test to verify the idempotence of the playbook using the
    merged state as the example.
    
    I does two configuration renders, one for the initial state that does not
    match the want state, and the second for the state where the want is already
    applied.
    
    After the first pass is run the result should be a populated list.
    
    After the second pass is run the result should be an empty list.
    '''
    
    want_by_id = index_vlan_data(want)
    
    first_pass_parsed = parse_vlan_config(RUNNING_CONFIG)
    first_pass_have_by_id = index_vlan_data(first_pass_parsed)
    first_pass_merged_state = build_merged_state(first_pass_have_by_id, want_by_id)
    expected_first_pass_rendered_cmds = [
        'vlan 10',
        ' name STAFF',
        'vlan 50',
        ' name IOT',
        'vlan 60',
        ' name PRINTERS'
    ]
    
    second_pass_parsed = parse_vlan_config(POST_MERGE_RUNNING_CONFIG)
    second_pass_have_by_id = index_vlan_data(second_pass_parsed)
    second_pass_merged_state = build_merged_state(second_pass_have_by_id, want_by_id)
    expected_second_pass_rendered_cmds = []
    
    for test_name, effective_state, have_by_id, expected_result in [
        (
            "IDEMPOTENCY FIRST PASS TEST",
            first_pass_merged_state,
            first_pass_have_by_id,
            expected_first_pass_rendered_cmds
        ),
        (
            "IDEMPOTENCY SECOND PASS TEST",
            second_pass_merged_state,
            second_pass_have_by_id,
            expected_second_pass_rendered_cmds
        )
    ]:
        changes = build_vlan_name_changes(have_by_id, effective_state)
        test_result = render_vlan_name_commands(changes)

        simple_result_compare(expected_result, test_result, test_name)


def run_render_test() -> None:
    changes = {
            10: {'after': 'STAFF', 'before': 'USERS'},
            50: {'after': 'IOT', 'before': None},
            60: {'after': 'PRINTERS', 'before': None}
        }
    render_result = render_vlan_name_commands(changes)
    expected_render_result = [
        'vlan 10',
        ' name STAFF',
        'vlan 50',
        ' name IOT',
        'vlan 60',
        ' name PRINTERS'
    ]
    
    simple_result_compare(expected_render_result, render_result, "RENDER TEST")
    
    remove_changes = {
        10: {'after': 'STAFF', 'before': 'USERS'},
        20: {'after': None, 'before': 'SERVERS'},
        50: {'after': 'IOT', 'before': None},
        60: {'after': 'PRINTERS', 'before': None}
    }
    render_remove_result = render_vlan_name_commands(remove_changes)
    expected_render_remove_result = [
        'vlan 10',
        ' name STAFF',
        'vlan 20',
        ' no name',
        'vlan 50',
        ' name IOT',
        'vlan 60',
        ' name PRINTERS'
    ]
    
    simple_result_compare(expected_render_remove_result, render_remove_result, "RENDER REMOVE TEST")

def run_change_test() -> None:
    have_by_id = index_vlan_data(have)
    want_by_id = index_vlan_data(want)
    merged_result = build_merged_state(have_by_id, want_by_id)
    expected_change_result = {
        10: {'after': 'STAFF', 'before': 'USERS'},
        50: {'after': 'IOT', 'before': None},
        60: {'after': 'PRINTERS', 'before': None}
    }
    change_result = build_vlan_name_changes(have_by_id, merged_result)
    
    simple_result_compare(expected_change_result, change_result, "CHANGE TEST")
    
    replaced_result = build_replaced_state(have_by_id, want_by_id)
    expected_change_result = {
        10: {'after': 'STAFF', 'before': 'USERS'},
        20: {'after': None, 'before': 'SERVERS'},
        50: {'after': 'IOT', 'before': None},
        60: {'after': 'PRINTERS', 'before': None}
    }
    change_result = build_vlan_name_changes(have_by_id, replaced_result)
    
    simple_result_compare(expected_change_result, change_result, "CHANGE REMOVE TEST")
    
    
def run_state_tests() -> None:
    have_by_id = index_vlan_data(have)
    want_by_id = index_vlan_data(want)
    delete_want_by_id = index_vlan_data(delete_want)
    
    merged_result = build_merged_state(have_by_id, want_by_id)
    expected_merged_result = {
        10: {'vlan_id': 10, 'name': 'STAFF'},
        20: {'vlan_id': 20, 'name': 'SERVERS'},
        30: {'vlan_id': 30, 'name': 'VOICE'},
        40: {'vlan_id': 40, 'name': 'GUEST'},
        50: {'vlan_id': 50, 'name': 'IOT'},
        60: {'vlan_id': 60, 'name': 'PRINTERS'}
    }

    simple_result_compare(expected_merged_result, merged_result, "STATE MERGED TEST")
    
    replaced_result = build_replaced_state(have_by_id, want_by_id)
    expected_replaced_result = {
        10: {'name': 'STAFF', 'vlan_id': 10},
        20: {'vlan_id': 20},
        30: {'name': 'VOICE', 'vlan_id': 30},
        40: {'name': 'GUEST', 'vlan_id': 40},
        50: {'name': 'IOT', 'vlan_id': 50},
        60: {'name': 'PRINTERS', 'vlan_id': 60}
    }
    
    simple_result_compare(expected_replaced_result, replaced_result, "STATE REPLACED TEST")
    
    overridden_result = build_overridden_state(have_by_id, want_by_id)
    expected_overridden_result = {
        10: {'name': 'STAFF', 'vlan_id': 10},
        20: {'vlan_id': 20},
        30: {'vlan_id': 30},
        40: {'name': 'GUEST', 'vlan_id': 40},
        50: {'name': 'IOT', 'vlan_id': 50},
        60: {'name': 'PRINTERS', 'vlan_id': 60}
    }
    
    simple_result_compare(expected_overridden_result, overridden_result, "STATE OVERRIDDEN TEST")
    
    deleted_result = build_deleted_state(have_by_id, delete_want_by_id)
    expected_deleted_result = {
        10: {'vlan_id': 10},
        20: {'vlan_id': 20},
        30: {'name': 'VOICE', 'vlan_id': 30},
        40: {'name': 'GUEST', 'vlan_id': 40},
        60: {'vlan_id': 60}
    }
    
    simple_result_compare(expected_deleted_result, deleted_result, "STATE DELETED TEST")


def run_index_tests() -> None:
    expected_result = {
        10: {'vlan_id': 10, 'name': 'USERS'},
        20: {'vlan_id': 20, 'name': 'SERVERS'}
        }
    result = index_vlan_data(INDEX_TEST_INPUT)
    
    simple_result_compare(expected_result, result, "INDEX TEST")


def run_parser_tests() -> None:
    expected_result = [{'vlan_id': 10, 'name': 'USERS'}]
    result = parse_vlan_config(VALID_VLAN_CONFIG)
    simple_result_compare(expected_result, result, "VALID VLAN TEST")
        
    non_integer_error = "vlan_id value of BAD is not an integer."
    mixed_vlan_id_error = "vlan_id value of 33BAD is not an integer."
    out_of_range_error = "vlan_id is out of range: 9999"
    
    for test_config, expected_error, title in [
        (NON_INTEGER_VLAN_CONFIG, non_integer_error, "NON-INTEGER VLAN TEST"),
        (MIXED_VLAN_ID_CONFIG, mixed_vlan_id_error, "MIXED VLAN ID TEST"),
        (OUT_OF_RANGE_VLAN_CONFIG, out_of_range_error, "OUT-OF-RANGE VLAN TEST")
    ]:
        print(f"\n####\n# {title}\n####")
        try:
            parse_vlan_config(test_config)
        except ValueError as e:
            if str(e) == expected_error:
                print(f"{title}: PASS")
            else:
                print(f"{title}: FAIL")
                print(f"EXPECTED ERROR: {expected_error}")
                print(f"RECEIVED ERROR: {str(e)}")
        else:
            print(f"{title}: FAIL")
            print(f"EXPECTED ERROR: {expected_error}")
            print("RESULT: Task executed error free.")
            
    bad_have_by_id_result = {10: {'after': 'USERS', 'before': None}}
    normalized_have_by_id_result = {}
    
    for test_config, expected_result, title in [
        (bad_have_by_id, bad_have_by_id_result, "FALSE DIFF TEST"),
        (normalized_have_by_id, normalized_have_by_id_result, "NO DIFF TEST")
    ]:
        result = build_vlan_name_changes(test_config, normalized_effective_by_id)
        
        simple_result_compare(expected_result, result, title)

    
def parse_vlan_config(config: str) -> list[dict[str, Any]]:
    parsed_config:list[dict[str, Any]] = []
    
    for block in config.split('!'):
        temp_dict: dict[str, Any] = {}
        block = block.strip()
        
        if not block:
            continue
        
        vlan_id_match = VLAN_ID_PATTERN.search(block)
        vlan_id_string = vlan_id_match.group("vlan_id") if vlan_id_match else None
        
        if vlan_id_string is None:
            continue
        
        try:
            vlan_id = int(vlan_id_string)
        except ValueError as e:
            raise ValueError(
                f"vlan_id value of {vlan_id_string} is not an integer."
                ) from e
            
        
        if 1 <= vlan_id <= 4094:
            temp_dict['vlan_id'] = vlan_id
        else:
            raise ValueError(
                f"vlan_id is out of range: {vlan_id}"
                )
        
        vlan_name_match = VLAN_NAME_PATTERN.search(block)
        vlan_name = vlan_name_match.group("vlan_name") if vlan_name_match else None

        if vlan_name is not None:
            temp_dict['name'] = vlan_name
            

        parsed_config.append(temp_dict)
    
    return parsed_config


def index_vlan_data(vlan_data: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    parsed: dict[int, dict[str, Any]] = {}
    for item in vlan_data:
        vlanid = item["vlan_id"]
        parsed[vlanid]=item
        
    return parsed


def diff_vlan_name_states(
    have_by_id: dict[int, dict[str, Any]],
    want_by_id: dict[int, dict[str, Any]],
    common: set[int]
) -> dict[int, str]:
    comp_data: dict[int, str] = {}
    for vlan_id in common:
        have_vlan = have_by_id[vlan_id]
        want_vlan = want_by_id[vlan_id]

        # print(vlan_id)
        # print(f"HAVE: {have_vlan}")
        # print(f"WANT: {want_vlan}")
        
        if "name" in have_vlan and "name" in want_vlan:
            if have_vlan["name"] == want_vlan["name"]:
                # print(f"Vlan: {vlan_id} has the same name attribute.")
                comp_data[vlan_id]="name_same"
            else:
                # print(f"Vlan: {vlan_id} has differing name attributes.")
                comp_data[vlan_id]="name_different"
        elif "name" in have_vlan and "name" not in want_vlan:
            # print(f"Vlan {vlan_id} name only in have.")
            comp_data[vlan_id]="name_only_have"
        elif "name" not in have_vlan and "name" in want_vlan:
            # print(f"Vlan {vlan_id} name only in want.")
            comp_data[vlan_id]="name_only_want"
        else:
            # print(f"Vlan {vlan_id} has no name attribute.")
            comp_data[vlan_id]="name_absent_both"
            
    return dict(sorted(comp_data.items()))


def build_merged_state(
    have_by_id: dict[int, dict[str, Any]],
    want_by_id: dict[int, dict[str, Any]]
) -> dict[int, dict[str, Any]]:
    merged = copy.deepcopy(have_by_id)

    for vlan_id, want_vlan in want_by_id.items():
        if vlan_id not in merged:
            merged[vlan_id] = want_vlan.copy()
        else:
            merged[vlan_id].update(want_vlan)
    
    return dict(sorted(merged.items()))


def build_replaced_state(
    have_by_id: dict[int, dict[str, Any]],
    want_by_id: dict[int, dict[str, Any]]
) -> dict[int, dict[str, Any]]:
    replaced = copy.deepcopy(have_by_id)

    for vlan_id, want_vlan in want_by_id.items():
        replaced[vlan_id] = want_vlan.copy()
            
    return dict(sorted(replaced.items()))


def build_overridden_state(
    have_by_id: dict[int, dict[str, Any]],
    want_by_id: dict[int, dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    overridden = copy.deepcopy(want_by_id)
    
    for vlan_id in have_by_id:
        if vlan_id not in overridden:
            overridden[vlan_id] = {"vlan_id": vlan_id}
    
    return dict(sorted(overridden.items()))


def build_deleted_state(
    have_by_id: dict[int, dict[str, Any]],
    want_by_id: dict[int, dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    deleted = copy.deepcopy(have_by_id)
    
    for vlan_id in want_by_id:
        if vlan_id in deleted:
            deleted[vlan_id] = {"vlan_id": vlan_id}
        
    return dict(sorted(deleted.items()))
    
def build_vlan_name_changes(
    have_by_id: dict[int, dict[str, Any]],
    effective_by_id: dict[int, dict[str, Any]],
) -> dict[int, dict[str, Any]]:
    changes: dict[int, dict[str, Any]] = {}
    
    # Unique marker used to distinguish a missing "name" key
    # from a "name" key whose actual value is None.
    missing = object()
    
    for vlan_id, have_vlan in have_by_id.items():
        # Determine if the have vlanid is in effective
        # If it isn't it is preserved/skipped
        if vlan_id not in effective_by_id:
            continue
        
        effective_vlan = effective_by_id[vlan_id]
        
        # Determine if the have and effective have the same "name" attribute
        # This will also validate if it is missing in both lists
        # If it is the same it is preserved/skipped
        if have_vlan.get("name", missing) == effective_vlan.get("name", missing):
            continue
        # If have doesn't have a name attribute, effective must.
        # Add the attribute to the have
        elif "name" not in have_vlan:
            changes[vlan_id] = {
                "before": None,
                "after": effective_vlan['name']
                }
        # If the effective doesn't have a name attribute, the existing have does.
        # Remove it.
        elif "name" not in effective_vlan:
            changes[vlan_id] = {
                "after": None,
                "before": have_vlan['name']
                }
        # Both have and effective has a name attribute.
        # Change the have to match effective
        elif have_vlan['name'] != effective_vlan['name']:
            changes[vlan_id] = {
                "after": effective_vlan['name'],
                "before": have_vlan['name']
                }
        else:
            raise RuntimeError(
                f"Unhandled name comparison for VLAN {vlan_id}: "
                f"HAVE={have_vlan}, EFFECTIVE={effective_vlan}"
            )

    for e_vlanid, effective_vlan in effective_by_id.items():
        if e_vlanid not in have_by_id and "name" in effective_vlan:
            changes[e_vlanid] = {
                "after": effective_vlan['name'],
                "before": None
                }
            
    return dict(sorted(changes.items()))


def render_vlan_name_commands(
    changes: dict[int, dict[str, Any]],
) -> list[str]:
    commands: list[str] = []
    negate_prefix = "no"
    for vlan_id, change_state in sorted(changes.items()):
        commands.append(f"vlan {vlan_id}")
        if change_state['after'] is None:
            commands.append(f" {negate_prefix} name")
        else:
            commands.append(f" name {change_state['after']}")
    
    return commands


def run_tests() -> None:
    run_parser_tests()
    run_index_tests()
    run_state_tests()
    run_change_test()
    run_render_test()
    run_idempotency_test()


def main() -> None:
    parsed = parse_vlan_config(RUNNING_CONFIG)
    post_merge_parsed = parse_vlan_config(POST_MERGE_RUNNING_CONFIG)
    have_by_id = index_vlan_data(parsed)
    post_merge_have_by_id = index_vlan_data(post_merge_parsed)
    print("Haves:")
    pprint(have_by_id)
    print("Haves (POST MERGE):")
    pprint(post_merge_have_by_id)
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
    ### MERGED TESTING ###
    print("Merged:")
    merged_by_id = build_merged_state(have_by_id, want_by_id)
    pprint(merged_by_id)
    print("Merged (POST):")
    post_merged_by_id = build_merged_state(post_merge_have_by_id, want_by_id)
    pprint(post_merged_by_id)
    ### REPLACED TESTING ###
    print("Replaced:")
    replaced_by_id = build_replaced_state(have_by_id, want_by_id)
    pprint(replaced_by_id)
    print("Overridden:")
    overridden_by_id = build_overridden_state(have_by_id, want_by_id)
    pprint(overridden_by_id)
    print("Deleted:")
    deleted_by_id = build_deleted_state(have_by_id, delete_want_by_id)
    pprint(deleted_by_id)
    for state_name, effective_state, haves in [
        ("MERGED", merged_by_id, have_by_id),
        ("MERGED (POST)", post_merged_by_id, post_merge_have_by_id),
        ("REPLACED", replaced_by_id, have_by_id),
        ("OVERRIDDEN", overridden_by_id, have_by_id),
        ("DELETED", deleted_by_id, have_by_id)
        ]:
        print(state_name + ':')
        changes = build_vlan_name_changes(haves, effective_state)
        print("Calculated Changes:")
        pprint(changes)
        print("Rendered Config:")
        pprint(render_vlan_name_commands(changes))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="VLAN have/want state engine demo."
    )
    parser.add_argument(
        "--run",
        choices=("main", "tests", "both"),
        default="main",
        help=(
            "What to execute: 'main' runs the demo (default), "
            "'tests' runs the test suite only, 'both' runs the demo then the tests."
        ),
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()

    if args.run in ("main", "both"):
        main()

    if args.run in ("tests", "both"):
        run_tests()
