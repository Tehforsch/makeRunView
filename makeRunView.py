import os, logging, ownUtils, executor, observer, time

class FileState:
    def __init__(self, fname):
        self.fname = fname
        self.successors = []
        self.predecessors = []
        self.resolvingFunction = self.findFileTypeFunction(fname)
        self.polluted = []

    def clean(self, workPath):
        if self.resolvingFunction is None:
            return None
        return self.resolvingFunction(workPath, self.fname)

    def findFileTypeFunction(self, fname):
        fileType = ownUtils.getFileType(fname)
        if fileType == ".gpi": # Gnuplot
            return executor.gnuplot
        if fileType == ".py": # Python script
            return executor.python

class MakeRunView:
    def __init__(self, workPath, dependencies):
        self.workPath = workPath

        logging.info("Checking files")
        self.files = []
        self.polluted = []
        self.scanForFiles(self.workPath)
        logging.info("Found " + str(len(self.files)) + " files")

        logging.info("Creating file tree")
        self.createFileTree(dependencies)

        self.obs = observer.Observer(self)
        self.observeFiles()
        self.ignoreNotifications = False
        self.SAFETYTIME = 1

    def observeFiles(self):
        for fileState in self.files:
            self.obs.addFile(fileState.fname)

    def createFileTree(self, dependencies):
        for (f1, f2) in dependencies:
            f1state = self.findFileState(f1)
            f2state = self.findFileState(f2)
            if f1state is None:
                logging.warning("Start file referenced in dependency does not exist: " + f1 + "... Creating a file state")
                f1state = self.addFileState(f1)
            if f2state is None:
                logging.warning("End file referenced in dependency does not exist: " + f2 + "... Creating a file state")
                f2state = self.addFileState(f2)
            f1state.successors.append(f2state)
            f2state.predecessors.append(f1state)

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
        if output is not None:
            logging.info("Cleaned " + self.niceFilename(startingState.fname) + ", Output:")
            logging.info(output)
        for state in startingState.successors:
            self.cleanTree(state)

    def niceFilename(self, fname):
        return fname.replace(self.workPath + "/", "")
