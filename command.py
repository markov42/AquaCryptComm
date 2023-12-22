import json

class Command:
    markedPhoneme = 'd'
    commandLength = 9

    def __init__(self, comm, encoded=False):
        with open('tokiToEngl.json') as json_file:
            self.tokiToEngl = json.load(json_file)

        with open('englToToki.json') as json_file:
            self.englToToki = json.load(json_file)

        if(encoded):
            self.command = self.fromTokiPona(self.unpadLength(comm))
        else:
            self.command = comm

    def getTokiPona(self):
        return self.toTokiPona(self.command)

    def getPadded(self):
        return self.padLength(self.command)
    
    def getOriginal(self):
        return self.command
    
    def toTokiPona(self, comm):
        return self.englToToki[comm]
    
    def fromTokiPona(self, comm):
        return self.tokiToEngl[comm]
    
    def padLength(self, comm):
        toki = self.englToToki[comm]
        noSpace = toki.replace(' ', self.markedPhoneme)
        while(len(noSpace)<self.commandLength):
            noSpace = noSpace + self.markedPhoneme
        return noSpace

    def unpadLength(self, comm):
        reg = comm.replace(self.markedPhoneme, ' ')
        return reg.strip()




    