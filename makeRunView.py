import os, logging, ownUtils, executor, observer, time, config
from fileState import FileState
from dependency import Dependency
from createDependencies import createDependencies

class MakeRunView:
    def __init__(self, workPath):
        self.workPath = workPath
        self.polluted = []

        logging.info("Checking files")
        self.files = []
        self.scanForFiles(self.workPath)
        logging.info("Found " + str(len(self.files)) + " files")

        logging.info("Creating dependencies.")
        self.dependencies = []
        createDependencies(self, self.files)
        
        logging.info("Created " + str(len(self.dependencies)) + " dependencies")
        for d in self.dependencies:
            logging.debug(self.niceFilename(d.start) + "->" + str(list(map(lambda x : self.niceFilename(x), d.targets))))

        logging.info("Creating file tree")
        self.createFileTree()

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

    def createFileTree(self):
        for d in self.dependencies:
            d.start.successors.append(d)

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
        for l in bufferOutput.splitlines():
            print(str(l, "utf-8"))
        logging.info("-------------------------------------------------")

    def outputWanted(self, dependency, output):
        if dependency.start.fileType == config.latexFileType:
            for l in output.splitlines():
                if "No pages of output" in str(l):
                    return True
        return dependency.start.fileType in config.fileTypesToPrintOutput
    
    def cleanedMessage(self, dependency, output):
        logging.info("Cleaned " + self.niceFilename(dependency.start))
        if output is not None and self.outputWanted(dependency, output):
            self.printOutput(output)

    def cleanTree(self, startingState):
        for dependency in startingState.successors:
            output = dependency.clean(self.workPath)
            self.cleanedMessage(dependency, output)
            for state in dependency.targets:
                self.cleanTree(state)

    def handle(self):
        # Check for polluted files, 
        if len(self.polluted) != 0:
            logging.info("found polluted file " + self.niceFilename(self.polluted[0]))
            # Files are polluted, ignore incoming notifications about changed files
            # because those will most likely be the cleaning process itself.
            self.ignoreNotifications = True
            self.cleanTree(self.polluted[0])
            self.polluted = []
            time.sleep(config.safetyTime)
            self.ignoreNotifications = False

    def observeFiles(self):
        for fileState in self.files:
            if fileState.shouldBeObserved():
                self.obs.addFile(fileState.fname)

    def findFileState(self, fname):
        for fileState in self.files:
            if fileState.fname == fname:
                return fileState
        return None

    def addDependency(self, startFname, targetFnames, cleanFunction=None):
        targets = []
        start = self.findFileState(startFname)
        if not start:
            start = self.addFileState(startFname)
            logging.warning("Referenced file doesn't exist. Added a file state for " + self.niceFilename(start) + ".")
        for targetFname in targetFnames:
            target = self.findFileState(targetFname)
            if not target:
                target = self.addFileState(targetFname)
                logging.warning("Referenced file doesn't exist. Added a file state for " + self.niceFilename(target) + ".")
            targets.append(target)
        self.dependencies.append(Dependency(start, targets, cleanFunction))

    def addFileState(self, fname):
        fileState = FileState(fname)
        self.files.append(fileState)
        return fileState

    def niceFilename(self, fileState):
        return fileState.fname.replace(self.workPath + "/", "")
