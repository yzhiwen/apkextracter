from abc import abstractmethod

class Format:
    @abstractmethod
    def tokens(self, str): 
        pass
    pass

class Opcode:
    def __init__(self, name: str, format: Format):
        self.name = name
        self.format = format
    pass

class Format10x(Format):
    def tokens(self, str):
        """op"""
        return [str]

class Format12x(Format):
    def tokens(self, str):
        """op vA, vB"""
        return str.replace(",", "").split(" ")

class Format11n(Format):
    def tokens(self, str):
        """op vA, #+B"""
        return str.replace(",", "").split(" ")

class Format11x(Format):
    def tokens(self, str):
        """op vAA"""
        return str.split(" ")

class Format10t(Format):
    def tokens(self, str):
        """op +AA"""
        return str.split(" ")

class Format20t(Format):
    def tokens(self, str):
        """op +AAAA"""
        return str.split(" ")

class Format20bc(Format):
    def tokens(self, str):
        """op AA, kind@BBBB"""
        return str.replace(",", "").split(" ")

class Format22x(Format):
    def tokens(self, str):
        """op vAA, vBBBB"""
        return str.replace(",", "").split(" ")

class Format21t(Format):
    def tokens(self, str):
        """op vAA, +BBBB"""
        return str.replace(",", "").split(" ")

class Format21s(Format):
    def tokens(self, str):
        """op vAA, #+BBBB"""
        return str.replace(",", "").split(" ")

class Format21h(Format):
    def tokens(self, str):
        """
        op vAA, #+BBBB0000
        op vAA, #+BBBB000000000000
        """
        return str.replace(",", "").split(" ")

class Format21c(Format):
    def tokens(self, str):
        """
        op vAA, type@BBBB
        op vAA, field@BBBB
        op vAA, method_handle@BBBB
        op vAA, proto@BBBB
        op vAA, string@BBBB
        """
        return str.replace(",", "").split(" ")

class Format23x(Format):
    def tokens(self, str):
        """op vAA, vBB, vCC"""
        return str.replace(",", "").split(" ")

class Format22b(Format):
    def tokens(self, str):
        """op vAA, vBB, #+CC"""
        return str.replace(",", "").split(" ")

class Format22t(Format):
    def tokens(self, str):
        """op vA, vB, +CCCC"""
        return str.replace(",", "").split(" ")

class Format22s(Format):
    def tokens(self, str):
        """op vA, vB, #+CCCC"""
        return str.replace(",", "").split(" ")

class Format22c(Format):
    def tokens(self, str):
        """
        op vA, vB, type@CCCC
        op vA, vB, field@CCCC
        """
        return str.replace(",", "").split(" ")

class Format22cs(Format):
    def tokens(self, str):
        """op vA, vB, fieldoff@CCCC"""
        return str.replace(",", "").split(" ")

class Format30t(Format):
    def tokens(self, str):
        """op +AAAAAAAA"""
        return str.split(" ")

class Format32x(Format):
    def tokens(self, str):
        """op vAAAA, vBBBB"""
        return str.replace(",", "").split(" ")

class Format31i(Format):
    def tokens(self, str):
        """op vAA, #+BBBBBBBB"""
        return str.replace(",", "").split(" ")

class Format31t(Format):
    def tokens(self, str):
        """op vAA, +BBBBBBBB"""
        return str.replace(",", "").split(" ")

class Format31c(Format):
    def tokens(self, str):
        """op vAA, string@BBBBBBBB"""
        return str.replace(",", "").split(" ")

# ....
class Format35c(Format):
    def tokens(self, str):
        """
        [A=5] op {vC, vD, vE, vF, vG}, meth@BBBB
        [A=5] op {vC, vD, vE, vF, vG}, site@BBBB
        [A=5] op {vC, vD, vE, vF, vG}, type@BBBB
        [A=4] op {vC, vD, vE, vF}, kind@BBBB
        [A=3] op {vC, vD, vE}, kind@BBBB
        [A=2] op {vC, vD}, kind@BBBB
        [A=1] op {vC}, kind@BBBB
        [A=0] op {}, kind@BBBB
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format35ms(Format):
    def tokens(self, str):
        """
        [A=5] op {vC, vD, vE, vF, vG}, vtaboff@BBBB
        [A=4] op {vC, vD, vE, vF}, vtaboff@BBBB
        [A=3] op {vC, vD, vE}, vtaboff@BBBB
        [A=2] op {vC, vD}, vtaboff@BBBB
        [A=1] op {vC}, vtaboff@BBBB
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format35mi(Format):
    def tokens(self, str):
        """
        [A=5] op {vC, vD, vE, vF, vG}, inline@BBBB
        [A=4] op {vC, vD, vE, vF}, inline@BBBB
        [A=3] op {vC, vD, vE}, inline@BBBB
        [A=2] op {vC, vD}, inline@BBBB
        [A=1] op {vC}, inline@BBBB
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]
    
class Format3rc(Format):
    def tokens(self, str):
        """
        op {vCCCC .. vNNNN}, meth@BBBB
        op {vCCCC .. vNNNN}, site@BBBB
        op {vCCCC .. vNNNN}, type@BBBB
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format3rms(Format):
    def tokens(self, str):
        """
        op {vCCCC .. vNNNN}, vtaboff@BBBB
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format3rmi(Format):
    def tokens(self, str):
        """
        op {vCCCC .. vNNNN}, inline@BBBB
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format45cc(Format):
    def tokens(self, str):
        """
        [A=5] op {vC, vD, vE, vF, vG}, meth@BBBB, proto@HHHH
        [A=4] op {vC, vD, vE, vF}, meth@BBBB, proto@HHHH
        [A=3] op {vC, vD, vE}, meth@BBBB, proto@HHHH
        [A=2] op {vC, vD}, meth@BBBB, proto@HHHH
        [A=1] op {vC}, meth@BBBB, proto@HHHH
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format4rcc(Format):
    def tokens(self, str:str):
        """
        op> {vCCCC .. vNNNN}, meth@BBBB, proto@HHHH
        """
        l = str.find("{")
        r = str.find("}")
        if l == -1 or r == -1: return str
        return [str[0:l].strip(), str[l:r+1], str[r+2:len(str)].strip()]

class Format51l(Format):
    def tokens(self, str):
        """
        op vAA, #+BBBBBBBBBBBBBBBB
        """
        return str.replace(",", "").split(" ")