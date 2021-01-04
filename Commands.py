import osascript, json
import applescript
import os
from colorit import *
from Gestures import Gestures

"""
------------------------------------------------------------------------------------------------------------------------
Commands Class
------------------------------------------------------------------------------------------------------------------------
Utility:

Commands is a class that abstracts the implementation of commands (actions) executed as a response to gestures

------------------------------------------------------------------------------------------------------------------------
Declaration:
Takes not argument. But fetchs the commands json file in Config folder 

------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------------------------------------
"""


class Commands:
    def __init__(self):
        self.__commands = {}
        self.__gestures = Gestures()

    def updateGesturesFromJSON(self):
        json_file = open("Config/commands.json", "r")
        commands = json_file.read()
        self.__commands = json.loads(commands)
        json_file.close()

    def getCommands(self):
        self.updateGesturesFromJSON()
        return self.__commands

    def getGestureByCommand(self, command):
        gestures = self.__gestures.getGestures()
        commands = self.__commands
        return gestures[commands[str(command)]['gesture']]

    def executeCommand(self, gesture):
        command = self.getCommandByGesture(gesture)
        if command == "0":
            self.mute()
        elif command == "1":
            self.volumeUp()
        elif command == "2":
            self.volumeDown()
        elif command == "3":
            self.openSafari()
        elif command == "4":
            self.emptyTrash()
        elif command == "5":
            self.shutDown()
        elif command == "6":
            self.mute()

    def printCommands(self):
        self.updateGesturesFromJSON()
        print(color("AVAILABLE COMMANDS: ", Colors.green))
        for command in self.__commands:
            print(color("{}: {}".format(self.__commands[command]["name"], self.getGestureByCommand(command)),
                        Colors.green))

    def getCommandByGesture(self, gesture):
        self.updateGesturesFromJSON()
        for command in self.__commands:
            if self.__commands[command]["gesture"] == str(gesture):
                return command

    def commandName(self, command):
        return self.__commands[str(command)]['name']

    def changeCommandName(self, command, name):
        self.updateGesturesFromJSON()
        self.__commands[str(command)]['name'] = name
        with open('Config/commands.json', 'w') as file:
            json.dump(self.__commands, file, indent=2)

    def changeCommandGesture(self, command, gesture):
        self.updateGesturesFromJSON()
        self.__commands[str(command)]['gesture'] = gesture
        with open('Config/commands.json', 'w') as file:
            json.dump(self.__commands, file, indent=2)

    def setVolume(self, volume):
        osascript.run("set volume output volume " + str(volume))
        code, out, err = osascript.run("output volume of (get volume settings)")
        if (err):
            return False
        else:
            return out

    def volumeUp(self, by=10):
        code, out, err = osascript.run("output volume of (get volume settings)")
        return self.setVolume(int(out) + by)

    def volumeDown(self, by=10):
        code, out, err = osascript.run("output volume of (get volume settings)")
        return self.setVolume(int(out) - by)

    def openSafari(self ):
        code, out, err = osascript.run('tell app "Safari" to activate')
        return out

    def mute(self ):
        code, out, err = osascript.run('set volume output muted TRUE')
        return out

    def emptyTrash(self ):
        code, out, err = osascript.run('tell application "Finder" to empty trash')
        return out

    def shutDown(self ):
        code, out, err = osascript.run('tell app "System Events" to shut down')
        return out

