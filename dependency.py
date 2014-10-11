import executor

class Dependency:
    """The biggest set of connected files that can be cleaned by executing one function."""
    def __init__(self, starts, targets, cleaningFunction, outputWanted):
        self.starts = starts
        self.targets = targets
        self.cleaningFunction = cleaningFunction
        self.outputWanted = outputWanted

    def clean(self, workPath):
        if self.cleaningFunction is None:
            return None
        if type(self.cleaningFunction) == str:
            return ""
        else:
            return self.cleaningFunction(workPath, self.starts, self.targets)

    def __str__(self):
        return self.cleaningFunction + ": [" + ", ".join(map(str, self.starts)) + "] -> [" + ", ".join(map(str, self.targets)) + "]"
