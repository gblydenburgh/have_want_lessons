from typing import Any
import re

VLAN_ID_PATTERN = re.compile(r"^vlan\s+(?P<vlan_id>\S+)")
VLAN_NAME_PATTERN = re.compile(r"^\s+name\s+(?P<vlan_name>.+)$", re.MULTILINE)

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