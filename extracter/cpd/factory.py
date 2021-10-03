from .model import Clazz
from .model import ClazzMethod
from .model import SnippetMethod

class ClazzFactory:
    CLAZZMAP = {}

    @staticmethod
    def clazz(file):
        if file in ClazzFactory.CLAZZMAP:
            return ClazzFactory.CLAZZMAP[file]
        else:
            clazz = Clazz(file)
            ClazzFactory.CLAZZMAP[file] = clazz
            return clazz
    
    @staticmethod
    def clazzCount(): 
        return len(ClazzFactory.CLAZZMAP)
    pass

class ClazzMethodFactory:
    CLAZZMETHODMAP = []

    @staticmethod
    def clazzMethod(file, label, tokens):
        clazz = ClazzFactory.clazz(file)
        clazzMethod = ClazzMethod(clazz, label, tokens)
        ClazzMethodFactory.onMethodCreated(clazzMethod)
        return clazzMethod
    
    @staticmethod
    def onMethodCreated(clazzMethod):
        ClazzMethodFactory.CLAZZMETHODMAP.append(clazzMethod)
        ClazzMethodTokenFactory.onMethodCreated(clazzMethod)

    @staticmethod
    def methodCount():
        return len(ClazzMethodFactory.CLAZZMETHODMAP)

    @staticmethod
    def printAllMethod():
        for method in ClazzMethodFactory.CLAZZMETHODMAP:
            print(method.methodstr + "\n")
    pass

class SnippetMethodFactory:
    SNIPPETMETHODMAP = []

    DATASET = {} # <method, <(start,len), snippetmethod>>

    """认为有hash冲突，不过概率相对较低，冲突了在输出可被辨识出来，<hash, <snippetstr, list>>中snippetstr耗时"""
    HASHDATASET = {} # <len, <hash, snippetlist>>

    @staticmethod
    def snippetMethod(method: ClazzMethod, start, len, hash):
        dataset = SnippetMethodFactory.DATASET
        if method not in dataset: dataset[method] = {}
        if (start, len) in dataset[method]: 
            return dataset[method][(start, len)]
        if hash is None: return None

        snippet = SnippetMethod(method, start, len, hash)
        dataset[method][(start, len)] = snippet
        SnippetMethodFactory.SNIPPETMETHODMAP.append(snippet)
        SnippetMethodFactory.onSinppetMethodCreated(snippet)
        return snippet
    
    @staticmethod
    def onSinppetMethodCreated(snippet):
        if snippet is None: return
        hashdataset = SnippetMethodFactory.HASHDATASET
        len = snippet.len
        hash = snippet.hash
        if len not in hashdataset: hashdataset[len] = {}
        if hash not in hashdataset[len]: hashdataset[len][hash] = []
        hashdataset[len][hash].append(snippet)
        pass

    @staticmethod
    def inflateAllSnippet():
        snippets = SnippetMethodFactory.SNIPPETMETHODMAP.copy()

        def snippetkey(snippet): return snippet.start
        snippets.sort(key=snippetkey)

        for snippet in snippets:
            if snippet.inflated: continue
            SnippetMethodFactory.inflate(snippet)
        pass

    @staticmethod
    def inflate(snippet):
        R = ClazzMethodTokenFactory.R()
        Q = ClazzMethodTokenFactory.Q()
        valueof = ClazzMethodTokenFactory.valueof
        inflatable = SnippetMethodFactory.inflatable
        nextSnippetMethod = SnippetMethodFactory.nextSnippetMethod

        hash = snippet.hash
        start = snippet.start
        method = snippet.method
        tokens = method.tokens

        count = 0
        cursor = snippet
        while(inflatable(cursor)):
            cursor.inflated = True
            cursor = nextSnippetMethod(cursor)
            if cursor is None: break
            index = start + snippet.len + count
            trailing = valueof(tokens[index])
            hash = (hash * R + trailing) % Q
            count += 1

        len = snippet.len + count
        return SnippetMethodFactory.snippetMethod(method, start, len, hash)

    @staticmethod
    def inflatable(snippet):
        """snippet(start, len) and snippet(start+1,len) and snippet(start-1, len)"""
        if snippet is None: return False
        nextsnippet = SnippetMethodFactory.nextSnippetMethod(snippet)
        prevsnippet = SnippetMethodFactory.prevSnippetMethod(snippet)
        if nextsnippet is None and prevsnippet is None: return False

        hashdataset = SnippetMethodFactory.HASHDATASET
        if snippet.len not in hashdataset: return False

        snippetlist = hashdataset[snippet.len][snippet.hash]
        prevsnippetlist = []
        nextsnippetlist = []
        if prevsnippet is not None: prevsnippetlist = hashdataset[snippet.len][prevsnippet.hash]
        if nextsnippet is not None: nextsnippetlist = hashdataset[snippet.len][nextsnippet.hash]
        if len(snippetlist) <= 1: return False
        if len(prevsnippetlist) > 1 or len(nextsnippetlist) > 1: return True
        return False

    @staticmethod
    def nextSnippetMethod(snippet):
        return SnippetMethodFactory.snippetMethod(snippet.method, snippet.start + 1, snippet.len, None)
    
    @staticmethod
    def prevSnippetMethod(snippet):
        return SnippetMethodFactory.snippetMethod(snippet.method, snippet.start - 1, snippet.len, None)
    pass

class ClazzMethodTokenFactory:
    TOKENMAP = {} # <str`token`, int`token value id`>

    @staticmethod
    def onMethodCreated(clazzMethod):
        TOKENMAP = ClazzMethodTokenFactory.TOKENMAP
        tokens = clazzMethod.tokens
        for token in tokens:
            if(token not in TOKENMAP):
                size = len(TOKENMAP)
                TOKENMAP[token] = size + 1
    
    @staticmethod
    def valueof(token:str):
        TOKENMAP = ClazzMethodTokenFactory.TOKENMAP
        if(token in TOKENMAP):
            return TOKENMAP[token]
        else:
            return 0 # throw?

    @staticmethod
    def R():
        """for rk algo"""
        return len(ClazzMethodTokenFactory.TOKENMAP)

    @staticmethod
    def RM(r: int, m:int, q:int):
        """for rk algo"""
        rm = 1
        for i in range(m): rm = (rm * r) % q
        return rm
    
    @staticmethod
    def Q():
        """for rk algo"""
        # return 1363005552434666078217421284621279933627102780881053358473
        return 285542542228279613901563566102164008326164238644702889199247456602284400390600653875954571505539843239754513915896150297878399377056071435169747221107988791198200988477531339214282772016059009904586686254989084815735422480409022344297588352526004383890632616124076317387416881148592486188361873904175783145696016919574390765598280188599035578448591077683677175520434074287726578006266759615970759521327828555662781678385691581844436444812511562428136742490459363212810180276096088111401003377570363545725120924073646921576797146199387619296560302680261790118132925012323046444438622308877924609373773012481681672424493674474488537770155783006880852648161513067144814790288366664062257274665275787127374649231096375001170901890786263324619578795731425693805073056119677580338084333381987500902968831935913095269821311141322393356490178488728982288156282600813831296143663845945431144043753821542871277745606447858564159213328443580206422714694913091762716447041689678070096773590429808909616750452927258000843500344831628297089902728649981994387647234574276263729694848304750917174186181130688518792748622612293341368928056634384466646326572476167275660839105650528975713899320211121495795311427946254553305387067821067601768750977866100460014602138408448021225053689054793742003095722096732954750721718115531871310231057902608580607
    pass