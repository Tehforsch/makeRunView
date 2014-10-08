import os, logging, tools, executor, observer, time, config
from dependencies import Dependencies
from fileState import FileState
# from dependency import Dependency
import imp

class MakeRunView:
    def __init__(self, workPath):
        self.workPath = workPath

        logging.info("Checking files")
        self.files = []
        self.scanForFiles(self.workPath)
        logging.info("Found " + str(len(self.files)) + " files")

        self.dependencies = Dependencies(self.workPath)
        self.polluted = []
        # createDependencies(self, self.files)
        
        logging.info("Starting observer thread")

        self.obs = observer.Observer(self)
        self.observeFiles()
        self.ignoreNotifications = False

    def scanForFiles(self, currentFolder):
        for thing in os.listdir(currentFolder):
            fullPathToThing = os.path.join(currentFolder, thing)
            if os.path.isdir(fullPathToThing):
                self.scanForFiles(os.path.join(currentFolder, thing))
            elif os.path.isfile(fullPathToThing):
                logging.debug("Adding file state for " + fullPathToThing)
                self.addFileState(fullPathToThing)
            else:
                logging.error("OH MY GOD ITS THE THING, CALL JOHN CARPENTER")

    def notifyChanged(self, fname):
        """Gets called by the notifier thread when fname changes. """
        if self.ignoreNotifications:
            return
        fileState = self.findFileState(fname)
        if fileState is None:
            raise Exception("Changed file not in file tree! Why did it get watched?")
        logging.info("File changed: " + self.niceFilename(fileState))
        self.polluted.append(fileState)

    def printOutput(self, bufferOutput):
        logging.info("-------------------------------------------------")
        # TODO
        # There is a reason why buffers exist. This code does not take this reason into account at all.
        for l in bufferOutput.splitlines():
            print(str(l, "utf-8"))
        logging.info("-------------------------------------------------")
    
    def cleanTree(self, startingState):
        self.dependencies.update(startingState)
        for dependency in startingState.successors:
            output = dependency.clean(self.workPath)
            logging.info("Cleaned " + self.niceFilename(dependency.start))
            if output is not None and dependency.outputWanted:
                self.printOutput(output)
            for state in dependency.targets:
                self.cleanTree(state)

    def handle(self):
        # Check for polluted files, 
        if len(self.polluted) != 0:
            logging.info("found polluted file " + self.niceFilename(self.polluted[0]))
            # Files are polluted, ignore incoming notifications about changed files
            # because those will most likely be the cleaning process itself.
            self.ignoreNotifications = True
            for poll in self.polluted:
                self.cleanTree(poll)
            self.polluted = []
            time.sleep(config.safetyTime)
            self.ignoreNotifications = False

    def observeFiles(self):
        for fileState in self.files:
            if fileState.shouldBeObserved():
                self.obs.addFile(fileState.fname)

    # Help functions
    def findFileState(self, fname):
        for fileState in self.files:
            if fileState.fname == fname:
                return fileState
        return None

    def addFileState(self, fname):
        fileState = FileState(fname)
        self.files.append(fileState)
        return fileState

    def niceFilename(self, fileState):
        return fileState.fname.replace(self.workPath + "/", "")
