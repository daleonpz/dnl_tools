#!/usr/bin/python2.7
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
            'test'      : cls.test()
            }.get(key, list_func(todo) )

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
        return re.findall("\*\* ([A-Za-z\s-]+)", self.string)

    def test(self):
        return "test"


################################
#   M A I N
################################
def main():
    dolist = todo()
    try:
        opts, args = getopt.getopt(sys.argv[1:] , "hf:", ["function="]  )
    except getopt.GetoptError:
        print 'todo_list.py -f <function>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print "Valid inputs:"
            print "-f, --function:\n\t" + list_func(todo)
            sys.exit()
        elif opt in ( '-f', '--function'):
            print select_func(arg, dolist)
        else:
            assert False, "unhandled option"


if __name__ == "__main__":
    main()


#script, func = argv
#dolist = todo()

#print select_func(func, dolist)

