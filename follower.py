from command import Command

class Follower:
    def __init__(self, comm):
        self.command = Command(comm, True)

    def setCommand(self, comm):
        self.command = Command(comm, True)

    def getDecodedCommand(self):
        return self.command.getOriginal()