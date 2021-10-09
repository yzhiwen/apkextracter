import os
from .factory import ClazzMethodFactory
from .smaliopcodefactory import OpcodeFactory

class SmalierWalker:

    def __init__(self, packageref = "") -> None:
        self.packageref = packageref

    def startup(self, path):
        smalifiles = self.walkFileTree(path)
        for smalifile in smalifiles:
            methods = self.methods(smalifile)
            for label, tokens in methods.items():
                ClazzMethodFactory.clazzMethod(smalifile, label, tokens)
    
    def methods(self, smalifile):
        """
        input: smali file
        output: <methodlabel:str, tokens:list<str>>
        """
        methods = {}
        with open(smalifile) as file:
            for line in file:
                if len(self.packageref) > 0 and line.startswith(".class"):
                    if self.packageref not in line:
                        return {}

                if line.startswith(".method"):
                    if self.methodfilter(line):
                        while not line.startswith(".end method"):
                            line = file.readline().strip()

                    label = line.lstrip(".method ").strip()
                    tokens = []
                    while not line.startswith(".end method"):
                        line = file.readline().strip()
                        if line.startswith(".end method"): break
                        if self.opcodefilter(line): continue

                        linetokens = OpcodeFactory.tokens(line)
                        if linetokens is None: continue
                        tokens.extend(linetokens)
                    if len(label) > 0 and len(tokens) > 0:
                        methods[label] = tokens
                pass
            pass
        return methods

    def methodfilter(self, line):
        if line is None: return True
        if len(line) <= 1: return True
        if line.startswith(".method"):
            if " native " in line: return True # native方法
            if " abstract " in line: return True # abstract方法，包含接口方法
            if " constructor " in line: return True # tmp
        return False

    def opcodefilter(self, line):
        if line is None: return True
        if len(line) <= 1: return True
        if line.startswith(".line"): return True
        if line.startswith(".locals"): return True
        if line.startswith(".prologue"): return True
        return False

    def walkFileTree(self, path):
        list = []
        if os.path.isfile(path):
            if path.endswith(".smali"):
                list.append(path)
        elif os.path.isdir(path):
            subfiles = os.listdir(path)
            for subfile in subfiles:
                subSmaliList = self.walkFileTree(os.path.join(path, subfile))
                list.extend(subSmaliList)
        return list