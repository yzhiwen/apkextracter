import os
from .factory import ClazzMethodFactory

class SmalierWalker:

    def startup(self, path):
        smalifiles = self.walkFileTree(path)
        for smalifile in smalifiles:
            methodstrlist = self.smaliMethods(smalifile)
            for methodstr in methodstrlist:
                ClazzMethodFactory.clazzMethod(smalifile, methodstr)

    def smaliMethods(self, filepath):
        """
        input: smali file
        ouput: list<methodstr>
        """
        methods = []
        method = ""
        with open(filepath) as file:
            for line in file:
                line = line.strip() + " "
                if(self.linefilter(line)):  continue
                if line.startswith(".method"):
                    method = line.lstrip(".method ")
                elif line.startswith(".end method"):
                    if len(method) == 0: continue # maybe skip .method public abstract
                    methods.append(method)
                    method = ""
                elif len(method) > 0:
                    method += line
        return methods

    def linefilter(self, line):
        if line is None: return True
        if len(line) <= 1: return True
        if line.startswith(".method"):
            if " native " in line: return True # native方法
            if " abstract " in line: return True # abstract方法，包含接口方法
            if " constructor " in line: return True # tmp
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