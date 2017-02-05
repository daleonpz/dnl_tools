#!/usr/bin/python2.7

###############################
#  T O   D O
###############################
# - add new jobs
# - mark jobs as done

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
    print "\t-h, --help\t\t\t: display help"
    print "\t-H, --headers\t\t\t: display available headers in your todolist.org" 
    print "\t-j, --jobs [header]\t\t: retrieve jobs from a specific header"
    print "\t-c, --completion [header]\t: job completion"


################################
#   C L A S S E S 
################################
class todo(object):
    def __init__(self):
        infile = open("/home/dnl/Documents/gitStuff/dnl_tools/todo.org")
        self.string = infile.read()
        infile.close()

    def headers(self):
        # need to delete the last whitespace
        head = re.findall("\*\* ([A-Za-z\s-]+)", self.string)
        print "    "+"\n    ".join(head)

    def completion_percentage(self, head):
        jobs = re.findall("\*\* " + head + " \[(.+)\]" , self.string)
        jobs = re.split("/", jobs[0] )  
        print "Completion status:"
        print "     %s of %s (%.2f %%)" % (
                jobs[0],
                jobs[1],
                float(jobs[0]) /  float(jobs[1]) * 100.0)
 

    def job_retrieval(self, head):
        pattern = re.compile("\*\* "+ head + " (.+?)\*\*", re.DOTALL)
        jobs = re.findall(pattern, self.string)
        jobs = re.split( "\n", jobs[0] )[1:-1]
        #jobs = [re.sub(" - \[.\] ","",x) for x in jobs] 
        print "    " + "\n    ".join(jobs)


################################
#   M A I N
################################
def main():
    dolist = todo()
    try:
        opts, args = getopt.getopt(sys.argv[1:] , "hHj:c:", ["jobs=","completion="]  )
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
        elif opt in ( '-c', '--completion'):
            dolist.completion_percentage(arg)
        else:
            assert False, "unhandled option"


if __name__ == "__main__":
    main()
