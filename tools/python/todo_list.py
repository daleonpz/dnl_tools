#!/usr/bin/python2.7

###############################
#  T O   D O
###############################
# - add new jobs
# - mark jobs as done
# - bug: error when header is contains blank spaces

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
        h = ['%-22s' '%s' % (x, self.completion_status(x)) for x in head ]
        print "    "+"\n    ".join(h)

    def completion_status(self, head):
        h = re.findall('^\s*(.*[a-zA-Z])\s*',head)[0]
        jobs = re.findall("\*\* " + h + "\s*\[(.+)\]" , self.string)
        try:
            jobs = re.split("/", jobs[0] )  
            return "     %s of %s (%.2f %%)" % (
                jobs[0],
                jobs[1],
                float(jobs[0]) /  float(jobs[1]) * 100.0)
        except IndexError:
            print "Invalid header"
            usage()
            sys.exit(2)

    def completion_percentage(self, head):
        print "Completion status:"
        print self.completion_status(head) 

    def job_retrieval(self, head):
        h = re.findall('^\s*(.*)$',head)[0];
     #
     # ^\*{2}.+[\n\r]       # match the beginning of the line, followed by two stars, anything else in between and a newline
    # (?P<block>           # open group "block"
    # (?:              # non-capturing group
    #    (?!^\*{2})   # a neg. lookahead, making sure no ** follows at the beginning of a line
    #    [\s\S]       # any character...
    # )+               # ...at least once
    # )                    # close group "block" 
        pattern = re.compile(r'^\*{2} ' + re.escape(h) + r'.+[\n\r](?P<block>(?:(?!^\*{2})[\s\S])+)', re.MULTILINE)
	try:
		items = pattern.search(self.string)
                print items.group('block')[:-2] 
	except:
		print "Invalid header"
                print "Display headers with -H option"
                sys.exit(2)


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
