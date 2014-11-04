import os, config, logging, tools
from dependency import Dependency
import importlib.machinery

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
        if os.path.isdir(workPath + config.moduleFolderName):
            self.modules = self.modules + self.loadModules(workPath + config.moduleFolderName + "/")
        # TEST
        # self.modules = [modules.gpimodule, modules.texmodule]
        self.initialCheck()

    def initialCheck(self):
        self.dependencies = []
        for f in self.files:
            if f.fileType in config.fileTypesToCheckImplicitDependencies:
                lines = f.readlines()
                for m in self.modules:
                    newDependencies = self.getDependencies(m, f, lines)
                    if newDependencies is not None:
                        if type(newDependencies) != list:
                            newDependencies = [newDependencies]
                        for dep in newDependencies:
                            dep.initialize(self.mrv, f)
                        self.dependencies = self.dependencies + newDependencies
        invalidDependencies = list(filter(lambda x : x.invalid, self.dependencies))
        if len(invalidDependencies) != 0:
            logging.warning("Invalid dependencies were created: \n" + "\n".join(map(str, invalidDependencies)))
            logging.warning("This can happen (input commands in preamble for example)")
        self.dependencies = list(filter(lambda x : not x.invalid, self.dependencies))
        logging.debug("List of created dependencies: \n" + "\n".join(map(str,self.dependencies)))
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
        dependencies = module.check(fileState, lines)
        return dependencies

    def loadModules(self, path):
        modules = []
        for f in os.listdir(path):
            if os.path.isfile(path + "/" + f):
                modules.append(self.loadModule(path + f))
        return modules

    def loadModule(self, fname):
        logging.debug("Loading module" + str(fname))
        loader = importlib.machinery.SourceFileLoader(os.path.split(fname)[1], fname)
        foo = loader.load_module()
        return foo


