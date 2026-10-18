have = {"vlan_id": 10, "name": "users"}   # read from the device
want = have                                # start from what the device has
want["name"] = "staff"                     # apply the task's change

print("HAVE:", have)
print("WANT:", want)
print("Needs a change:", want != have)
