from command import Command
from leader import Leader
from follower import Follower

command = Command("anpaddddd", True)
print(command.getOriginal())
print(command.getTokiPona())
print(command.getPadded())

leader = Leader("north")
print(leader.getEncodedCommand())
follower = Follower(leader.getEncodedCommand())
print(follower.getDecodedCommand())
leader.setCommand("watch")
print(leader.getEncodedCommand())
follower.setCommand(leader.getEncodedCommand())
print(follower.getDecodedCommand())