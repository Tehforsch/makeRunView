import os, config
from dependency import Dependency
import tools

import modules.gpimodule

class DependencyManager:
    """Checks dependencies between files by calling modules. Modules are loaded from a global module folder
    whose path is defined by config.py as well as the modules subfolder of the project path if it exists. The
    name of this subfolder is defined by config.py.
    Each module must define a check function which takes the read lines of a file as an argument
    and returns [[starts], [targets], function]"""

    def __init__(self, mrv, workPath):
        self.mrv = mrv
        self.files = self.mrv.files
        self.modules = self.loadModules(workPath)
        self.modules = self.modules + self.loadModules(config.globalPath)
        # TEST
        self.modules = [modules.gpimodule]
        self.initialCheck()

    def initialCheck(self):
        self.dependencies = []
        for f in self.files:
            if f.fileType in config.fileTypesToCheckImplicitDependencies:
                lines = f.readlines()
                for m in self.modules:
                    newDependencies = self.getDependencies(m, f, lines)
                    if newDependencies is not None:
                        self.dependencies = self.dependencies + newDependencies
        for d in self.dependencies:
            for startFile in d.starts:
                startFile.successors.append(d)

    def update(self, fileState):
        if fileState.fileType in config.fileTypesToCheckImplicitDependencies:
            lines = fileState.readlines()
            for m in self.modules:
                dependencies = self.getDependencies(m, fileState, lines)

    def getDependencies(self, module, fileState, lines):
        # Module.check returns a list of entries of the form (starts, targets, function)
        rawList = module.check(fileState, lines)
        dependencies = []
        # Safety measures
        i = 0
        while i < len(rawList):
            if len(rawList[i][0]) == 0 or len(rawList[i][1]) == 0:
                del rawList[i]
            else:
                i += 1
        path = tools.getFilePath(fileState.fileName)
        for d in rawList:
            d[0] = self.convertLocalFileNamesToStates(d[0], path)
            d[1] = self.convertLocalFileNamesToStates(d[1], path)
            dependencies.append(Dependency(d[0], d[1], d[2], d[3]))
        return dependencies

    def convertLocalFileNamesToStates(self, fileNames, path):
        fileNames = map(lambda filename : tools.ensureAbsPath(filename, path), fileNames)
        return list(map(lambda name : self.mrv.findFileState(name), fileNames))

    def loadModules(self, path):
        modules = []
        for f in os.listdir(path):
            if os.path.isfile(path + "/" + f):
                modules.append(self.loadModule(path + "/" + f))
        return modules

    def loadModule(self, fname):
        return fname


