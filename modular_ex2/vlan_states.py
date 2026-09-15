import copy
from typing import Any

def index_vlan_data(vlan_data: list[dict[str, Any]]) -> dict[int, dict[str, Any]]:
    parsed: dict[int, dict[str, Any]] = {}
    for item in vlan_data:
        vlanid = item["vlan_id"]
        parsed[vlanid]=item
        
    return parsed

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


