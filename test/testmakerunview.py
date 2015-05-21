from makeRunView import makerunview
import mock
from mock import Mock

class TestMakeRunViewFileSystemInteractions():
    def setUp(self):
        self.patcher = mock.patch('makeRunView.makerunview.os')
        self.mockOs = self.patcher.start()
        self.mrv = makerunview.MakeRunView(".")
        # Default project setup : Just a folder with one subfolder and one file.
        # Everything called folder is a folder, everything called file is a file
        listdir = lambda x : ["subfolder", "file1"] if x == "." else []
        isdir = lambda x : True if "folder" in x else False
        self.mockOs.listdir = Mock(side_effect = listdir)
        self.mockOs.path.isdir = Mock(side_effect = isdir)
        self.mockOs.path.join = Mock(side_effect = lambda x, y : x)

    def testScanForFilesFindsFiles(self):
        self.mrv.addFileState = Mock()
        self.mrv.scanForFiles(".")
        self.mrv.addFileState.assert_any_call(".")
    
    @mock.patch('makeRunView.filestate.FileState')
    def testTreeCleanedIfFileChanged(self, fileState):
        # need to mock FileState creation since it gets called with a path which doesnt have "/" at the beginning, which induces errors
        self.mrv.cleanTree = Mock(name="cleantree")
        f1 = Mock(name="filestate")
        f1.fname = "file1"
        self.mrv.files = [f1]
        self.mrv.notifyChanged("file1")
        self.mrv.handle()
        self.mrv.cleanTree.assert_called_once_with(f1)

    def testDependencyCommandExecutedByCleanTree(self):
        f1 = Mock(name="f1")
        f2 = Mock(name="f2")
        f1.fname = "file1"
        f2.fname = "file2"
        mockDependency = mock.Mock(name="dependency")
        mockDependency.clean = mock.Mock(return_value = None)
        mockDependency.targets = [f2]
        f1.successors = [mockDependency]
        f2.successors = []
        self.mrv.files = [f1, f2]
        self.mrv.cleanTree(f1)
        mockDependency.clean.assert_called_once_with(".")

    def tearDown(self):
        self.mrv.kill()
