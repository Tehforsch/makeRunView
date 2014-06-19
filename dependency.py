import executor

class Dependency:
    def __init__(self, start, targets, cleaningFunction=None):
        self.start = start
        self.targets = targets
        if cleaningFunction is None:
            self.cleaningFunction = self.findFileTypeFunction()
        else:
            self.cleaningFunction = cleaningFunction
        self.start = start

    def findFileTypeFunction(self):
        if self.start.fileType == ".gpi": # Gnuplot
            return executor.gnuplot
        if self.start.fileType == ".py": # Python script
            return executor.python
        if self.start.fileType == ".tex": # Latex
            return executor.latex

    def clean(self, workPath):
        if self.cleaningFunction is None:
            return None
        return self.cleaningFunction(workPath, self.start, self.targets)
