class IosRouter:
    def __init__(self, hostname):
        self.hostname = hostname

    def show_version(self):
        return f"{self.hostname}: show version"

    def save_command():
        return "write memory"


r1 = IosRouter("r1")
print(r1.show_version())
print(r1.save_command())
