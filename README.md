### MakeRunView

A tool to automatize compiling/execution. The ultimate goal of makeRunView is to allow the user to work on a project (a LaTeX document, a simple script or even a large program) without having to execute any of the necessary commands (pdflatex foo.tex, python bar.py, ...) everytime something in the code changes.

MakeRunView observes all files in the project folder. If a file gets written by the user, all the commands that lead to the final product (a pdf file that can be viewed or the output of a program) will be run. 
Determining what these commands are and how they produce subsequent files is the main job of makeRunView. In order to be adaptive enough, it loads a set of (project specific) modules that determine these commands.

## Modules

Each module should fulfill one specific job. That is, it should take the content of a file as input and then read it to determine if other files are referenced. For example, a latex picture module checks each line of a .tex file for a line like "\includegraphics{pics/test.png}" and remembers that the .tex file needs the test.png file.
Each module is a python file stored in either the makeRunView modules subfolder or a .makeRunView folder in the project we're working on. The makeRunView modules try to be as general as possible, however some very project specific things just can't be recognized in general. In this case the user can simply write modules for just this project.

## Project Examples
#Example 1

A (very) small project contains a gnuplot command file test.gpi which contains the lines

```
set terminal pngcairo
set output "./test.png"
plot sin(x)
```

Here, makeRunView would read the line which contains "set output ..." and therefore create the dependency:
["test.gpi"] -> ["test.png"] gnuplot
meaning that the test.png file depends on test.gpi. In this case it would watch over test.gpi and, whenever the file is written on the filesystem would execute 
```
gnuplot test.gpi
```
to satisfy the dependency.

#Example 2
Suppose we have our test.gpi file again, however this time outputting to two different files
```
set terminal epslatex
set output "./test1.png"
plot sin(x)
set output "./test2.png"
plot sin(x)
```
Here, makeRunView would create the dependency 
["test.gpi"] -> ["test1.png", "test2.png"] gnuplot
The nice thing is that the command gnuplot only needs to be executed once to create both output files and makeRunView (or rather the module which creates these dependencies) recognizes that.

#Example 3
Let's add another file to the previous project: test.tex, which contains the lines
```
...
\begin{figure}
    \includegraphics{test1.png}
\end{figure}
...
```
In this case, the includegraphics line would trigger one of the makeRunView-modules to create the dependency
["test1.png"] -> ["main.tex"] pdflatex -interaction=nonstopmode
Since the files from earlier are also present in the project, the dependency
["test.gpi"] -> ["test1.png", "test2.png"] gnuplot
exists as well. This means that if we change test.gpi makeRunView will automatically execute
gnuplot test.gpi
pdflatex -interaction=nonstopmode test.tex
to create the file test.pdf which we can simply view to see the result of our plot script in our final document immediately.
