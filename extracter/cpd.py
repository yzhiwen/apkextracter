from optparse import OptionParser
from cpd.cpder import Cpder

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: cpd.py [options] file")

    parser.add_option("-t", "--minitokens", dest="minitokens", default=100,
        help="the lowest tokens, default: 100", type="int")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        file = args[0]
        Cpder().startup(file, options.minitokens)