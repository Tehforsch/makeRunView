import os, logging, time
from makeRunView import observer, config, dependencymanager, filestate
from makeRunView.utils import fileUtils

class MakeRunView:
    def __init__(self, workPath):
        self.workPath = workPath

        logging.debug("Checking files")
        self.files = []
        self.scanForFiles(self.workPath)
        logging.debug("Found " + str(len(self.files)) + " files")

        self.dependencyManager = dependencymanager.DependencyManager(self, self.workPath)
        self.polluted = []
        # createDependencies(self, self.files)
        
        logging.debug("Starting observer thread")

        self.obs = observer.Observer(self)
        self.observeFiles([f for f in os.listdir(self.workPath) if os.path.isdir(f)] + [workPath])
        self.ignoreNotifications = False

    def scanForFiles(self, currentFolder):
        """For every file in the folder, check for dependencies and then run this function on each of the subfolders."""
        for thing in os.listdir(currentFolder):
            fullPathToThing = os.path.join(currentFolder, thing)
            if os.path.isdir(fullPathToThing):
                self.scanForFiles(os.path.join(currentFolder, thing))
            else:
                logging.debug("Adding file state for " + fullPathToThing)
                self.addFileState(fullPathToThing)

    def notifyChanged(self, fname):
        """Gets called by the notifier thread when fname changes. """
        if self.ignoreNotifications:
            return
        # fileState = self.findFileState(fname)
        fileState = next((fileState for fileState in self.files if fileState.fname == fname), None)
        if fileState is None:
            self.addCreatedFile(fname)
        else:
            logging.info("File changed: " + self.niceFilename(fileState))
            self.polluted.append(fileState)

    def addCreatedFile(self, fname):
        """Gets called by the notifier thread when fname is created. """
        fileState = self.addFileState(fname)
        logging.info("File created: " + self.niceFilename(fileState))
        self.polluted.append(fileState)

    def printOutput(self, dependency, bufferOutput):
        # TODO
        # There is a reason why buffers exist. This code does not take this reason into account at all
        logging.info(dependency)
        if bufferOutput is not None and dependency.printOutput:
            for l in bufferOutput.splitlines():
                # print(str(l, "ISO-8859-1"))
                print(str(l, "utf-8"))

    def cleanTree(self, startingState):
        """If a file has been polluted, this function takes care of all the files dependent on it."""
        for dependency in startingState.successors:
            output = dependency.clean(self.workPath)
            self.printOutput(dependency, output)
            for state in dependency.targets:
                self.cleanTree(state)

    def handle(self):
        # Check for polluted files, 
        if len(self.polluted) != 0:
            logging.debug("File is polluted: " + self.niceFilename(self.polluted[0]))
            # Files are polluted, ignore incoming notifications about changed files
            # because those will most likely be the cleaning process itself.
            self.ignoreNotifications = True
            for poll in self.polluted:
                # The file that changed needs to be checked for new/removed dependencies.
                # This was initially done for each of the affected files (those further down the tree)
                # however this resulted in problems in some cases and also isn't needed.
                self.dependencyManager.update(poll)
                self.cleanTree(poll)
            self.polluted = []
            time.sleep(config.safetyTime)
            self.ignoreNotifications = False

    def observeFiles(self, folderList):
        # Watch already existent files for changes.
        for fileState in self.files:
            if fileState.shouldBeObserved():
                self.obs.addFile(fileState.fname)
        # Watch all folders in the project for files created within them.
        for folder in folderList:
            self.obs.addFolder(folder)


    def kill(self):
        return self.obs.kill()

    # Help functions
    def findFileState(self, fname):
        """Given a absolute filename return the file state of this file if it exists. Otherwise create a state"""
        # Side comment: If the file state doesnt exist, that probably means the physical file doesnt exist, which could happen if a dependency was created, which, upon execution creates the file (pdflatex creates a .pdf file which could not have been there before)
        return next((fileState for fileState in self.files if fileState.fname == fname), filestate.FileState(fname))

    def convertLocalFileNamesToStates(self, fileNames, path):
        """Returns the fileState of a file fileName in a subfolder path, """
        fileNames = map(lambda filename : fileUtils.ensureAbsPath(filename, path), fileNames)
        return list(map(lambda name : self.findFileState(name), fileNames))

    def addFileState(self, fname):
        """Given the absolute path of a file, create a file state and keep it"""
        fileState = filestate.FileState(fname)
        self.files.append(fileState)
        return fileState

    def niceFilename(self, fileState):
        """Return the fileState path relative to the project"""
        return fileState.fname.replace(self.workPath + "/", "")
