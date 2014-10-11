import tools, config, os, logging

class FileState:
    def __init__(self, fname):
        self.fname = fname
        assert(self.fname[0] == "/") # All paths should be absolute.
        self.successors = []
        self.fileType = tools.getFileType(fname)
        # self.fileName = tools.getFileName(fname)
        self.fileName = fname

    def readlines(self):
        # First check if this file actually exists, which might not be the case
        if not os.path.isfile(self.fname):
            return None
        try:
            f = open(self.fname, "r")
            lines = f.readlines()
            f.close()
            return lines
        except UnicodeDecodeError as e:
            # logging.warning("Trying to read " + self.fname + " when the following error appeared")
            # logging.warning(e)
            pass
        return ""

    def shouldBeObserved(self):
        return self.fileType in config.fileTypesToWatch

    def __str__(self):
        return "<" + self.fileName + ">"
