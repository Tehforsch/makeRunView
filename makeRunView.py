import os, logging, ownUtils, executor, observer, time, createDependencies, config

class MakeRunView:
    def __init__(self, workPath):
        self.workPath = workPath

        logging.info("Checking files")
        self.files = []
        self.polluted = []
        self.scanForFiles(self.workPath)
        logging.info("Found " + str(len(self.files)) + " files")
        
        createDependencies.createDependencies(self, map(lambda x : x.fname, self.files))

        logging.info("Creating file tree")
        self.createFileTree()

        self.obs = observer.Observer(self)
        self.observeFiles()
        self.ignoreNotifications = False
        self.SAFETYTIME = 1

    def observeFiles(self):
        for fileState in self.files:
            if fileState.shouldBeObserved():
                self.obs.addFile(fileState.fname)

    def createFileTree(self):
        for d in self.dependencies:
            f1state = self.findFileState(d.f1)
            f2state = self.findFileState(d.f2)
            if f1state is None:
                logging.warning("Start file referenced in dependency does not exist: " + d.f1 + "... Creating a file state")
                f1state = self.addFileState(d.f1)
            if f2state is None:
                logging.warning("End file referenced in dependency does not exist: " + d.f2 + "... Creating a file state")
                f2state = self.addFileState(d.f2)
            f1state.successors.append(d)
            f2state.predecessors.append(d)

    def scanForFiles(self, currentFolder):
        logging.debug("RUN " + currentFolder)
        for thing in os.listdir(currentFolder):
            fullPathToThing = os.path.join(currentFolder, thing)
            logging.debug("CHK " + fullPathToThing)
            if os.path.isdir(fullPathToThing):
                self.scanForFiles(os.path.join(currentFolder, thing))
            elif os.path.isfile(fullPathToThing):
                logging.debug("ADD " + fullPathToThing)
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
        logging.info("File changed: " + self.niceFilename(fname))
        self.polluted.append(fileState)

    def handle(self):
        # Check for polluted files, 
        if len(self.polluted) != 0:
            logging.info("found polluted file " + self.polluted[0].fname)
            # Files are polluted, ignore incoming notifications about changed files
            # because those will most likely be the cleaning process itself.
            self.ignoreNotifications = True
            self.cleanTree(self.polluted[0])
            self.polluted = []
            time.sleep(self.SAFETYTIME)
            self.ignoreNotifications = False
        
    def findFileState(self, fname):
        for fileState in self.files:
            if fileState.fname == fname:
                return fileState
        return None

    def addFileState(self, fname):
        fileState = FileState(fname)
        self.files.append(fileState)
        return fileState

    def cleanTree(self, startingState):
        output = startingState.clean(self.workPath)
        if output is not None and startingState.fileType != ".tex":
            logging.info("Cleaned " + self.niceFilename(startingState.fname) + ", Output:")
            for l in output.splitlines():
                logging.info(l)
        for state in startingState.successors:
            self.cleanTree(state)

    def niceFilename(self, fname):
        return fname.replace(self.workPath + "/", "")


class FileState:
    def __init__(self, fname):
        self.fname = fname
        self.successors = []
        self.predecessors = []
        self.fileType = ownUtils.getFileType(fname)
        self.resolvingFunction = self.findFileTypeFunction(fname)
        self.polluted = []

    def clean(self, workPath):
        if self.resolvingFunction is None:
            return None
        return self.resolvingFunction(workPath, self.fname)

    def findFileTypeFunction(self, fname):
        if self.fileType == ".gpi": # Gnuplot
            return executor.gnuplot
        if self.fileType == ".py": # Python script
            return executor.python
        if self.fileType == ".tex": # Latex
            return executor.latex

    def shouldBeObserved(self):
        return self.fileType in config.fileTypesToWatch

