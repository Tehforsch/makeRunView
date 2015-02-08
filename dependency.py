import os, tools, logging

class Dependency:
    """The biggest set of connected files that can be cleaned by executing one function."""
    def __init__(self, starts, targets, command=None, runCommandOnStartFile = True, printOutput = True, exactCommand = False, explicit=False):
        self.starts = starts
        self.targets = targets
        self.command = command
        self.printOutput = printOutput
        self.exactCommand = exactCommand
        self.runCommandOnStartFile = runCommandOnStartFile 
        self.initialized = False
        self.explicit = explicit

    def initialize(self, mrv, originFile, pathIsRelativeToProject=False):
        self.mrv = mrv
        if self.starts is None or self.targets is None: # Faulty module
            self.invalid = True
            return
        if pathIsRelativeToProject:
            path = ""
        else:
            path = tools.getFilePath(originFile.fileName)
        if not type(self.starts) is list:
            self.starts = [self.starts]
        if not type(self.targets) is list:
            self.targets = [self.targets]
        startsCopy = self.starts[:]
        targetsCopy = self.targets[:]
        self.starts = mrv.convertLocalFileNamesToStates(self.starts, path)
        self.targets = mrv.convertLocalFileNamesToStates(self.targets, path)
        self.originFile = originFile
        self.invalid = False
        if type(self.starts) != list:
            self.starts = [self.starts]
        if type(self.targets) != list:
            self.targets = [self.targets]
        if len(self.starts) == 0 or len(self.targets) == 0:
            self.invalid = True
        self.initialized = True

    def clean(self, workPath):
        if self.command is None: # a dependency that is just needed for the tree structure so we know what may change, but doesn't need to get cleaned
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
        if self.initialized:
            return "[" + ", ".join(map(self.mrv.niceFilename, self.starts)) + "] -> [" + ", ".join(map(self.mrv.niceFilename, self.targets)) + "] " + ("" if self.command is None else self.command)
        else:
            return str(self.starts) + " " + str(self.targets)
    
