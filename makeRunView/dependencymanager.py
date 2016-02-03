import os, logging, sys
from makeRunView import config, tools
from makeRunView.utils import fileUtils
from makeRunView.dependency import Dependency
from makeRunView.filestate import FileState
import importlib.machinery
import re

class DependencyManager:
    """Checks dependencies between files by calling modules. Modules are loaded from a global module folder
    whose path is defined by config.py as well as the modules subfolder of the project path if it exists. The
    name of this subfolder is defined by config.py.
    Each module must define a check function which takes the read lines of a file as an argument
    and returns [[starts], [targets], function]"""

    def __init__(self, mrv, workPath):
        self.mrv = mrv
        self.files = self.mrv.files
        self.modules = self.loadModules(config.globalPath)
        if os.path.isdir(workPath + "/" + config.projectSubfolder):
            self.modules = self.modules + self.loadModules(workPath + "/" + config.projectSubfolder)
        self.dependencies = []
        self.initialCheck()

    def initialCheck(self):
        self.getExplicitDependencies()
        self.getImplicitDependencies()
        self.filterInvalidDependencies()
        logging.info("List of created dependencies: \n" + "\n".join(str(d) for d in self.dependencies))
    
    def filterInvalidDependencies(self):
        # Check for invalid dependencies (target or start file does not exist, this happens if dependencies are misinterpreted. Filter those dependencies out
        invalidDependencies = [x for x in self.dependencies if x.invalid]
        for d in invalidDependencies:
            logging.warning("Invalid dependency \"" + str(d) + "\" was created, meaning the referenced file does not exist:")
        # Only keep the valid dependencies
        self.dependencies = [x for x in self.dependencies if not x.invalid]

    def getImplicitDependencies(self):
        for f in self.files:
            if f.fileType in config.fileTypesToCheckImplicitDependencies:
                self.update(f)

    def getExplicitDependencies(self):
        filename = self.mrv.workPath + "/" + config.projectSubfolder + config.explicitDependenciesFilename
        if not os.path.exists(filename):
            return []
        f = open(filename, "r")
        lines = f.readlines()
        lines = [l.replace("\n", "") for l in lines]
        f.close()
        dependencies = self.readExplicitDependencies(lines)
        for dep in dependencies:
            if type(dep.starts[0]) == FileState:
                fileStateOfStartFile = dep.starts[0]
            else:
                fileStateOfStartFile = self.mrv.findFileState(self.mrv.workPath + "/" + dep.starts[0])
            dep.initialize(self.mrv, fileStateOfStartFile, pathIsRelativeToProject=True,explicit=True)
            self.addDependency(dep)
        return dependencies
    
    def readExplicitDependencies(self, lines):
        # Format of lines : [start1, start2, ...] -> [target1, target2, ...] -> command 
        dependencies = []
        for l in lines:
            sp = l.split(config.explicitFileSeparator)
            if len(sp) > 1:
                starts = sp[0]
                targets = sp[1]
                if "," in starts:
                    starts = starts.split(",")
                else:
                    starts = [starts]
                if "," in targets:
                    targets = targets.split(",")
                else:
                    targets = [targets]
            command = sp[2].strip() if len(sp) == 3 else None
            starts = [tools.cleanFilename(x) for x in starts]
            targets = [tools.cleanFilename(x) for x in targets]
            starts = self.findMatches(starts)
            targets = self.findMatches(targets)
            if starts == [] or targets == []:
                continue
            dependencies.append(Dependency(starts = starts, targets = targets, command = command, printOutput = True))
        return dependencies

    def findMatches(self, expressions):
        return [f2 for f1 in expressions for f2 in self.files if self.isMatch(f1, f2.fname)]

    def isMatch(self, regex, filename):
        localName = filename.replace(self.mrv.workPath + "/", "")
        match = re.match(regex, localName)
        return match is not None

    def addDependency(self, d):
        self.dependencies.append(d)
        for startFile in d.starts:
            startFile.successors.append(d)

    def removeDependency(self, d):
        self.dependencies.remove(d)
        for startFile in d.starts:
            startFile.successors.remove(d)

    def update(self, fileState):
        # This file has either changed or this is the initial check. Run all modules on it to see if a new dependency has to be created
        newDependencies = []
        if fileState.fileType in config.fileTypesToCheckImplicitDependencies:
            lines = fileState.readlines()
            for m in self.modules:
                newDependencies = newDependencies + tools.ensureList(self.getDependencies(m, fileState, lines))
        # Whatever dependencies we found: These are now correct. Delete all the old ones that originally came from this file, add the new ones. However, don't touch explicit dependencies, since they have to live during the whole runtime.
        deprecatedDependencies = [d for d in self.dependencies if d.originFile == fileState]
        for d in deprecatedDependencies:
            if not d.explicit:
                self.removeDependency(d)
        for d in newDependencies:
            d.initialize(self.mrv, fileState)
            if d not in self.dependencies:
                self.addDependency(d)

    def getDependencies(self, module, fileState, lines):
        # Module.check returns a list of entries of the form (starts, targets, function)
        if lines == None:
            logging.error("Error while running the module " + str(module)  + " on " + str(fileState) + " - File doesn't exist")
            return
        return module.check(fileState, lines)

    def loadModules(self, path):
        modules = []
        for f in os.listdir(path):
            if fileUtils.getFileType(f) == "py":
                if os.path.isfile(path + "/" + f):
                    modules.append(self.loadModule(path + f))
        return modules

    def loadModule(self, fname):
        logging.debug("Loading module" + str(fname))
        loader = importlib.machinery.SourceFileLoader(os.path.split(fname)[1], fname)
        module = loader.load_module()
        return module


