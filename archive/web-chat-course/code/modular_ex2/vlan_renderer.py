from typing import Any

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