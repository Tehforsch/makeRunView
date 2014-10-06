import executor

class Dependency:
    """The biggest set of connected files that can be cleaned by executing one function."""
    def __init__(self, starts, targets, cleaningFunction=None):
        self.starts = starts
        self.targets = targets
        self.cleaningFunction = cleaningFunction

    def clean(self, workPath):
        if self.cleaningFunction is None:
            return None
        return self.cleaningFunction(workPath, self.start, self.targets)
