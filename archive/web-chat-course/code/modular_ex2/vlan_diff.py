from typing import Any

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