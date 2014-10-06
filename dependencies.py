class Dependencies:
    def __init__(self, files):
        self.files = files

    def update(self, fileState):
        print(fileState)
        # read the files, run all modules to check for dependencies
        # add them to a list and do this down the tree. OWNED
