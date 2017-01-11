#!/usr/bin/python2.7

###############################
#  T O   D O
###############################
# - add new jobs
# - mark jobs as done
# - query jobs from headers

################################
#   I M P O R T S
################################
import re
import getopt
import sys   

from types  import FunctionType

################################
#   F U N C T I O N S
################################
def list_func(cls):
    funcs = [x for x, y in cls.__dict__.items() if (type(y) == FunctionType  and not x.startswith('_')) ]
    # funcs = ['a', 'b']
    # "\n\t".join(funcs) :>  'a' + '\n\t' + 'b'
    return  "\n\t".join(funcs)


def select_func(key, cls):
    return {
            'headers'   : cls.headers(),
            'getjob'    : cls.test()
            }.get(key, list_func(todo) )

def usage():
    print "Usage:"
    print "\t-h, --help\t\t: display help"
    print "\t-H, --headers\t\t: display available headers in your todolist.org" 
    print "\t-j, --jobs [header]\t: retrieve jobs from a specific header"


################################
#   C L A S S E S 
################################
class todo(object):
    def __init__(self):
        infile = open("/home/dnl/Documents/MyStuff/dnl_tools/todo.org")
        self.string = infile.read()
        infile.close()

    def headers(self):
        # need to delete the last whitespace
        head = re.findall("\*\* ([A-Za-z\s-]+)", self.string)
        print "    "+"\n    ".join(head)

    def job_retrieval(self, arg):
        print arg


################################
#   M A I N
################################
def main():
    dolist = todo()
    try:
        opts, args = getopt.getopt(sys.argv[1:] , "hHj:", ["jobs="]  )
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if (opts == []):
            usage()
            sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ( '-H', '--headers'):
            dolist.headers()
        elif opt in ( '-j', '--jobs'):
            dolist.job_retrieval(arg)
        else:
            assert False, "unhandled option"


if __name__ == "__main__":
    main()
