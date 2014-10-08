import os, config
import modules.gpimodule

class Dependencies:
    """Checks dependencies between files by calling modules. Modules are loaded from a global module folder
    whose path is defined by config.py as well as the modules subfolder of the project path if it exists. The
    name of this subfolder is defined by config.py.
    Each module must define a check function which takes the read lines of a file as an argument
    and returns [[starts], [targets], function]"""
    def __init__(self, workPath):
        self.modules = self.loadModules(workPath)
        self.modules = self.modules + self.loadModules(config.globalPath)
        # TEST
        self.modules = [modules.gpimodule]

    def update(self, fileState):
        lines = fileState.readlines()
        # read the files, run all modules to check for dependencies
        # add them to a list and do this down the tree. OWNED
        for m in self.modules:
            dependencies = m.check(fileState, lines)

    def loadModules(self, path):
        modules = []
        for f in os.listdir(path):
            if os.path.isfile(path + "/" + f):
                modules.append(self.loadModule(path + "/" + f))
        return modules

    def loadModule(self, fname):
        return fname


