from optparse import OptionParser
from cpd.cpder import Cpder

def packageref(package):
    if package is None: return "";
    if package == "": return "";
    if package == ".": return "";
    if "." in package: return package.replace(".", "/")
    return package

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: cpd.py [options] file")

    parser.add_option("-t", "--minitokens", dest="minitokens", default=100,
        help="the lowest tokens, default: 100", type="int")

    parser.add_option("-p", "--package", dest="package", default="",
        help="specify the scan package name, '.' is all (default: application package name)", type="str")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        file = args[0]
        Cpder().startup(file, packageref(options.package), options.minitokens)
    else:
        parser.print_help()

"""
`some case`
class total:  142930
method total:  518955
smali file walker time:  112.19369530677795
method hash time:  151.45780849456787
hash walker time:  153.93056082725525
"""