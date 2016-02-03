#TODO RENAME TESTS, add logging in gnuplot scripts again maybe
from nose.tools import eq_ as eq
from modules import gnuplotLoad
from modules import gnuplotOutput
from modules import pyImport
from modules import texIncludeGraphics
from modules import texInput
from modules import texMainFile
from modules import texSubImport
from modules import javaImport
from modules import javaAnt
from makeRunView import filestate
import mock
from mock import Mock
# from makeRunView import makerunview

class TestMakeRunViewModules():
    def setUp(self):
        pass
        # self.patcher = mock.patch('makeRunView.makerunview.os')
        # self.mockOs = self.patcher.start()
        # self.mrv = makerunview.MakeRunView(".")
        # Default project setup : Just a folder with one subfolder and one file.
        # Everything called folder is a folder, everything called file is a file
        # isdir = lambda x : True if "folder" in x else False
        # self.mockOs.path.isdir = Mock(side_effect = isdir)
        # self.mockOs.path.join = Mock(side_effect = lambda x, y : x)

    def testGnuplotLoad(self):
        f = Mock(fileType = "gpi")
        # Check with double quotes
        lines = ["load \"template.gpi\""]
        res = gnuplotLoad.check(f, lines)
        assert(res != None and len(res.starts) == 1 and res.starts[0] == "template.gpi")
        # Check with single quotes
        lines = ["load 'template.gpi'"]
        res = gnuplotLoad.check(f, lines)
        # Test with a dynamic string for loading which should produce no dependency
        assert(res != None and len(res.starts) == 1 and res.starts[0] == "template.gpi")
        lines = ["set terminal wxt",
            "load 'template'.x.'.gpi'", 
            "plot f(x)"]
        res = gnuplotLoad.check(f, lines)
        assert(res == None)

    def testGnuplotOutput(self):
        f = Mock(fileType = "gpi")
        # Check with double quotes
        lines = ["set terminal wxt",
            "set output \"test.tex\"",
            "plot f(x)"]
        res = gnuplotOutput.check(f, lines)
        assert(res != None and len(res.targets) == 1 and res.targets[0] == "test.tex")
        # Check with single quotes
        lines = ["set output 'test.tex'"]
        res = gnuplotOutput.check(f, lines)
        assert(res != None and len(res.targets) == 1 and res.targets[0] == "test.tex")
        # Dynamic output string -> No dependency
        lines = ["set output 'test'.x.'.tex'"]
        res = gnuplotOutput.check(f, lines)
        assert(res == None)
        # No output string -> No dependency
        lines = ["set terminal wxt", "plot f(x)"]
        res = gnuplotOutput.check(f, lines)
        assert(res == None)

    def testPyImport(self):
        f = Mock(fileType = "py")
        lines = ["import test"]
        res = pyImport.check(f, lines)
        assert(res != None and len(res.starts) == 1 and res.starts[0] == "test.py")
        lines = ["import test1, test2"]
        res = pyImport.check(f, lines)
        assert(res != None and len(res.starts) == 2 and res.starts[0] == "test1.py" and res.starts[1] == "test2.py")

    def testTexIncludeGraphics(self):
        f = Mock(fileType = "tex")
        lines = ["% GNUPLOT: LaTeX picture with Postscript", "\\begingroup", "\\makeatletter"]
        assert(texIncludeGraphics.check(f, lines) == None)
        lines = ["\\includegraphics{pics/test}"]
        texIncludeGraphics.os.path.isfile = Mock(side_effect = lambda x : False)
        res = texIncludeGraphics.check(f, lines) 
        assert(res == None)
        lines = ["\\includegraphics{pics/test}"]
        texIncludeGraphics.os.path.isfile = Mock(side_effect = lambda x : (x == "pics/test.png"))
        res = texIncludeGraphics.check(f, lines) 
        assert(res.starts[0] == "pics/test.png")

    def testTexInput(self):
        f = Mock(fileType = "tex")
        lines = ["% GNUPLOT: LaTeX picture with Postscript", "\\begingroup", "\\makeatletter"]
        assert(texInput.check(f, lines) == None)
        lines = ["\\input{test}"]
        # texInput.os.path.isfile = Mock(side_effect = lambda x : False)
        res = texInput.check(f, lines) 
        assert(res.starts[0] == "test.tex")

    def testTexMainFile(self):
        f = Mock(fileType = "tex", fname = "test.tex")
        lines = ["% GNUPLOT: LaTeX picture with Postscript", "\\begingroup", "\\makeatletter"]
        assert(texMainFile.check(f, lines) == None)
        lines = ["\\begin{document}"]
        res = texMainFile.check(f, lines) 
        assert(res.targets == "test.pdf")

    def testTexSubImport(self):
        f = Mock(fileType = "tex", fname = "test.tex")
        lines = ["\\subimport{pics/}{test}"]
        res = texSubImport.check(f, lines) 
        assert(res.starts[0] == "pics/test.tex")

    def testIgnoreIncorrectFiletypes(self): 
        modulesAndIncorrectFiletypes = [
            [gnuplotLoad, "pdf"],
            [gnuplotOutput, "pdf"],
            [gnuplotOutput, "pdf"],
            [pyImport, "pdf"],
            [texIncludeGraphics, "pdf"],
            [texInput, "pdf"],
            [texMainFile, "pdf"],
            [texSubImport, "pdf"]
        ]
        for module, incorrectFileType in modulesAndIncorrectFiletypes:
            yield self._testIgnoreIncorrectFileType, module, incorrectFileType

    def _testIgnoreIncorrectFileType(self, module, incorrectFileType):
        f = Mock(fileType = "pdf")
        lines = []
        assert(module.check(f, lines) == None)

    def testIgnoresGnuplotFiles(self): 
        modules = [texIncludeGraphics, texInput, texMainFile, texSubImport]
        for module in modules:
            yield self._testIgnoresGnuplotFiles, module

    def _testIgnoresGnuplotFiles(self, module):
        f = Mock(fileType = "tex")
        lines = ["% GNUPLOT: LaTeX picture with Postscript", "\\begingroup", "\\makeatletter"]
        assert(module.check(f, lines) == None)

    def testJavaImport(self):
        f = Mock(fileType = "java")
        lines = ["package a.b;\n", 
                 "import a.b.c;\n"]
        res = javaImport.check(f, lines)
        assert(res != None and len(res.starts) == 1 and res.starts[0] == "../../a/b/c.java")
        f = Mock(fileType = "java")
        lines = ["package a.b;\n", 
                 "import a.b.c;\n",
                 "import a.d.e;\n"]
        res = javaImport.check(f, lines)
        assert(res != None and len(res.starts) == 2 and res.starts[0] == "../../a/b/c.java" and res.starts[1] == "../../a/d/e.java")

    def testJavaAnt(self):
        f = Mock(fileType = "xml")
        lines = """
        <target name="compile">
            <mkdir dir="build/classes"/>
            <my.javac srcdir="src" destdir="build/classes"/>
        </target>
        <target name="jar">
            <mkdir dir="build/jar"/>
            <jar destfile="build/jar/Main.jar" basedir="build/classes">
                <manifest>
                    <attribute name="Main-Class" value="main.Main"/>
                </manifest>
            </jar>
        </target>"""
        lines = lines.split("\n")
        res = javaAnt.check(f, lines)
        assert(res != None and len(res.starts) == 1 and res.starts[0] == "src/main/Main.java")

