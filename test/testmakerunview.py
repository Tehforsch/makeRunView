from makeRunView import makerunview
import mock
from mock import Mock

# class Graph:
#     def __init__(self):
#         self.topNode = Node()

#     def collect(self, node = None):
#         if node == None:
#             node = self.topNode
#         nodes = set([node])
#         for n in node.successors:
#             nodes = nodes.union(self.collect(n))
#         return nodes

#     def collectEdges(self, node = None):
#         if node == None:
#             node = self.topNode
#         edges = [(node, n) for n in node.successors]
#         for n in node.successors:
#             edges = edges + self.collectEdges(n)
#         return edges
        
#     def convertToDependencies(self):
#         nodes = list(self.collect())
#         for (i, n) in enumerate(nodes):
#             n.name = str(i)
#         files = [Mock(fname = "f" + str(i)) for (i, f) in enumerate(nodes)]
#         edges = self.collectEdges()
#         dependencies = []
#         for e in edges:
#             dependencies.append((files[nodes.index(e[0])], files[nodes.index(e[1])]))
#         self.printEdges()
#         return files, dependencies

#     def printEdges(self):
#         print("\n".join(str(x[0]) + " -> " + str(x[1]) for x in self.collectEdges()))
        
# class Node:
#     def __init__(self):
#         self.successors = []
#         self.name = ""

#     def addSuccessor(self, n):
#         self.successors.append(n)
        
#     def __str__(self):
#         return "N" + self.name


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

    def testDependencyChainCleaned(self):
        # If this exceeds 1000 the test will actually fail because of the recursion depth limit :)
        N = 200
        files = [Mock(name = "f" + str(i)) for i in range(N)]
        for (i,f) in enumerate(files):
            f.fname = "file" + str(i)
        dependencies = [mock.Mock(name="dependency" + str(i)) for i in range(N-1)]
        for (i,d) in enumerate(dependencies):
            d.clean = mock.Mock(return_value = None)
            d.targets = [files[i+1]]
            files[i].successors = [d]
            files[i+1].successors = []
            self.mrv.files = files
        self.mrv.cleanTree(files[0])
        for (i,d) in enumerate(dependencies):
            d.clean.assert_called_once_with(".")

    @mock.patch('makeRunView.filestate.FileState')
    def testDependenciesAddedWhenFileCreated(self, fileState):
        self.mrv.cleanTree = Mock(name="cleantree")
        self.mrv.dependencyManager = Mock(name="dependencyManager")
        f1 = Mock(name="filestate")
        f1.fname = "file1"
        self.mrv.files = [f1]
        self.mrv.notifyChanged("file2")
        assert(len(self.mrv.files) == 2)
        f2 = self.mrv.files[1]
        self.mrv.handle()
        self.mrv.cleanTree.assert_called_once_with(f2)
        self.mrv.dependencyManager.update.assert_called_once_with(f2)

    # def testDependencyGraph(self):
    #     g = Graph()
    #     g.topNode.addSuccessor(Node())
    #     g.topNode.addSuccessor(Node())
    #     g.topNode.successors[0].addSuccessor(Node())
    #     files, dependencies = g.convertToDependencies()

    def tearDown(self):
        self.mrv.kill()
