import os, logging
from makeRunView.utils import fileUtils, osUtils
from makeRunView import tools
from makeRunView import config
from makeRunView.filestate import FileState

class Dependency:
    """The biggest set of connected files that can be cleaned by executing one function."""
    def __init__(self, starts, targets, command=None, runInStartFolder = True, printOutput = True):
        self.starts = starts
        self.targets = targets
        self.command = command
        self.printOutput = printOutput
        self.runInStartFolder = runInStartFolder 
        self.initialized = False

    def initialize(self, mrv, originFile, pathIsRelativeToProject=False, explicit=False):
        self.mrv = mrv
        self.explicit = explicit
        self.originFile = originFile
        if self.starts is None or self.targets is None: # Faulty module
            self.invalid = True
            return
        if pathIsRelativeToProject:
            path = ""
        else:
            path = fileUtils.getFilePath(originFile.fname)
        if not type(self.starts) is list:
            self.starts = [self.starts]
        if not type(self.targets) is list:
            self.targets = [self.targets]
        startsCopy = self.starts[:]
        targetsCopy = self.targets[:]
        self.invalid = False
        if type(self.starts) != list:
            self.starts = [self.starts]
        if type(self.targets) != list:
            self.targets = [self.targets]
        if type(self.starts[0]) != FileState:
            self.starts = mrv.convertLocalFileNamesToStates(self.starts, path)
        if type(self.targets[0]) != FileState:
            self.targets = mrv.convertLocalFileNamesToStates(self.targets, path)
        if len(self.starts) == 0 or len(self.targets) == 0:
            self.invalid = True
        self.command = self.process(self.command)
        self.initialized = True

    def process(self, s):
        if s is None:
            return None
        s = s.replace(config.startFilePlaceholder, self.starts[0].fname)
        s = s.replace(config.targetFilePlaceholder, self.targets[0].fname)
        return s

    def clean(self, workPath):
        if self.command is None: # a dependency that is just needed for the tree structure so we know what may change, but doesn't need to get cleaned
            return None
        if type(self.command) == str:
            if self.runInStartFolder:
                return osUtils.executeCommand(workPath, self.starts[0].fname, self.command)
            else:
                return osUtils.executeCommand(workPath, self.targets[0].fname, self.command)
        else:
            logging.error("makeRunView does not support custom functions yet, try to get by with terminal commands")

    def __str__(self):
        if self.initialized:
            return "[" + ", ".join(map(self.mrv.niceFilename, self.starts)) + "] -> [" + ", ".join(map(self.mrv.niceFilename, self.targets)) + "] " + ("" if self.command is None else self.command)
        else:
            return str(self.starts) + " " + str(self.targets)
