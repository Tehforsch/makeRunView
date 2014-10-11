import tools
def check(f, lines):
    dependencies = []
    start = f.fname
    targets = []
    for l in lines:
        if "set output" in l:
            targets.append(tools.charactersBetween(l, "\"", "\""))
    return [[[start], targets, "gnuplot", True]]
