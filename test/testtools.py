from makeRunView import tools

def testIsCommentWorksWithWhitespace():
    assert(tools.isComment("    \t # plot sin(x)", "#"))

def testCharactersBetweenOnTheSameCharacterTwice():
    assert(tools.charactersBetween("-randomstring-", "-", "-") == "randomstring")

def testCharactersBetweenStartIndex():
    s = "----A-randomstring-"
    assert(tools.charactersBetween(s, "-", "-", s.index("A")) == "randomstring")

def testCharactersBetweenAppearancesOfEndStringBeforeStartString():
    assert(tools.charactersBetween("YYYYYYXrandomstringY", "X", "Y") == "randomstring")

def testCharactersBetweenReturnsNoneIfStartStringNotFound():
    assert(tools.charactersBetween("abcdefY", "X", "Y") == None)

def testCharactersBetweenReturnsNoneIfEndStringNotFound():
    assert(tools.charactersBetween("Xabcdef", "X", "Y") == None)

def testEnsureListWithNone():
    assert(tools.ensureList(None) == [])

def testEnsureListWithList():
    assert(tools.ensureList([1,2,3]) == [1,2,3])

def testEnsureListWithString():
    assert(tools.ensureList("test") == ["test"])
