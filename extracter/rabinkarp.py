import os
import subprocess
from optparse import OptionParser

class SmaliCpder:

    Q = 162259276829213363391578010288127
    # Q = 1363005552434666078217421284621279933627102780881053358473
    nextTokenValue = 1
    minimumTokens = 600 # todo init
    smalifiles = []
    cpdhashs = {} # <hash, (file, start, end)s>

    def accessfile(self, path:str):
        if os.path.isfile(path):
            if path.endswith(".smali"):
                self.smalifiles.append(path)
            return None
        
        if os.path.isdir(path):
            subfiles = os.listdir(path)
            for subfile in subfiles:
                self.accessfile(os.path.join(path, subfile)) # os.path.join

    def prepare(self):
        """
        token解析和token映射值预处理
        """
        for file in set(self.smalifiles):
            tokens = self.smali2tokens(file)
            print("smali2tokens " + file)
            self.token2value(tokens)
        # print("in the prepare " + str(len(self.tokenValueMap)) + " " + str(self.tvalue))

    def handle(self):
        for file in set(self.smalifiles):
            tokens = self.smali2tokens(file)
            print("token2hash " + file)
            hashmap = self.token2hash(tokens) #  Map<hash, (start, end)s>
            cpdhashs = self.cpdhashs
            for hash in hashmap.keys():
                if hash not in cpdhashs: cpdhashs[hash] = []
                pairs = hashmap[hash]
                for pair in pairs:
                    start, end = pair
                    cpdhashs[hash].append((file, start, end))


    def token2hash(self, tokens:list):
        """
        rk
        """
        hashmap = {}
        n = len(tokens)
        m = self.minimumTokens   # patten length
        if(n < m): return hashmap
        R = self.nextTokenValue
        Q = self.Q
        RM = self.rm(m-1, R, Q)

        hash = 0
        for i in range(m):
            hash = (hash * R + self.tokenValue(tokens[i])) % Q
        
        if hash not in hashmap: hashmap[hash] = []
        hashmap[hash].append((0, m)) # [0, m) tokens[0:m]

        for i in range(n-m):
            # leading digit
            leading = self.tokenValue(tokens[i])
            # remove leading digit
            hash = (hash - leading * RM % Q + Q) % Q

            # trailing digit
            trailing = self.tokenValue(tokens[m+i])
            # add trailing digit
            hash = (hash*R + trailing) % Q

            if hash not in hashmap: hashmap[hash] = []
            hashmap[hash].append((i+1, m+i+1))
        return hashmap

    def rm(self, m, R, Q):
        _rm = 1
        for i in range(m):
            _rm = (_rm * R) % Q
        return _rm


    tokenValueMap = {} # <str,int>, <token,value>
    def token2value(self, tokens:list):
        tokenValueMap = self.tokenValueMap
        for token in tokens:
            if(token not in tokenValueMap):
                tokenValueMap[token] = self.nextTokenValue
                self.nextTokenValue = self.nextTokenValue + 1

    def tokenValue(self, token):
        assert token in self.tokenValueMap
        return self.tokenValueMap[token]


    ########## smali to tokens ###########
    smaliCache = {}

    def smali2tokens(self, file:str):
        if(file in self.smaliCache):
            return self.smaliCache[file]
        else:
            tokens = self._smali2tokens(file)
            self.smaliCache[file] = tokens # <file,tokens>
            return tokens
    
    def _smali2tokens(self, file:str):
        """
        request: smali
        usage: smali tokens [<options>] [<file>|<dir>]+ , Assembles the given files. 
            If a directory is specified, it will be recursively searched for any files with a .smali prefix
        output: list<token> <class list<str>>
        """
        # check file
        cmd=["smali", "tokens", file]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').split("\n")
            
if __name__ == "__main__":
    parser = OptionParser(usage="Usage: smalicpd.py [options] files/paths")

    parser.add_option("-t", "--minimum-tokens", dest="minimumTokens", default=50,
        help="the tokens nums for cpb", type="int")

    (options, args) = parser.parse_args()
    print(options)
    print(args)

    cpder = SmaliCpder();
    for file in args: cpder.accessfile(os.path.realpath(file))
    print("accessfile end with " + str(len(cpder.smalifiles)) + " smali file")
    cpder.prepare()
    cpder.handle()

    for k in cpder.cpdhashs:
        v = cpder.cpdhashs[k]
        if len(v) > 1:
            print(v)