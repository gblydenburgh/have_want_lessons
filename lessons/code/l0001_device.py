"""Lesson 0001: your turn. Edit this file, then run l0001_check.py."""


class Device:
    def __init__(self, hostname, mgmt_ip, platform, username):
        self.hostname = hostname
        self.mgmt_ip = mgmt_ip
        self.platform = platform
        self.username = username

    def describe(self):
        return f"{self.hostname} ({self.platform}) at {self.mgmt_ip}"

    def ssh_target(self):
        return f"{self.username}@{self.mgmt_ip}"


if __name__ == "__main__":
    r1 = Device("r1", "10.0.0.1", "ios", "admin")
    print(r1.describe())
    print(r1.ssh_target())
