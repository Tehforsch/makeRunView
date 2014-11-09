import os, logging, tools, observer, time, config
from dependencyManager import DependencyManager
from fileState import FileState

class MakeRunView:
    def __init__(self, workPath):
        self.workPath = workPath

        logging.debug("Checking files")
        self.files = []
        self.scanForFiles(self.workPath)
        logging.debug("Found " + str(len(self.files)) + " files")

        self.dependencyManager = DependencyManager(self, self.workPath)
        self.polluted = []
        # createDependencies(self, self.files)
        
        logging.debug("Starting observer thread")

        self.obs = observer.Observer(self)
        self.observeFiles()
        self.ignoreNotifications = False

    def scanForFiles(self, currentFolder):
        """For every file in the folder, check for dependencies and then run this function on each of the subfolders."""
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
        logging.debug("File changed: " + self.niceFilename(fileState))
        self.polluted.append(fileState)

    def notifyCreated(self, fname):
        """Gets called by the notifier thread when fname is created. """
        logging.error("not yet implemented - creation of files should add them into the system")

    def printOutput(self, dependency, bufferOutput):
        # TODO
        # There is a reason why buffers exist. This code does not take this reason into account at all.
        logging.info(dependency)
        if bufferOutput is not None and dependency.printOutput:
            for l in bufferOutput.splitlines():
                # print(str(l, "ISO-8859-1"))
                logging.info(str(l, "utf-8"))
    
    def cleanTree(self, startingState):
        """If a file has been polluted, this function takes care of all the files dependent on it."""
        self.dependencyManager.update(startingState)
        for dependency in startingState.successors:
            output = dependency.clean(self.workPath)
            self.printOutput(dependency, output)
            for state in dependency.targets:
                self.cleanTree(state)

    def handle(self):
        # Check for polluted files, 
        if len(self.polluted) != 0:
            logging.info("File is polluted: " + self.niceFilename(self.polluted[0]))
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
        """Given a absolute filename return the file state of this file if it exists. Otherwise return create a state"""
        for fileState in self.files:
            if fileState.fname == fname:
                return fileState
        # The state has not yet been created. This is probably because the file just doesn't exist yet but will exist once a specific command for a dependency is executed (e.g. pdflatex which creates a .pdf file upon creation which might not have existed before"
        return FileState(fname)


    def convertLocalFileNamesToStates(self, fileNames, path):
        """Returns the absolute path of a file fileName in a subfolder path, """
        fileNames = map(lambda filename : tools.ensureAbsPath(filename, path), fileNames)
        return list(map(lambda name : self.findFileState(name), fileNames))

    def addFileState(self, fname):
        """Given the absolute path of a file, create a file state and keep it"""
        fileState = FileState(fname)
        self.files.append(fileState)
        return fileState

    def niceFilename(self, fileState):
        """Return the fileState path relative to the project"""
        return fileState.fname.replace(self.workPath + "/", "")
