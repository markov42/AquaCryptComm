from command import Command
    
class Leader:
    def __init__(self, comm):
        self.command = Command(comm)
    
    def setCommand(self, comm):
        self.command = Command(comm)

    def getEncodedCommand(self):
        return self.command.getPadded()