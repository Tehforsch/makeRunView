import os, tools, logging

class Dependency:
    """The biggest set of connected files that can be cleaned by executing one function."""
    def __init__(self, mrv, originFile, starts, targets, command, runCommandOnStartFile = True, printOutput = True, exactCommand = False):
        self.invalid = False
        self.mrv = mrv
        path = tools.getFilePath(originFile.fileName)
        if type(starts) != list:
            starts = [starts]
        if type(targets) != list:
            targets = [targets]
        if len(starts) == 0 or len(targets) == 0:
            self.invalid = True
        self.starts = mrv.convertLocalFileNamesToStates(starts, path)
        self.targets = mrv.convertLocalFileNamesToStates(targets, path)
        self.originFile = originFile
        self.command = command
        self.printOutput = printOutput
        self.exactCommand = exactCommand
        self.runCommandOnStartFile = runCommandOnStartFile 

    def clean(self, workPath):
        if self.command is None:
            return None
        if type(self.command) == str:
            if self.exactCommand:
                return tools.executeExactCommand(workPath, self.command)
            else:
                if self.runCommandOnStartFile:
                    return tools.executeStandardCommand(workPath, self.starts[0].fname, self.command)
                else:
                    return tools.executeStandardCommand(workPath, self.targets[0].fname, self.command)
        else:
            logging.error("makeRunView does not support custom functions yet, try to get by with terminal commands")

    def __str__(self):
        return "[" + ", ".join(map(self.mrv.niceFilename, self.starts)) + "] -> [" + ", ".join(map(self.mrv.niceFilename, self.targets)) + "] " + self.command 

