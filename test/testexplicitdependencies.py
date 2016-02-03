#TODO RENAME TESTS, add logging in gnuplot scripts again maybe
from nose.tools import eq_ as eq
from makeRunView.dependencymanager import DependencyManager
import mock
from mock import Mock, MagicMock

class TestExplicitDependencies():
    def setUp(self):
        pass

    def testSimpleExplicitDependency(self):
        lines = ["a.tex -> b.tex -> pdflatex %t"]
        depMan = MagicMock()
        depMan.findMatches = lambda x : x
        res = DependencyManager.readExplicitDependencies(depMan, lines)
        assert(res != None)
        assert(res[0].starts == ["a.tex"])
        assert(res[0].targets == ["b.tex"])
        assert(res[0].command == "pdflatex %t")
        
    def testRegexCheck(self):
        depMan = MagicMock(mrv = Mock(workPath="--"))
        depMan.files = [Mock(fname = "bar/foo.py"), Mock(fname="bar/bar.py")]
        depMan.isMatch = lambda x,y : DependencyManager.isMatch(depMan, x,y)
        res = DependencyManager.findMatches(depMan, ["bar/.*.py"])
        assert(res != None)
        assert(res[0].fname == "bar/foo.py")
        assert(res[1].fname == "bar/bar.py")
