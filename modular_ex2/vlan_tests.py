from typing import TypeVar
from vlan_diff import build_vlan_name_changes
from vlan_parser import parse_vlan_config
from vlan_renderer import render_vlan_name_commands
from vlan_states import (
    build_deleted_state,
    build_merged_state,
    build_overridden_state,
    build_replaced_state,
    index_vlan_data,
)


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

bad_have_by_id = {
    "10": {"vlan_id": "10", "name": "USERS"}
}

normalized_have_by_id = {
    10: {"vlan_id": 10, "name": "USERS"}
}

normalized_effective_by_id = {
    10: {"vlan_id": 10, "name": "USERS"}
}

def simple_result_compare(expected_result: T, test_result: T, title: str) -> None:
    print(f"\n####\n# {title}\n####")
    if test_result == expected_result:
        print(f"{title}: PASS")
    else:
        print(f"{title}: FAIL")
        print(f"EXPECTED: {expected_result}")
        print(f"RESULT: {test_result}")


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
    
    simple_result_compare(expected_render_remove_result, render_remove_result, "RENDER REMOVETEST")

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

def main() -> None:
    run_parser_tests()
    run_index_tests()
    run_state_tests()
    run_change_test()
    run_render_test()


if __name__ == "__main__":
    main()
    