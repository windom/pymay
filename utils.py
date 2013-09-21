class PrettyPrinter:
    def __init__(self):
        self.tabs = []
        self.col = 0
        self.content = []

    def __iadd__(self, s):
        if hasattr(s, "prettyPrint"):
            s.prettyPrint(self)
        else:
            self.content.append(s)
            self.col += len(s)
        return self

    def join(self, lst, delimiter=" "):
        if lst:
            self += lst[0]
        for s in lst[1:]:
            self += delimiter
            self += s

    def newLine(self):
        self.content.append("\n")
        self.col = 0
        self += self.tabs[-1]
        return self

    def addTab(self):
        self.tabs.append(' ' * self.col)
        return self

    def delTab(self):
        self.tabs.pop()
        return self

    def __str__(self):
        return "".join(self.content)
